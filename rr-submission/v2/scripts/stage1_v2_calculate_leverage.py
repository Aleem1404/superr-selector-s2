import pandas as pd
import numpy as np
import glob
import os
import json

def run_stage1_v2():
    print("=" * 60)
    print("STAGE 1 (v2): Ingesting Official Data + ball-to-ball-stats Enriched Venues & Phases")
    print("=" * 60)
    
    # 1. Load official data
    bbb = pd.read_csv('data/ball_by_ball.csv')
    matches = pd.read_csv('data/matches.csv')
    comps = pd.read_csv('data/competitions.csv')
    
    # 2. Extract IPL venue and phase mapping from ball-to-ball-stats
    print("Loading enriched IPL match metadata from ball-to-ball-stats...")
    ipl_files = sorted(glob.glob('ball-to-ball-stats/ipl_*_deliveries.csv'))
    ipl_dfs = []
    for f in ipl_files:
        df = pd.read_csv(f)
        ipl_dfs.append(df)
    all_ipl_balls = pd.concat(ipl_dfs, ignore_index=True)
    
    # Compute venue par economy
    all_ipl_balls['total_runs'] = all_ipl_balls['runs_of_bat'] + all_ipl_balls['extras']
    venue_stats = all_ipl_balls.groupby('venue').agg(
        v_balls=('total_runs', 'count'),
        v_runs=('total_runs', 'sum')
    ).reset_index()
    venue_stats['venue_par_rpo'] = ((venue_stats['v_runs'] / venue_stats['v_balls']) * 6.0).round(2)
    
    # Match metadata from ball-to-ball-stats
    ipl_match_meta = all_ipl_balls.groupby(['season', 'match_no']).agg(
        venue=('venue', 'first'),
        phase=('phase', 'first'),
        date=('date', 'first')
    ).reset_index()
    
    # Merge venue par
    ipl_match_meta = ipl_match_meta.merge(venue_stats[['venue', 'venue_par_rpo']], on='venue', how='left')
    ipl_match_meta['phase'] = ipl_match_meta['phase'].fillna('Group Stage')
    
    # Map comp_id to season for IPL in matches.csv
    comp_season_map = {
        1358: 2022,
        1715: 2023,
        2193: 2024,
        2725: 2025,
        3298: 2026
    }
    matches['season'] = matches['comp_id'].map(comp_season_map)
    matches['is_ipl'] = matches['season'].notna()
    
    # Merge matches with ipl_match_meta
    matches = matches.merge(
        ipl_match_meta[['season', 'match_no', 'venue', 'phase', 'venue_par_rpo']],
        left_on=['season', 'match_number'],
        right_on=['season', 'match_no'],
        how='left'
    )
    
    # Fill defaults for non-IPL international matches
    matches['venue'] = matches['venue'].fillna('International / Neutral Venue')
    default_phase = np.where(matches['knock_out'] == 1, 'Knockout', 'Group Stage')
    matches['phase'] = np.where(matches['phase'].notna(), matches['phase'], default_phase)
    matches['venue_par_rpo'] = matches['venue_par_rpo'].fillna(8.85) # Global T20 par baseline
    
    # 3. Stage & Knockout Leverage Weights in v2
    # Finals = 1.30x, Qualifiers/Eliminators = 1.20x, Regular Knockouts = 1.15x
    def get_phase_multiplier(row):
        phase_str = str(row['phase']).lower()
        if 'final' in phase_str:
            return 1.30
        elif any(k in phase_str for k in ['qualifier', 'eliminator', 'super 4']):
            return 1.20
        elif row['knock_out'] == 1 or str(row['stage']).lower() in ['final', 'semi final', 'qualifier', 'eliminator']:
            return 1.15
        return 1.00
        
    matches['phase_multiplier'] = matches.apply(get_phase_multiplier, axis=1)
    
    # IPL match competition fidelity multiplier (IPL delivers highest opposition quality)
    matches['comp_fidelity'] = np.where(matches['is_ipl'], 1.15, 1.00)
    
    # Sort deliveries
    bbb = bbb.sort_values(by=['match_id', 'innings', 'innings_ball_num', 'overid', 'over_ball_num']).reset_index(drop=True)
    
    # Merge match info into BBB
    m_cols = ['match_id', 'is_ipl', 'venue', 'venue_par_rpo', 'phase', 'phase_multiplier', 'comp_fidelity', 'revised_target', 'win_team_id']
    bbb = bbb.merge(matches[m_cols], on='match_id', how='left')
    
    # Run bookkeeping
    bbb['is_legal'] = ~bbb['extras_type'].isin(['wide', 'Overstep'])
    ball_team_runs = bbb['runs'].copy()
    ball_team_runs += bbb['extras_2_runs'].fillna(0)
    ball_team_runs += (bbb['extras_type'] == 'wide') * 1
    ball_team_runs += (bbb['extras_type'] == 'Overstep') * 1
    ball_team_runs += (bbb['extras_type'].isin(['legbyes', 'byes', 'other', 'Penalty']) & (bbb['runs'] == 0)) * 1
    bbb['ball_team_runs'] = ball_team_runs
    bbb['bowler_runs'] = bbb['runs'] + (bbb['extras_type'] == 'wide') * 1 + (bbb['extras_type'] == 'Overstep') * 1
    
    # Cumulative stats
    bbb['cum_runs'] = bbb.groupby(['match_id', 'innings'])['ball_team_runs'].cumsum() - bbb['ball_team_runs']
    bbb['cum_legal_balls'] = bbb.groupby(['match_id', 'innings'])['is_legal'].cumsum() - bbb['is_legal'].astype(int)
    bbb['cum_wickets'] = bbb.groupby(['match_id', 'innings'])['is_wicket'].cumsum() - bbb['is_wicket'].astype(int)
    
    # Innings 1 total
    inn1_totals = bbb[bbb['innings'] == 1].groupby('match_id')['ball_team_runs'].sum().reset_index()
    inn1_totals.columns = ['match_id', 'inn1_total']
    bbb = bbb.merge(inn1_totals, on='match_id', how='left')
    
    # Chasing leverage
    bbb['target'] = np.where(bbb['revised_target'].notna(), bbb['revised_target'], bbb['inn1_total'] + 1)
    bbb['balls_rem'] = np.maximum(0, 120 - bbb['cum_legal_balls'])
    bbb['runs_req'] = np.maximum(0, bbb['target'] - bbb['cum_runs'])
    bbb['rrr'] = np.where(bbb['balls_rem'] > 0, bbb['runs_req'] / (bbb['balls_rem'] / 6.0), 36.0)
    bbb['wickets_in_hand'] = np.maximum(0, 10 - bbb['cum_wickets'])
    
    # Formulate Pressure Index (v2) with venue adjustment
    # Centered at venue par RPO instead of fixed 9.0
    u_rrr = 1.0 / (1.0 + np.exp(-0.5 * (bbb['rrr'] - bbb['venue_par_rpo'])))
    d_balls = 1.0 - (bbb['balls_rem'] / 120.0)
    w_lev = 1.0 - (bbb['wickets_in_hand'] / 10.0)**1.2
    p_chase = 0.40 * u_rrr + 0.35 * d_balls * (bbb['rrr'] / bbb['venue_par_rpo']) + 0.25 * w_lev
    
    # Innings 1: Death Overs & Crisis Collapse
    is_death = (bbb['overid'] >= 16).astype(float)
    death_p = 0.55 + 0.08 * (bbb['overid'] - 16) + 0.15 * (bbb['cum_wickets'] / 10.0)
    crisis_p = np.where((bbb['overid'] <= 6) & (bbb['cum_wickets'] >= 3), 0.70,
               np.where((bbb['overid'] <= 10) & (bbb['cum_wickets'] >= 4), 0.65, 0.30))
    p_inn1 = np.maximum(is_death * death_p, crisis_p)
    
    # Base PI v2
    pi_v2 = np.where(bbb['innings'] == 2, p_chase,
            np.where(bbb['innings'] == 1, p_inn1, 1.0))
    
    # Apply Stage Multiplier
    pi_v2 = pi_v2 * bbb['phase_multiplier']
    bbb['pressure_index_v2'] = np.clip(pi_v2, 0.0, 1.0).round(4)
    bbb['is_hp_v2'] = bbb['pressure_index_v2'] >= 0.60
    
    out_cols = [
        'match_id', 'is_ipl', 'venue', 'venue_par_rpo', 'phase', 'phase_multiplier', 'comp_fidelity',
        'innings', 'overid', 'over_ball_num', 'innings_ball_num',
        'striker_id', 'striker_name', 'bowler_id', 'bowler_name',
        'runs', 'is_four', 'is_six', 'is_wicket', 'is_legal', 'bowler_runs',
        'target', 'balls_rem', 'runs_req', 'rrr', 'pressure_index_v2', 'is_hp_v2'
    ]
    
    out_csv = 'rr-submission/v2/stage1_ball_leverage/ball_by_ball_pressure_v2.csv'
    print(f"Writing v2 ball-level pressure data to: {out_csv} ...")
    bbb[out_cols].to_csv(out_csv, index=False)
    
    summary = {
        'total_deliveries': len(bbb),
        'high_pressure_deliveries_v2': int(bbb['is_hp_v2'].sum()),
        'high_pressure_percentage_v2': round(float(bbb['is_hp_v2'].mean() * 100), 2),
        'ipl_deliveries': int(bbb['is_ipl'].sum()),
        'total_matches': int(bbb['match_id'].nunique()),
        'unique_venues_tracked': int(bbb['venue'].nunique())
    }
    
    with open('rr-submission/v2/stage1_ball_leverage/stage1_summary_v2.json', 'w') as f:
        json.dump(summary, f, indent=2)
        
    print(f"STAGE 1 (v2) COMPLETE:")
    print(f"  * Total Deliveries: {summary['total_deliveries']:,}")
    print(f"  * High-Pressure Deliveries (v2): {summary['high_pressure_deliveries_v2']:,} ({summary['high_pressure_percentage_v2']}%)")
    print(f"  * IPL Deliveries with Enriched Venue: {summary['ipl_deliveries']:,}")

if __name__ == '__main__':
    run_stage1_v2()
