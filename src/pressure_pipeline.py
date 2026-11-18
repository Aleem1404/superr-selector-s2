import pandas as pd
import numpy as np
import os
import json

def run_pipeline():
    print("Loading datasets...")
    bbb = pd.read_csv('data/ball_by_ball.csv')
    matches = pd.read_csv('data/matches.csv')
    comps = pd.read_csv('data/competitions.csv')
    mapping = pd.read_csv('data/competition_team_player_mapping.csv')
    
    # Clean and sort deliveries
    bbb = bbb.sort_values(by=['match_id', 'innings', 'innings_ball_num', 'overid', 'over_ball_num']).reset_index(drop=True)
    
    # Competition tier weighting
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
    
    # Knockout flag
    matches['is_knockout'] = (matches['knock_out'] == 1) | (matches['stage'].isin(['Final', 'Qualifier', 'Eliminator', 'Semi Final', 'Super 4']))
    
    # Merge match info
    m_info = matches[['match_id', 'comp_id', 'comp_weight', 'is_knockout', 'stage', 'revised_target', 'win_team_id']].copy()
    bbb = bbb.merge(m_info, on='match_id', how='left')
    
    # Legal balls and run bookkeeping
    bbb['is_legal'] = ~bbb['extras_type'].isin(['wide', 'Overstep'])
    
    # Runs scored off bat vs extras
    ball_team_runs = bbb['runs'].copy()
    ball_team_runs += bbb['extras_2_runs'].fillna(0)
    ball_team_runs += (bbb['extras_type'] == 'wide') * 1
    ball_team_runs += (bbb['extras_type'] == 'Overstep') * 1
    ball_team_runs += (bbb['extras_type'].isin(['legbyes', 'byes', 'other', 'Penalty']) & (bbb['runs'] == 0)) * 1
    bbb['ball_team_runs'] = ball_team_runs
    
    # Bowler runs: bat runs + wide + overstep
    bbb['bowler_runs'] = bbb['runs'] + (bbb['extras_type'] == 'wide') * 1 + (bbb['extras_type'] == 'Overstep') * 1
    
    # Cumulative stats
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
    
    # --- PRESSURE INDEX (PI) CALCULATION ---
    # Innings 2: Leverage Index derived from RRR, balls remaining decay, and wickets in hand
    u_rrr = 1.0 / (1.0 + np.exp(-0.5 * (bbb['rrr'] - 9.0)))
    d_balls = 1.0 - (bbb['balls_rem'] / 120.0)
    w_lev = 1.0 - (bbb['wickets_in_hand'] / 10.0)**1.2
    p_chase = 0.40 * u_rrr + 0.35 * d_balls * (bbb['rrr'] / 8.5) + 0.25 * w_lev
    
    # Innings 1: Death overs execution + Crisis / Collapse recovery
    is_death = (bbb['overid'] >= 16).astype(float)
    death_p = 0.55 + 0.08 * (bbb['overid'] - 16) + 0.15 * (bbb['cum_wickets'] / 10.0)
    crisis_p = np.where((bbb['overid'] <= 6) & (bbb['cum_wickets'] >= 3), 0.70,
               np.where((bbb['overid'] <= 10) & (bbb['cum_wickets'] >= 4), 0.65, 0.30))
    p_inn1 = np.maximum(is_death * death_p, crisis_p)
    
    # Base PI
    pi = np.where(bbb['innings'] == 2, p_chase,
         np.where(bbb['innings'] == 1, p_inn1, 1.0)) # Super Overs = 1.0
    
    # Knockout / Tournament multiplier
    pi = np.where(bbb['is_knockout'], pi * 1.15, pi)
    bbb['pressure_index'] = np.clip(pi, 0.0, 1.0)
    bbb['is_hp'] = bbb['pressure_index'] >= 0.60
    
    print(f"Total deliveries: {len(bbb)}")
    print(f"High-Pressure deliveries: {bbb['is_hp'].sum()} ({bbb['is_hp'].mean()*100:.1f}%)")
    
    # --- BATTER ANALYSIS ---
    print("\nAnalyzing Batters...")
    # Ball-level metrics for batters
    bat = bbb.groupby(['striker_id', 'striker_name', 'is_hp']).agg(
        balls=('runs', 'count'),
        runs=('runs', 'sum'),
        dots=('runs', lambda s: (s == 0).sum()),
        boundaries=('runs', lambda s: (s.isin([4, 6])).sum()),
        fours=('is_four', 'sum'),
        sixes=('is_six', 'sum'),
        outs=('is_wicket', 'sum')
    ).reset_index()
    
    bat_p = bat.pivot(index=['striker_id', 'striker_name'], columns='is_hp', values=['balls', 'runs', 'dots', 'boundaries', 'outs', 'fours', 'sixes']).fillna(0)
    bat_p.columns = [f'{col}_{is_hp}' for col, is_hp in bat_p.columns]
    bat_p = bat_p.reset_index()
    
    bat_p['hp_balls'] = bat_p['balls_True']
    bat_p['base_balls'] = bat_p['balls_False']
    bat_p['total_balls'] = bat_p['hp_balls'] + bat_p['base_balls']
    
    # Empirical Bayes Shrinkage for Batters
    # Prior values (league HP averages)
    prior_hp_sr = 135.0
    prior_hp_dot = 36.0
    k_bat = 50.0 # Shrinkage strength (equivalent to 50 balls prior)
    
    bat_p['raw_hp_sr'] = (bat_p['runs_True'] / np.maximum(1, bat_p['hp_balls'])) * 100
    bat_p['shrunk_hp_sr'] = (bat_p['hp_balls'] / (bat_p['hp_balls'] + k_bat)) * bat_p['raw_hp_sr'] + (k_bat / (bat_p['hp_balls'] + k_bat)) * prior_hp_sr
    
    bat_p['base_sr'] = (bat_p['runs_False'] / np.maximum(1, bat_p['base_balls'])) * 100
    bat_p['delta_sr'] = bat_p['shrunk_hp_sr'] - bat_p['base_sr']
    
    bat_p['raw_hp_dot_pct'] = (bat_p['dots_True'] / np.maximum(1, bat_p['hp_balls'])) * 100
    bat_p['shrunk_hp_dot_pct'] = (bat_p['hp_balls'] / (bat_p['hp_balls'] + k_bat)) * bat_p['raw_hp_dot_pct'] + (k_bat / (bat_p['hp_balls'] + k_bat)) * prior_hp_dot
    
    bat_p['base_dot_pct'] = (bat_p['dots_False'] / np.maximum(1, bat_p['base_balls'])) * 100
    bat_p['delta_dot_pct'] = bat_p['base_dot_pct'] - bat_p['shrunk_hp_dot_pct'] # positive = reduces dots under pressure
    
    bat_p['hp_bnd_pct'] = (bat_p['boundaries_True'] / np.maximum(1, bat_p['hp_balls'])) * 100
    bat_p['hp_dismissal_rate'] = (bat_p['outs_True'] / np.maximum(1, bat_p['hp_balls'])) * 100
    
    # Match-level consistency for batters
    # For each match where batter faced >= 8 HP balls, evaluate if they produced above-average value added
    match_bat = bbb[bbb['is_hp']].groupby(['match_id', 'striker_id']).agg(
        hp_m_balls=('runs', 'count'),
        hp_m_runs=('runs', 'sum')
    ).reset_index()
    match_bat = match_bat[match_bat['hp_m_balls'] >= 8]
    match_bat['m_sr'] = (match_bat['hp_m_runs'] / match_bat['hp_m_balls']) * 100
    match_bat['is_clutch_inns'] = match_bat['m_sr'] >= 140.0
    
    consistency_bat = match_bat.groupby('striker_id').agg(
        clutch_inns_count=('is_clutch_inns', 'sum'),
        total_hp_inns=('is_clutch_inns', 'count')
    ).reset_index()
    consistency_bat['consistency_rate'] = consistency_bat['clutch_inns_count'] / np.maximum(1, consistency_bat['total_hp_inns'])
    
    bat_p = bat_p.merge(consistency_bat, on='striker_id', how='left')
    bat_p['consistency_rate'] = bat_p['consistency_rate'].fillna(0.35)
    bat_p['clutch_inns_count'] = bat_p['clutch_inns_count'].fillna(0)
    
    # Confidence multiplier based on sample size (min eligibility: 150 HP balls)
    bat_p['sample_confidence'] = np.minimum(1.0, np.sqrt(bat_p['hp_balls'] / 250.0))
    
    # Multi-dimensional Composite Batter Pressure Score (CBPS)
    # Z-scores across eligible pool
    elig_bat = bat_p[bat_p['hp_balls'] >= 150].copy()
    
    def z_score(series):
        return (series - series.mean()) / (series.std() + 1e-6)
    
    elig_bat['z_shrunk_sr'] = z_score(elig_bat['shrunk_hp_sr'])
    elig_bat['z_delta_sr'] = z_score(elig_bat['delta_sr'])
    elig_bat['z_dot_red'] = z_score(elig_bat['delta_dot_pct'])
    elig_bat['z_bnd'] = z_score(elig_bat['hp_bnd_pct'])
    elig_bat['z_cons'] = z_score(elig_bat['consistency_rate'])
    
    # Composite formula:
    # 30% Shrunk HP SR + 25% Delta SR + 20% Dot reduction + 15% Boundary % + 10% Consistency
    elig_bat['raw_cbps'] = (
        0.30 * elig_bat['z_shrunk_sr'] +
        0.25 * elig_bat['z_delta_sr'] +
        0.20 * elig_bat['z_dot_red'] +
        0.15 * elig_bat['z_bnd'] +
        0.10 * elig_bat['z_cons']
    )
    elig_bat['cbps'] = elig_bat['raw_cbps'] * elig_bat['sample_confidence']
    
    top_batters = elig_bat.sort_values(by='cbps', ascending=False).reset_index(drop=True)
    top_batters['rank'] = top_batters.index + 1
    
    print("\n--- TOP 10 BATTERS UNDER PRESSURE ---")
    print(top_batters[['rank', 'striker_name', 'hp_balls', 'raw_hp_sr', 'base_sr', 'delta_sr', 'raw_hp_dot_pct', 'hp_bnd_pct', 'consistency_rate', 'cbps']].head(15))
    
    # --- BOWLER ANALYSIS ---
    print("\nAnalyzing Bowlers...")
    bowl = bbb.groupby(['bowler_id', 'bowler_name', 'is_hp']).agg(
        balls=('is_legal', 'sum'),
        runs=('bowler_runs', 'sum'),
        dots=('bowler_runs', lambda s: (s == 0).sum()),
        wickets=('is_wicket', 'sum'),
        boundaries=('runs', lambda s: (s.isin([4, 6])).sum()),
        fours=('is_four', 'sum'),
        sixes=('is_six', 'sum')
    ).reset_index()
    
    bowl_p = bowl.pivot(index=['bowler_id', 'bowler_name'], columns='is_hp', values=['balls', 'runs', 'dots', 'wickets', 'boundaries', 'fours', 'sixes']).fillna(0)
    bowl_p.columns = [f'{col}_{is_hp}' for col, is_hp in bowl_p.columns]
    bowl_p = bowl_p.reset_index()
    
    bowl_p['hp_balls'] = bowl_p['balls_True']
    bowl_p['base_balls'] = bowl_p['balls_False']
    bowl_p['total_balls'] = bowl_p['hp_balls'] + bowl_p['base_balls']
    
    # Empirical Bayes Shrinkage for Bowlers
    prior_hp_econ = 9.20
    prior_hp_wkt = 7.0
    k_bowl = 50.0
    
    bowl_p['raw_hp_econ'] = (bowl_p['runs_True'] / np.maximum(1, bowl_p['hp_balls'])) * 6.0
    bowl_p['shrunk_hp_econ'] = (bowl_p['hp_balls'] / (bowl_p['hp_balls'] + k_bowl)) * bowl_p['raw_hp_econ'] + (k_bowl / (bowl_p['hp_balls'] + k_bowl)) * prior_hp_econ
    
    bowl_p['base_econ'] = (bowl_p['runs_False'] / np.maximum(1, bowl_p['base_balls'])) * 6.0
    bowl_p['delta_econ'] = bowl_p['base_econ'] - bowl_p['shrunk_hp_econ'] # positive = tighter in pressure than baseline
    
    bowl_p['raw_hp_dot_pct'] = (bowl_p['dots_True'] / np.maximum(1, bowl_p['hp_balls'])) * 100
    bowl_p['raw_hp_wkt_rate'] = (bowl_p['wickets_True'] / np.maximum(1, bowl_p['hp_balls'])) * 100
    bowl_p['shrunk_hp_wkt_rate'] = (bowl_p['hp_balls'] / (bowl_p['hp_balls'] + k_bowl)) * bowl_p['raw_hp_wkt_rate'] + (k_bowl / (bowl_p['hp_balls'] + k_bowl)) * prior_hp_wkt
    bowl_p['hp_bnd_conceded_pct'] = (bowl_p['boundaries_True'] / np.maximum(1, bowl_p['hp_balls'])) * 100
    
    # Match-level consistency for bowlers
    match_bowl = bbb[bbb['is_hp']].groupby(['match_id', 'bowler_id']).agg(
        hp_m_balls=('is_legal', 'sum'),
        hp_m_runs=('bowler_runs', 'sum'),
        hp_m_wkts=('is_wicket', 'sum')
    ).reset_index()
    match_bowl = match_bowl[match_bowl['hp_m_balls'] >= 8]
    match_bowl['m_econ'] = (match_bowl['hp_m_runs'] / match_bowl['hp_m_balls']) * 6.0
    # A clutch bowling spell under pressure: either econ <= 8.0 or taken >= 1 wicket
    match_bowl['is_clutch_spell'] = (match_bowl['m_econ'] <= 8.5) | (match_bowl['hp_m_wkts'] >= 1)
    
    consistency_bowl = match_bowl.groupby('bowler_id').agg(
        clutch_spells_count=('is_clutch_spell', 'sum'),
        total_hp_spells=('is_clutch_spell', 'count')
    ).reset_index()
    consistency_bowl['consistency_rate'] = consistency_bowl['clutch_spells_count'] / np.maximum(1, consistency_bowl['total_hp_spells'])
    
    bowl_p = bowl_p.merge(consistency_bowl, on='bowler_id', how='left')
    bowl_p['consistency_rate'] = bowl_p['consistency_rate'].fillna(0.40)
    
    # Confidence multiplier based on sample size (min eligibility: 150 HP balls)
    bowl_p['sample_confidence'] = np.minimum(1.0, np.sqrt(bowl_p['hp_balls'] / 250.0))
    
    elig_bowl = bowl_p[bowl_p['hp_balls'] >= 150].copy()
    
    elig_bowl['z_shrunk_econ'] = -z_score(elig_bowl['shrunk_hp_econ']) # negative because lower economy is better
    elig_bowl['z_delta_econ'] = z_score(elig_bowl['delta_econ'])
    elig_bowl['z_wkt_rate'] = z_score(elig_bowl['shrunk_hp_wkt_rate'])
    elig_bowl['z_dot_pct'] = z_score(elig_bowl['raw_hp_dot_pct'])
    elig_bowl['z_bnd_suppr'] = -z_score(elig_bowl['hp_bnd_conceded_pct']) # lower boundary conceded is better
    elig_bowl['z_cons'] = z_score(elig_bowl['consistency_rate'])
    
    # Composite formula for bowlers:
    # 30% Economy Suppression + 25% Wicket Threat + 15% Dot Pressure + 15% Boundary Prevention + 15% Consistency
    elig_bowl['raw_cbps'] = (
        0.30 * elig_bowl['z_shrunk_econ'] +
        0.25 * elig_bowl['z_wkt_rate'] +
        0.15 * elig_bowl['z_dot_pct'] +
        0.15 * elig_bowl['z_bnd_suppr'] +
        0.15 * elig_bowl['z_cons']
    )
    elig_bowl['cbps'] = elig_bowl['raw_cbps'] * elig_bowl['sample_confidence']
    
    top_bowlers = elig_bowl.sort_values(by='cbps', ascending=False).reset_index(drop=True)
    top_bowlers['rank'] = top_bowlers.index + 1
    
    print("\n--- TOP 10 BOWLERS UNDER PRESSURE ---")
    print(top_bowlers[['rank', 'bowler_name', 'hp_balls', 'raw_hp_econ', 'base_econ', 'raw_hp_wkt_rate', 'raw_hp_dot_pct', 'hp_bnd_conceded_pct', 'consistency_rate', 'cbps']].head(15))
    
    os.makedirs('output', exist_ok=True)
    top_batters.to_csv('output/top_batters_under_pressure.csv', index=False)
    top_bowlers.to_csv('output/top_bowlers_under_pressure.csv', index=False)
    print("\nSaved output/top_batters_under_pressure.csv and output/top_bowlers_under_pressure.csv successfully.")

if __name__ == '__main__':
    run_pipeline()

