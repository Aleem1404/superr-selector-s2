import pandas as pd
import numpy as np
import os

def run_stage3_v2():
    print("=" * 60)
    print("STAGE 3 (v2): Empirical Bayes Shrinkage on Venue-Adjusted Differentials")
    print("=" * 60)
    
    bat_csv = 'rr-submission/v2/stage2_player_aggregates/raw_batting_aggregates_v2.csv'
    bowl_csv = 'rr-submission/v2/stage2_player_aggregates/raw_bowling_aggregates_v2.csv'
    
    df_bat = pd.read_csv(bat_csv)
    df_bowl = pd.read_csv(bowl_csv)
    
    # 1. Batters Bayesian Shrinkage
    prior_hp_sr = 135.0
    prior_hp_dot = 36.0
    prior_delta_venue = 0.0
    k_bat = 50.0
    
    df_bat['is_eligible'] = df_bat['hp_balls'] >= 150
    df_bat['sample_confidence'] = np.minimum(1.0, np.sqrt(df_bat['hp_balls'] / 250.0)).round(3)
    
    # Shrunken metrics
    df_bat['shrunk_hp_sr'] = (
        (df_bat['hp_balls'] / (df_bat['hp_balls'] + k_bat)) * df_bat['hp_sr'] +
        (k_bat / (df_bat['hp_balls'] + k_bat)) * prior_hp_sr
    ).round(2)
    
    df_bat['shrunk_hp_dot_pct'] = (
        (df_bat['hp_balls'] / (df_bat['hp_balls'] + k_bat)) * df_bat['hp_dot_pct'] +
        (k_bat / (df_bat['hp_balls'] + k_bat)) * prior_hp_dot
    ).round(2)
    
    df_bat['shrunk_delta_venue'] = (
        (df_bat['hp_balls'] / (df_bat['hp_balls'] + k_bat)) * df_bat['delta_sr_venue'] +
        (k_bat / (df_bat['hp_balls'] + k_bat)) * prior_delta_venue
    ).round(2)
    
    df_bat['shrunk_delta_baseline'] = (df_bat['shrunk_hp_sr'] - df_bat['base_sr']).round(2)
    df_bat['shrunk_delta_dot_pct'] = (df_bat['base_dot_pct'] - df_bat['shrunk_hp_dot_pct']).round(2)
    
    out_bat = 'rr-submission/v2/stage3_bayesian_filtering/shrunken_batters_v2.csv'
    df_bat.to_csv(out_bat, index=False)
    print(f"Saved {len(df_bat):,} stabilized batter records ({df_bat['is_eligible'].sum()} eligible) to: {out_bat}")
    
    # 2. Bowlers Bayesian Shrinkage
    prior_hp_econ = 9.20
    prior_hp_wkt = 7.0
    prior_delta_econ_venue = 0.0
    k_bowl = 50.0
    
    df_bowl['is_eligible'] = df_bowl['hp_balls'] >= 150
    df_bowl['sample_confidence'] = np.minimum(1.0, np.sqrt(df_bowl['hp_balls'] / 250.0)).round(3)
    
    df_bowl['shrunk_hp_econ'] = (
        (df_bowl['hp_balls'] / (df_bowl['hp_balls'] + k_bowl)) * df_bowl['hp_econ'] +
        (k_bowl / (df_bowl['hp_balls'] + k_bowl)) * prior_hp_econ
    ).round(2)
    
    df_bowl['shrunk_hp_wkt_rate'] = (
        (df_bowl['hp_balls'] / (df_bowl['hp_balls'] + k_bowl)) * df_bowl['hp_wkt_rate'] +
        (k_bowl / (df_bowl['hp_balls'] + k_bowl)) * prior_hp_wkt
    ).round(2)
    
    df_bowl['shrunk_delta_venue_econ'] = (
        (df_bowl['hp_balls'] / (df_bowl['hp_balls'] + k_bowl)) * df_bowl['delta_econ_venue'] +
        (k_bowl / (df_bowl['hp_balls'] + k_bowl)) * prior_delta_econ_venue
    ).round(2)
    
    df_bowl['shrunk_delta_baseline_econ'] = (df_bowl['base_econ'] - df_bowl['shrunk_hp_econ']).round(2)
    
    out_bowl = 'rr-submission/v2/stage3_bayesian_filtering/shrunken_bowlers_v2.csv'
    df_bowl.to_csv(out_bowl, index=False)
    print(f"Saved {len(df_bowl):,} stabilized bowler records ({df_bowl['is_eligible'].sum()} eligible) to: {out_bowl}")
    print("\nSTAGE 3 (v2) COMPLETE.")

if __name__ == '__main__':
    run_stage3_v2()

