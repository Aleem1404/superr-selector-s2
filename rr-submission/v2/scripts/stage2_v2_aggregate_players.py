import pandas as pd
import numpy as np
import os

def run_stage2_v2():
    print("=" * 60)
    print("STAGE 2 (v2): Aggregating Venue-Adjusted Player Performance")
    print("=" * 60)
    
    in_csv = 'rr-submission/v2/stage1_ball_leverage/ball_by_ball_pressure_v2.csv'
    bbb = pd.read_csv(in_csv)
    print(f"Loaded {len(bbb):,} deliveries from Stage 1 (v2).")
    
    # --- A. BATTING AGGREGATION ---
    print("\nAggregating batting metrics with venue baseline adjustments...")
    
    # 1. Standard Base vs HP Aggregation
    bat = bbb.groupby(['striker_id', 'striker_name', 'is_hp_v2']).agg(
        balls=('runs', 'count'),
        runs=('runs', 'sum'),
        dots=('runs', lambda s: (s == 0).sum()),
        boundaries=('runs', lambda s: (s.isin([4, 6])).sum()),
        fours=('is_four', 'sum'),
        sixes=('is_six', 'sum'),
        outs=('is_wicket', 'sum'),
        ipl_balls=('is_ipl', 'sum'),
        expected_runs=('venue_par_rpo', lambda s: (s / 6.0).sum())
    ).reset_index()
    
    bat_p = bat.pivot(
        index=['striker_id', 'striker_name'],
        columns='is_hp_v2',
        values=['balls', 'runs', 'dots', 'boundaries', 'fours', 'sixes', 'outs', 'ipl_balls', 'expected_runs']
    ).fillna(0)
    bat_p.columns = [f'{col}_{is_hp}' for col, is_hp in bat_p.columns]
    bat_p = bat_p.reset_index()
    
    bat_df = pd.DataFrame()
    bat_df['player_id'] = bat_p['striker_id']
    bat_df['player_name'] = bat_p['striker_name']
    
    # Baseline Metrics
    bat_df['base_balls'] = bat_p['balls_False'].astype(int)
    bat_df['base_runs'] = bat_p['runs_False'].astype(int)
    bat_df['base_sr'] = np.where(bat_df['base_balls'] > 0, (bat_df['base_runs'] / bat_df['base_balls']) * 100.0, 0.0).round(2)
    bat_df['base_dot_pct'] = np.where(bat_df['base_balls'] > 0, (bat_p['dots_False'] / bat_df['base_balls']) * 100.0, 0.0).round(2)
    
    # High-Pressure Metrics (v2)
    bat_df['hp_balls'] = bat_p['balls_True'].astype(int)
    bat_df['hp_ipl_balls'] = bat_p['ipl_balls_True'].astype(int)
    bat_df['hp_runs'] = bat_p['runs_True'].astype(int)
    bat_df['hp_outs'] = bat_p['outs_True'].astype(int)
    bat_df['hp_boundaries'] = bat_p['boundaries_True'].astype(int)
    bat_df['hp_sr'] = np.where(bat_df['hp_balls'] > 0, (bat_df['hp_runs'] / bat_df['hp_balls']) * 100.0, 0.0).round(2)
    bat_df['hp_dot_pct'] = np.where(bat_df['hp_balls'] > 0, (bat_p['dots_True'] / bat_df['hp_balls']) * 100.0, 0.0).round(2)
    bat_df['hp_bnd_pct'] = np.where(bat_df['hp_balls'] > 0, (bat_df['hp_boundaries'] / bat_df['hp_balls']) * 100.0, 0.0).round(2)
    
    # Venue Expected Run Rate & Venue Delta SR
    bat_df['hp_exp_runs'] = bat_p['expected_runs_True'].round(1)
    bat_df['hp_exp_sr'] = np.where(bat_df['hp_balls'] > 0, (bat_df['hp_exp_runs'] / bat_df['hp_balls']) * 100.0, 145.0).round(2)
    bat_df['delta_sr_venue'] = (bat_df['hp_sr'] - bat_df['hp_exp_sr']).round(2)
    bat_df['delta_sr_baseline'] = (bat_df['hp_sr'] - bat_df['base_sr']).round(2)
    bat_df['delta_dot_pct'] = (bat_df['base_dot_pct'] - bat_df['hp_dot_pct']).round(2)
    
    out_bat = 'rr-submission/v2/stage2_player_aggregates/raw_batting_aggregates_v2.csv'
    bat_df.to_csv(out_bat, index=False)
    print(f"Saved {len(bat_df):,} batting records to: {out_bat}")
    
    # --- B. BOWLING AGGREGATION ---
    print("\nAggregating bowling metrics with venue baseline adjustments...")
    bowl = bbb.groupby(['bowler_id', 'bowler_name', 'is_hp_v2']).agg(
        balls=('is_legal', 'sum'),
        runs=('bowler_runs', 'sum'),
        dots=('bowler_runs', lambda s: (s == 0).sum()),
        wickets=('is_wicket', 'sum'),
        boundaries=('runs', lambda s: (s.isin([4, 6])).sum()),
        ipl_balls=('is_ipl', 'sum'),
        expected_runs=('venue_par_rpo', lambda s: (s / 6.0).sum())
    ).reset_index()
    
    bowl_p = bowl.pivot(
        index=['bowler_id', 'bowler_name'],
        columns='is_hp_v2',
        values=['balls', 'runs', 'dots', 'wickets', 'boundaries', 'ipl_balls', 'expected_runs']
    ).fillna(0)
    bowl_p.columns = [f'{col}_{is_hp}' for col, is_hp in bowl_p.columns]
    bowl_p = bowl_p.reset_index()
    
    bowl_df = pd.DataFrame()
    bowl_df['player_id'] = bowl_p['bowler_id']
    bowl_df['player_name'] = bowl_p['bowler_name']
    
    # Baseline
    bowl_df['base_balls'] = bowl_p['balls_False'].astype(int)
    bowl_df['base_runs'] = bowl_p['runs_False'].astype(int)
    bowl_df['base_econ'] = np.where(bowl_df['base_balls'] > 0, (bowl_df['base_runs'] / bowl_df['base_balls']) * 6.0, 0.0).round(2)
    bowl_df['base_dot_pct'] = np.where(bowl_df['base_balls'] > 0, (bowl_p['dots_False'] / bowl_df['base_balls']) * 100.0, 0.0).round(2)
    
    # High-Pressure
    bowl_df['hp_balls'] = bowl_p['balls_True'].astype(int)
    bowl_df['hp_ipl_balls'] = bowl_p['ipl_balls_True'].astype(int)
    bowl_df['hp_runs'] = bowl_p['runs_True'].astype(int)
    bowl_df['hp_wickets'] = bowl_p['wickets_True'].astype(int)
    bowl_df['hp_econ'] = np.where(bowl_df['hp_balls'] > 0, (bowl_df['hp_runs'] / bowl_df['hp_balls']) * 6.0, 0.0).round(2)
    bowl_df['hp_dot_pct'] = np.where(bowl_df['hp_balls'] > 0, (bowl_p['dots_True'] / bowl_df['hp_balls']) * 100.0, 0.0).round(2)
    bowl_df['hp_wkt_rate'] = np.where(bowl_df['hp_balls'] > 0, (bowl_df['hp_wickets'] / bowl_df['hp_balls']) * 100.0, 0.0).round(2)
    bowl_df['hp_bnd_conceded_pct'] = np.where(bowl_df['hp_balls'] > 0, (bowl_p['boundaries_True'] / bowl_df['hp_balls']) * 100.0, 0.0).round(2)
    
    # Venue Adjusted Economy
    bowl_df['hp_exp_runs'] = bowl_p['expected_runs_True'].round(1)
    bowl_df['hp_venue_par_econ'] = np.where(bowl_df['hp_balls'] > 0, (bowl_df['hp_exp_runs'] / bowl_df['hp_balls']) * 6.0, 8.85).round(2)
    bowl_df['delta_econ_venue'] = (bowl_df['hp_venue_par_econ'] - bowl_df['hp_econ']).round(2) # Positive = suppressed runs below venue par
    bowl_df['delta_econ_baseline'] = (bowl_df['base_econ'] - bowl_df['hp_econ']).round(2)
    
    out_bowl = 'rr-submission/v2/stage2_player_aggregates/raw_bowling_aggregates_v2.csv'
    bowl_df.to_csv(out_bowl, index=False)
    print(f"Saved {len(bowl_df):,} bowling records to: {out_bowl}")
    print("\nSTAGE 2 (v2) COMPLETE.")

if __name__ == '__main__':
    run_stage2_v2()

