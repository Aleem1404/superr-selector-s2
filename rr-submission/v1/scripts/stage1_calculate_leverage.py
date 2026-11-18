import pandas as pd
import numpy as np
import os
import json

def run_stage1():
    print("=" * 60)
    print("STAGE 1: Ingesting Raw Data & Computing Ball-Level Pressure Index (PI)")
    print("=" * 60)
    
    bbb_path = 'data/ball_by_ball.csv'
    matches_path = 'data/matches.csv'
    comps_path = 'data/competitions.csv'
    
    print("Loading official RR match and ball-by-ball files...")
    bbb = pd.read_csv(bbb_path)
    matches = pd.read_csv(matches_path)
    comps = pd.read_csv(comps_path)
    
    # Sort deliveries strictly by chronological sequence
    bbb = bbb.sort_values(by=['match_id', 'innings', 'innings_ball_num', 'overid', 'over_ball_num']).reset_index(drop=True)
    
    # 1. Competition Tier Weighting
    comp_type = {}
    for _, row in comps.iterrows():
        cid = row['comp_id']
        cname = str(row['comp_name'])
        if 'IPL' in cname:
            comp_type[cid] = 1.00 # Highest competition density
        elif any(k in cname for k in ['Asia Cup', 'World Cup', 'Australia', 'India', 'England', 'South Africa']):
            comp_type[cid] = 0.95
        else:
            comp_type[cid] = 0.90
            
    matches['comp_weight'] = matches['comp_id'].map(comp_type).fillna(0.90)
    
    # Knockout Multiplier
    matches['is_knockout'] = (matches['knock_out'] == 1) | (matches['stage'].isin(['Final', 'Qualifier', 'Eliminator', 'Semi Final', 'Super 4']))
    
    # Merge match info
    m_info = matches[['match_id', 'comp_id', 'comp_weight', 'is_knockout', 'stage', 'revised_target', 'win_team_id']].copy()
    bbb = bbb.merge(m_info, on='match_id', how='left')
    
    # 2. Legal balls & Run Bookkeeping
    bbb['is_legal'] = ~bbb['extras_type'].isin(['wide', 'Overstep'])
    
    ball_team_runs = bbb['runs'].copy()
    ball_team_runs += bbb['extras_2_runs'].fillna(0)
    ball_team_runs += (bbb['extras_type'] == 'wide') * 1
    ball_team_runs += (bbb['extras_type'] == 'Overstep') * 1
    ball_team_runs += (bbb['extras_type'].isin(['legbyes', 'byes', 'other', 'Penalty']) & (bbb['runs'] == 0)) * 1
    bbb['ball_team_runs'] = ball_team_runs
    
    # Bowler runs
    bbb['bowler_runs'] = bbb['runs'] + (bbb['extras_type'] == 'wide') * 1 + (bbb['extras_type'] == 'Overstep') * 1
    
    # Cumulative stats per innings
    bbb['cum_runs'] = bbb.groupby(['match_id', 'innings'])['ball_team_runs'].cumsum() - bbb['ball_team_runs']
    bbb['cum_legal_balls'] = bbb.groupby(['match_id', 'innings'])['is_legal'].cumsum() - bbb['is_legal'].astype(int)
    bbb['cum_wickets'] = bbb.groupby(['match_id', 'innings'])['is_wicket'].cumsum() - bbb['is_wicket'].astype(int)
    
    # First innings total
    inn1_totals = bbb[bbb['innings'] == 1].groupby('match_id')['ball_team_runs'].sum().reset_index()
    inn1_totals.columns = ['match_id', 'inn1_total']
    bbb = bbb.merge(inn1_totals, on='match_id', how='left')
    
    # Second innings target & chasing metrics
    bbb['target'] = np.where(bbb['revised_target'].notna(), bbb['revised_target'], bbb['inn1_total'] + 1)
    bbb['balls_rem'] = np.maximum(0, 120 - bbb['cum_legal_balls'])
    bbb['runs_req'] = np.maximum(0, bbb['target'] - bbb['cum_runs'])
    bbb['rrr'] = np.where(bbb['balls_rem'] > 0, bbb['runs_req'] / (bbb['balls_rem'] / 6.0), 36.0)
    bbb['wickets_in_hand'] = np.maximum(0, 10 - bbb['cum_wickets'])
    
    # 3. Formulating Pressure Index (PI)
    # Innings 2: Chase Leverage
    u_rrr = 1.0 / (1.0 + np.exp(-0.5 * (bbb['rrr'] - 9.0)))
    d_balls = 1.0 - (bbb['balls_rem'] / 120.0)
    w_lev = 1.0 - (bbb['wickets_in_hand'] / 10.0)**1.2
    p_chase = 0.40 * u_rrr + 0.35 * d_balls * (bbb['rrr'] / 8.5) + 0.25 * w_lev
    
    # Innings 1: Death Overs & Crisis Collapse
    is_death = (bbb['overid'] >= 16).astype(float)
    death_p = 0.55 + 0.08 * (bbb['overid'] - 16) + 0.15 * (bbb['cum_wickets'] / 10.0)
    crisis_p = np.where((bbb['overid'] <= 6) & (bbb['cum_wickets'] >= 3), 0.70,
               np.where((bbb['overid'] <= 10) & (bbb['cum_wickets'] >= 4), 0.65, 0.30))
    p_inn1 = np.maximum(is_death * death_p, crisis_p)
    
    # Base PI
    pi = np.where(bbb['innings'] == 2, p_chase,
         np.where(bbb['innings'] == 1, p_inn1, 1.0))
    
    # Tournament Stakes Multiplier
    pi = np.where(bbb['is_knockout'], pi * 1.15, pi)
    bbb['pressure_index'] = np.clip(pi, 0.0, 1.0).round(4)
    bbb['is_hp'] = bbb['pressure_index'] >= 0.60
    
    # Output columns
    out_cols = [
        'match_id', 'innings', 'overid', 'over_ball_num', 'innings_ball_num',
        'striker_id', 'striker_name', 'bowler_id', 'bowler_name',
        'runs', 'is_four', 'is_six', 'is_wicket', 'is_legal', 'bowler_runs',
        'cum_runs', 'cum_legal_balls', 'cum_wickets', 'target', 'balls_rem', 'runs_req', 'rrr',
        'pressure_index', 'is_hp'
    ]
    
    out_csv = 'rr-submission/stage1_ball_leverage/ball_by_ball_pressure.csv'
    print(f"Writing ball-level pressure data to: {out_csv} ...")
    bbb[out_cols].to_csv(out_csv, index=False)
    
    summary = {
        'total_deliveries': len(bbb),
        'high_pressure_deliveries': int(bbb['is_hp'].sum()),
        'high_pressure_percentage': round(float(bbb['is_hp'].mean() * 100), 2),
        'total_matches': int(bbb['match_id'].nunique()),
        'innings_1_hp_balls': int(bbb[bbb['innings'] == 1]['is_hp'].sum()),
        'innings_2_hp_balls': int(bbb[bbb['innings'] == 2]['is_hp'].sum()),
        'super_overs_balls': int(bbb[bbb['innings'] > 2]['is_hp'].sum())
    }
    
    with open('rr-submission/stage1_ball_leverage/stage1_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
        
    print(f"STAGE 1 COMPLETE: {summary['total_deliveries']:,} deliveries processed.")
    print(f"  * High-Pressure Deliveries (PI >= 0.60): {summary['high_pressure_deliveries']:,} ({summary['high_pressure_percentage']}%)")
    print(f"  * Total Matches: {summary['total_matches']:,}")
    return bbb

if __name__ == '__main__':
    run_stage1()

