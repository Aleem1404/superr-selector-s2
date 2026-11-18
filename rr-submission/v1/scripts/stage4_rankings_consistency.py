import pandas as pd
import numpy as np
import os

def run_stage4():
    print("=" * 60)
    print("STAGE 4: Match-Level Consistency Scoring & Final Composite Pressure Rankings (CBPS)")
    print("=" * 60)
    
    bbb_csv = 'rr-submission/stage1_ball_leverage/ball_by_ball_pressure.csv'
    bat_csv = 'rr-submission/stage3_bayesian_filtering/shrunken_batters.csv'
    bowl_csv = 'rr-submission/stage3_bayesian_filtering/shrunken_bowlers.csv'
    
    bbb = pd.read_csv(bbb_csv)
    df_bat = pd.read_csv(bat_csv)
    df_bowl = pd.read_csv(bowl_csv)
    
    # 1. Match-Level Batting Consistency
    print("\nCalculating match-level reliability for batters...")
    match_bat = bbb[bbb['is_hp']].groupby(['match_id', 'striker_id']).agg(
        hp_m_balls=('runs', 'count'),
        hp_m_runs=('runs', 'sum')
    ).reset_index()
    match_bat = match_bat[match_bat['hp_m_balls'] >= 8]
    match_bat['m_sr'] = (match_bat['hp_m_runs'] / match_bat['hp_m_balls']) * 100.0
    match_bat['is_clutch_inns'] = match_bat['m_sr'] >= 140.0
    
    cons_bat = match_bat.groupby('striker_id').agg(
        clutch_inns_count=('is_clutch_inns', 'sum'),
        total_hp_inns=('is_clutch_inns', 'count')
    ).reset_index()
    cons_bat['consistency_rate'] = (cons_bat['clutch_inns_count'] / np.maximum(1, cons_bat['total_hp_inns'])).round(3)
    
    df_bat = df_bat.merge(cons_bat[['striker_id', 'clutch_inns_count', 'total_hp_inns', 'consistency_rate']],
                          left_on='player_id', right_on='striker_id', how='left')
    df_bat['consistency_rate'] = df_bat['consistency_rate'].fillna(0.35)
    df_bat['clutch_inns_count'] = df_bat['clutch_inns_count'].fillna(0).astype(int)
    df_bat['total_hp_inns'] = df_bat['total_hp_inns'].fillna(0).astype(int)
    
    # 2. Match-Level Bowling Consistency
    print("Calculating match-level reliability for bowlers...")
    match_bowl = bbb[bbb['is_hp']].groupby(['match_id', 'bowler_id']).agg(
        hp_m_balls=('is_legal', 'sum'),
        hp_m_runs=('bowler_runs', 'sum'),
        hp_m_wkts=('is_wicket', 'sum')
    ).reset_index()
    match_bowl = match_bowl[match_bowl['hp_m_balls'] >= 8]
    match_bowl['m_econ'] = (match_bowl['hp_m_runs'] / match_bowl['hp_m_balls']) * 6.0
    match_bowl['is_clutch_spell'] = (match_bowl['m_econ'] <= 8.5) | (match_bowl['hp_m_wkts'] >= 1)
    
    cons_bowl = match_bowl.groupby('bowler_id').agg(
        clutch_spells_count=('is_clutch_spell', 'sum'),
        total_hp_spells=('is_clutch_spell', 'count')
    ).reset_index()
    cons_bowl['consistency_rate'] = (cons_bowl['clutch_spells_count'] / np.maximum(1, cons_bowl['total_hp_spells'])).round(3)
    
    df_bowl = df_bowl.merge(cons_bowl[['bowler_id', 'clutch_spells_count', 'total_hp_spells', 'consistency_rate']],
                            left_on='player_id', right_on='bowler_id', how='left')
    df_bowl['consistency_rate'] = df_bowl['consistency_rate'].fillna(0.40)
    df_bowl['clutch_spells_count'] = df_bowl['clutch_spells_count'].fillna(0).astype(int)
    df_bowl['total_hp_spells'] = df_bowl['total_hp_spells'].fillna(0).astype(int)
    
    # 3. Z-Score Normalization and Composite Pressure Scoring (CBPS)
    def z_score(series):
        return (series - series.mean()) / (series.std() + 1e-6)
    
    # Batters Scoring (Eligible Pool >= 150 HP balls)
    elig_bat = df_bat[df_bat['is_eligible']].copy()
    elig_bat['z_shrunk_sr'] = z_score(elig_bat['shrunk_hp_sr'])
    elig_bat['z_delta_sr'] = z_score(elig_bat['shrunk_delta_sr'])
    elig_bat['z_dot_red'] = z_score(elig_bat['shrunk_delta_dot_pct'])
    elig_bat['z_bnd'] = z_score(elig_bat['hp_boundary_pct'])
    elig_bat['z_cons'] = z_score(elig_bat['consistency_rate'])
    
    elig_bat['raw_cbps'] = (
        0.30 * elig_bat['z_shrunk_sr'] +
        0.25 * elig_bat['z_delta_sr'] +
        0.20 * elig_bat['z_dot_red'] +
        0.15 * elig_bat['z_bnd'] +
        0.10 * elig_bat['z_cons']
    )
    elig_bat['cbps_score'] = (elig_bat['raw_cbps'] * elig_bat['sample_confidence']).round(2)
    ranked_batters = elig_bat.sort_values(by='cbps_score', ascending=False).reset_index(drop=True)
    ranked_batters['pressure_rank'] = ranked_batters.index + 1
    
    # Bowlers Scoring (Eligible Pool >= 150 HP balls)
    elig_bowl = df_bowl[df_bowl['is_eligible']].copy()
    elig_bowl['z_shrunk_econ'] = -z_score(elig_bowl['shrunk_hp_econ']) # Negative because lower econ is superior
    elig_bowl['z_wkt_rate'] = z_score(elig_bowl['shrunk_hp_wkt_rate'])
    elig_bowl['z_dot_pct'] = z_score(elig_bowl['hp_dot_pct'])
    elig_bowl['z_bnd_suppr'] = -z_score(elig_bowl['hp_bnd_conceded_pct']) # Lower boundary conceded is superior
    elig_bowl['z_cons'] = z_score(elig_bowl['consistency_rate'])
    
    elig_bowl['raw_cbps'] = (
        0.30 * elig_bowl['z_shrunk_econ'] +
        0.25 * elig_bowl['z_wkt_rate'] +
        0.15 * elig_bowl['z_dot_pct'] +
        0.15 * elig_bowl['z_bnd_suppr'] +
        0.15 * elig_bowl['z_cons']
    )
    elig_bowl['cbps_score'] = (elig_bowl['raw_cbps'] * elig_bowl['sample_confidence']).round(2)
    ranked_bowlers = elig_bowl.sort_values(by='cbps_score', ascending=False).reset_index(drop=True)
    ranked_bowlers['pressure_rank'] = ranked_bowlers.index + 1
    
    # 4. Save Master and Top 10 Files
    out_dir = 'rr-submission/stage4_consistency_scoring'
    
    # Master ranked lists
    ranked_batters.to_csv(os.path.join(out_dir, 'ranked_batters_master.csv'), index=False)
    ranked_bowlers.to_csv(os.path.join(out_dir, 'ranked_bowlers_master.csv'), index=False)
    
    # Top 10 lists
    top10_bat = ranked_batters.head(10).copy()
    top10_bowl = ranked_bowlers.head(10).copy()
    
    top10_bat.to_csv(os.path.join(out_dir, 'top10_batters_final.csv'), index=False)
    top10_bowl.to_csv(os.path.join(out_dir, 'top10_bowlers_final.csv'), index=False)
    
    # Also save in root of rr-submission for instant reviewer convenience
    top10_bat.to_csv('rr-submission/top10_batters_final.csv', index=False)
    top10_bowl.to_csv('rr-submission/top10_bowlers_final.csv', index=False)
    
    print("\n" + "=" * 60)
    print("TOP 10 BATTERS UNDER PRESSURE (FINAL OFFICIAL SELECTIONS)")
    print("=" * 60)
    print(top10_bat[['pressure_rank', 'player_name', 'hp_balls', 'hp_sr', 'base_sr', 'delta_sr', 'hp_dot_pct', 'consistency_rate', 'cbps_score']].to_string(index=False))
    
    print("\n" + "=" * 60)
    print("TOP 10 BOWLERS UNDER PRESSURE (FINAL OFFICIAL SELECTIONS)")
    print("=" * 60)
    print(top10_bowl[['pressure_rank', 'player_name', 'hp_balls', 'hp_econ', 'base_econ', 'delta_econ', 'hp_wkt_rate', 'consistency_rate', 'cbps_score']].to_string(index=False))
    print("\nSTAGE 4 COMPLETE.")

if __name__ == '__main__':
    run_stage4()

