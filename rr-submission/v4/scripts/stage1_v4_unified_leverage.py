import pandas as pd
import numpy as np
import glob
import os
import json

def run_stage1_v4():
    print("=" * 70)
    print("STAGE 1 (v4): Unified Contextual Leverage Framework")
    print("  - 17 Venue Pitch Pars")
    print("  - Playoff Multipliers (1.20x / 1.30x)")
    print("  - Option A: Opposition Quality Tiering (Bowler Quality & Wicket Value)")
    print("  - Option B: Chase Urgency Asymmetry (RRR vs Venue Par)")
    print("  - Option C: Entry Point Cohort Classification (Anchor vs Finisher)")
    print("=" * 70)
    
    # 1. Load official data
    bbb = pd.read_csv('data/ball_by_ball.csv')
    matches = pd.read_csv('data/matches.csv')
    comps = pd.read_csv('data/competitions.csv')
    
    # 2. Extract IPL venue and phase mapping from ball-to-ball-stats
    print("[1/5] Ingesting stadium pars from ball-to-ball-stats...")
    ipl_files = sorted(glob.glob('ball-to-ball-stats/ipl_*_deliveries.csv'))
    ipl_dfs = [pd.read_csv(f) for f in ipl_files]
    all_ipl_balls = pd.concat(ipl_dfs, ignore_index=True)
    
    all_ipl_balls['total_runs'] = all_ipl_balls['runs_of_bat'] + all_ipl_balls['extras']
    venue_stats = all_ipl_balls.groupby('venue').agg(
        v_balls=('total_runs', 'count'),
        v_runs=('total_runs', 'sum')
    ).reset_index()
    venue_stats['venue_par_rpo'] = ((venue_stats['v_runs'] / venue_stats['v_balls']) * 6.0).round(2)
    
    ipl_match_meta = all_ipl_balls.groupby(['season', 'match_no']).agg(
        venue=('venue', 'first'),
        phase=('phase', 'first'),
        date=('date', 'first')
    ).reset_index()
    ipl_match_meta = ipl_match_meta.merge(venue_stats[['venue', 'venue_par_rpo']], on='venue', how='left')
    ipl_match_meta['phase'] = ipl_match_meta['phase'].fillna('Group Stage')
    
    comp_season_map = {1358: 2022, 1715: 2023, 2193: 2024, 2725: 2025, 3298: 2026}
    matches['season'] = matches['comp_id'].map(comp_season_map)
    matches['is_ipl'] = matches['season'].notna()
    
    matches = matches.merge(
        ipl_match_meta[['season', 'match_no', 'venue', 'phase', 'venue_par_rpo']],
        left_on=['season', 'match_number'],
        right_on=['season', 'match_no'],
        how='left'
    )
    
    matches['venue'] = matches['venue'].fillna('International / Neutral Venue')
    default_phase = np.where(matches['knock_out'] == 1, 'Knockout', 'Group Stage')
    matches['phase'] = np.where(matches['phase'].notna(), matches['phase'], default_phase)
    matches['venue_par_rpo'] = matches['venue_par_rpo'].fillna(8.85)
    
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
    matches['comp_fidelity'] = np.where(matches['is_ipl'], 1.15, 1.00)
    
    # Sort deliveries
    bbb = bbb.sort_values(by=['match_id', 'innings', 'innings_ball_num', 'overid', 'over_ball_num']).reset_index(drop=True)
    m_cols = ['match_id', 'is_ipl', 'venue', 'venue_par_rpo', 'phase', 'phase_multiplier', 'comp_fidelity', 'revised_target', 'win_team_id']
    bbb = bbb.merge(matches[m_cols], on='match_id', how='left')
    
    # Bookkeeping
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
    
    inn1_totals = bbb[bbb['innings'] == 1].groupby('match_id')['ball_team_runs'].sum().reset_index()
    inn1_totals.columns = ['match_id', 'inn1_total']
    bbb = bbb.merge(inn1_totals, on='match_id', how='left')
    
    bbb['target'] = np.where(bbb['revised_target'].notna(), bbb['revised_target'], bbb['inn1_total'] + 1)
    bbb['balls_rem'] = np.maximum(0, 120 - bbb['cum_legal_balls'])
    bbb['runs_req'] = np.maximum(0, bbb['target'] - bbb['cum_runs'])
    bbb['rrr'] = np.where(bbb['balls_rem'] > 0, bbb['runs_req'] / (bbb['balls_rem'] / 6.0), 36.0)
    bbb['wickets_in_hand'] = np.maximum(0, 10 - bbb['cum_wickets'])
    
    # [OPTION B] Chase Asymmetry: Non-linear escalation when chasing above venue par
    print("[2/5] Formulating Innings Chase Asymmetry (Option B)...")
    u_rrr = 1.0 / (1.0 + np.exp(-0.5 * (bbb['rrr'] - bbb['venue_par_rpo'])))
    d_balls = 1.0 - (bbb['balls_rem'] / 120.0)
    w_lev = 1.0 - (bbb['wickets_in_hand'] / 10.0)**1.2
    
    # Chase Asymmetry Multiplier: 1.00x up to 1.15x for high RRR chases
    chase_asymmetry_mult = np.where(
        bbb['innings'] == 2,
        1.0 + 0.15 * np.clip((bbb['rrr'] - bbb['venue_par_rpo']) / (bbb['venue_par_rpo'] + 1e-6), 0.0, 1.0),
        1.00
    )
    p_chase = (0.40 * u_rrr + 0.35 * d_balls * (bbb['rrr'] / bbb['venue_par_rpo']) + 0.25 * w_lev) * chase_asymmetry_mult
    
    # Innings 1: Death Overs & Crisis Collapse
    is_death = (bbb['overid'] >= 16).astype(float)
    death_p = 0.55 + 0.08 * (bbb['overid'] - 16) + 0.15 * (bbb['cum_wickets'] / 10.0)
    crisis_p = np.where((bbb['overid'] <= 6) & (bbb['cum_wickets'] >= 3), 0.70,
               np.where((bbb['overid'] <= 10) & (bbb['cum_wickets'] >= 4), 0.65, 0.30))
    p_inn1 = np.maximum(is_death * death_p, crisis_p)
    
    # Base PI before opposition quality
    pi_base = np.where(bbb['innings'] == 2, p_chase,
              np.where(bbb['innings'] == 1, p_inn1, 1.0))
    pi_base = pi_base * bbb['phase_multiplier']
    
    # [OPTION A] Opposition Quality Tiering (Bowler Tiers & Batter Dismissal Value)
    print("[3/5] Calibrating Opposition Quality & Wicket Value (Option A)...")
    # Pre-identify elite bowlers by career economy in pressure
    bowler_agg = bbb.groupby('bowler_name').agg(
        b_balls=('is_legal', 'sum'),
        b_runs=('bowler_runs', 'sum'),
        b_wkts=('is_wicket', 'sum')
    ).reset_index()
    bowler_agg = bowler_agg[bowler_agg['b_balls'] >= 150]
    bowler_agg['econ'] = (bowler_agg['b_runs'] / bowler_agg['b_balls']) * 6.0
    bowler_agg['wkt_pct'] = (bowler_agg['b_wkts'] / bowler_agg['b_balls']) * 100.0
    
    # Elite bowlers: econ <= 7.80 or wkt_pct >= 9.0%
    elite_bowlers = set(bowler_agg[(bowler_agg['econ'] <= 7.85) | (bowler_agg['wkt_pct'] >= 9.5)]['bowler_name'])
    
    # Bowler Quality Multiplier for Batter: 1.15x for facing Elite, 1.00x Standard, 0.88x Part-Timer (<60 balls)
    part_timers = set(bowler_agg[bowler_agg['b_balls'] < 80]['bowler_name'])
    
    bbb['bowler_tier_mult'] = np.where(bbb['bowler_name'].isin(elite_bowlers), 1.15,
                              np.where(bbb['bowler_name'].isin(part_timers), 0.88, 1.00))
    
    # Bowler Wicket Value: Dismissals in overs 1-15 (Top/Middle order) = 1.0x; Overs 16-20 with >= 7 wickets down (Tail) = 0.70x
    is_tailender_wkt = (bbb['overid'] >= 16) & (bbb['cum_wickets'] >= 7) & (bbb['is_wicket'] == 1)
    bbb['wkt_quality_weight'] = np.where(is_tailender_wkt, 0.70, 1.00)
    
    # [OPTION C] Role & Entry Point Cohort
    print("[4/5] Classifying Entry Point Tactical Cohorts (Option C)...")
    # Identify entry over for striker in each match
    batter_entry = bbb.groupby(['match_id', 'striker_id'])['overid'].min().reset_index()
    batter_entry.columns = ['match_id', 'striker_id', 'entry_over']
    bbb = bbb.merge(batter_entry, on=['match_id', 'striker_id'], how='left')
    bbb['tactical_cohort'] = np.where(bbb['entry_over'] <= 14, 'Anchor/Top-Order', 'Death Finisher')
    
    # Unified Effective Pressure Index (v4)
    # Blend base PI with bowler tier quality
    pi_v4 = pi_base * np.sqrt(bbb['bowler_tier_mult'])
    bbb['pressure_index_v4'] = np.clip(pi_v4, 0.0, 1.0).round(4)
    bbb['is_hp_v4'] = bbb['pressure_index_v4'] >= 0.60
    
    # Save output
    out_cols = [
        'match_id', 'is_ipl', 'venue', 'venue_par_rpo', 'phase', 'phase_multiplier', 'comp_fidelity',
        'innings', 'overid', 'over_ball_num', 'innings_ball_num',
        'striker_id', 'striker_name', 'bowler_id', 'bowler_name', 'bowler_tier_mult', 'tactical_cohort',
        'runs', 'is_four', 'is_six', 'is_wicket', 'wkt_quality_weight', 'is_legal', 'bowler_runs',
        'target', 'balls_rem', 'runs_req', 'rrr', 'pressure_index_v4', 'is_hp_v4'
    ]
    
    out_csv = 'rr-submission/v4/stage1_ball_leverage/ball_by_ball_pressure_v4.csv'
    print(f"[5/5] Writing v4 ball-level unified pressure dataset to: {out_csv} ...")
    bbb[out_cols].to_csv(out_csv, index=False)
    
    summary = {
        'total_deliveries': len(bbb),
        'high_pressure_deliveries_v4': int(bbb['is_hp_v4'].sum()),
        'high_pressure_percentage_v4': round(float(bbb['is_hp_v4'].mean() * 100), 2),
        'ipl_deliveries': int(bbb['is_ipl'].sum()),
        'elite_bowler_count': len(elite_bowlers),
        'venues_calibrated': int(bbb['venue'].nunique())
    }
    
    with open('rr-submission/v4/stage1_ball_leverage/stage1_summary_v4.json', 'w') as f:
        json.dump(summary, f, indent=2)
        
    print("\nSTAGE 1 (v4) COMPLETE:")
    print(f"  * Total Deliveries: {summary['total_deliveries']:,}")
    print(f"  * High-Pressure Deliveries (v4): {summary['high_pressure_deliveries_v4']:,} ({summary['high_pressure_percentage_v4']}%)")
    print(f"  * Elite Bowlers Categorized: {summary['elite_bowler_count']}")

if __name__ == '__main__':
    run_stage1_v4()

