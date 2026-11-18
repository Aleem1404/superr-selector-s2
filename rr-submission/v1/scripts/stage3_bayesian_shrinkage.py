import pandas as pd
import numpy as np
import os

def run_stage3():
    print("=" * 60)
    print("STAGE 3: Empirical Bayes Shrinkage & Sample Normalization")
    print("=" * 60)
    
    bat_csv = 'rr-submission/stage2_player_aggregates/raw_batting_aggregates.csv'
    bowl_csv = 'rr-submission/stage2_player_aggregates/raw_bowling_aggregates.csv'
    
    df_bat = pd.read_csv(bat_csv)
    df_bowl = pd.read_csv(bowl_csv)
    
    # --- 1. BAYESIAN SHRINKAGE FOR BATTERS ---
    # Priors derived from league-wide high-pressure distribution
    prior_hp_sr = 135.0
    prior_hp_dot = 36.0
    k_bat = 50.0 # Prior pseudo-ball weighting
    
    df_bat['is_eligible'] = df_bat['hp_balls'] >= 150
    df_bat['sample_confidence'] = np.minimum(1.0, np.sqrt(df_bat['hp_balls'] / 250.0)).round(3)
    
    # Shrunken HP Strike Rate
    df_bat['shrunk_hp_sr'] = (
        (df_bat['hp_balls'] / (df_bat['hp_balls'] + k_bat)) * df_bat['hp_sr'] +
        (k_bat / (df_bat['hp_balls'] + k_bat)) * prior_hp_sr
    ).round(2)
    
    # Shrunken HP Dot Ball %
    df_bat['shrunk_hp_dot_pct'] = (
        (df_bat['hp_balls'] / (df_bat['hp_balls'] + k_bat)) * df_bat['hp_dot_pct'] +
        (k_bat / (df_bat['hp_balls'] + k_bat)) * prior_hp_dot
    ).round(2)
    
    # Re-calculate differential metrics using stabilized Bayesian estimates
    df_bat['shrunk_delta_sr'] = (df_bat['shrunk_hp_sr'] - df_bat['base_sr']).round(2)
    df_bat['shrunk_delta_dot_pct'] = (df_bat['base_dot_pct'] - df_bat['shrunk_hp_dot_pct']).round(2)
    
    out_bat = 'rr-submission/stage3_bayesian_filtering/shrunken_batters.csv'
    df_bat.to_csv(out_bat, index=False)
    print(f"Saved {len(df_bat):,} stabilized batter records ({df_bat['is_eligible'].sum()} eligible) to: {out_bat}")
    
    # --- 2. BAYESIAN SHRINKAGE FOR BOWLERS ---
    prior_hp_econ = 9.20
    prior_hp_wkt = 7.0
    k_bowl = 50.0
    
    df_bowl['is_eligible'] = df_bowl['hp_balls'] >= 150
    df_bowl['sample_confidence'] = np.minimum(1.0, np.sqrt(df_bowl['hp_balls'] / 250.0)).round(3)
    
    # Shrunken HP Economy
    df_bowl['shrunk_hp_econ'] = (
        (df_bowl['hp_balls'] / (df_bowl['hp_balls'] + k_bowl)) * df_bowl['hp_econ'] +
        (k_bowl / (df_bowl['hp_balls'] + k_bowl)) * prior_hp_econ
    ).round(2)
    
    # Shrunken HP Wicket Rate %
    df_bowl['shrunk_hp_wkt_rate'] = (
        (df_bowl['hp_balls'] / (df_bowl['hp_balls'] + k_bowl)) * df_bowl['hp_wkt_rate'] +
        (k_bowl / (df_bowl['hp_balls'] + k_bowl)) * prior_hp_wkt
    ).round(2)
    
    # Differentials
    df_bowl['shrunk_delta_econ'] = (df_bowl['base_econ'] - df_bowl['shrunk_hp_econ']).round(2)
    
    out_bowl = 'rr-submission/stage3_bayesian_filtering/shrunken_bowlers.csv'
    df_bowl.to_csv(out_bowl, index=False)
    print(f"Saved {len(df_bowl):,} stabilized bowler records ({df_bowl['is_eligible'].sum()} eligible) to: {out_bowl}")
    print("\nSTAGE 3 COMPLETE.")

if __name__ == '__main__':
    run_stage3()

