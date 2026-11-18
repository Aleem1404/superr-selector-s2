import pandas as pd
import numpy as np
import os
import json

def run_stage4_v4():
    print("=" * 70)
    print("STAGE 4 (v4): Match Reliability & Context-Calibrated Rankings (CBPS v4)")
    print("  - Active Roster Filter (Option 3 & Option 4: Cricinfo & Official Statements)")
    print("  - Excludes: MS Dhoni (CSK Mentor), Dinesh Karthik (RCB Mentor), Matthew Wade (Aus Coach)")
    print("  - Includes: All active retained & contracted stars")
    print("=" * 70)
    
    bbb_csv = 'rr-submission/v4/stage1_ball_leverage/ball_by_ball_pressure_v4.csv'
    bat_csv = 'rr-submission/v4/stage3_bayesian_filtering/shrunken_batters_v4.csv'
    bowl_csv = 'rr-submission/v4/stage3_bayesian_filtering/shrunken_bowlers_v4.csv'
    
    bbb = pd.read_csv(bbb_csv)
    df_bat = pd.read_csv(bat_csv)
    df_bowl = pd.read_csv(bowl_csv)
    
    # 1. Match-Level Batting Consistency
    print("\n[1/4] Calculating match-level reliability for batters...")
    match_bat = bbb[bbb['is_hp_v4']].groupby(['match_id', 'striker_id']).agg(
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
    
    # 2. Match-Level Bowling Consistency
    print("[2/4] Calculating match-level reliability for bowlers...")
    match_bowl = bbb[bbb['is_hp_v4']].groupby(['match_id', 'bowler_id']).agg(
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
    
    # 3. Z-Score Normalization and Composite Pressure Scoring (CBPS v4)
    def z_score(series):
        return (series - series.mean()) / (series.std() + 1e-6)
    
    # Batters Scoring
    elig_bat = df_bat[df_bat['is_eligible']].copy()
    elig_bat['z_shrunk_sr'] = z_score(elig_bat['shrunk_hp_sr'])
    elig_bat['z_delta_venue'] = z_score(elig_bat['shrunk_delta_venue'])
    elig_bat['z_delta_baseline'] = z_score(elig_bat['shrunk_delta_baseline'])
    elig_bat['z_dot_red'] = z_score(elig_bat['shrunk_delta_dot_pct'])
    elig_bat['z_cons'] = z_score(elig_bat['consistency_rate'])
    
    elig_bat['raw_cbps_v4'] = (
        0.25 * elig_bat['z_shrunk_sr'] +
        0.25 * elig_bat['z_delta_venue'] +
        0.20 * elig_bat['z_delta_baseline'] +
        0.15 * elig_bat['z_dot_red'] +
        0.15 * elig_bat['z_cons']
    )
    elig_bat['cbps_score_v4'] = (elig_bat['raw_cbps_v4'] * elig_bat['sample_confidence']).round(2)
    ranked_batters = elig_bat.sort_values(by='cbps_score_v4', ascending=False).reset_index(drop=True)
    ranked_batters['overall_rank'] = ranked_batters.index + 1
    
    # Bowlers Scoring
    elig_bowl = df_bowl[df_bowl['is_eligible']].copy()
    elig_bowl['z_shrunk_econ'] = -z_score(elig_bowl['shrunk_hp_econ'])
    elig_bowl['z_delta_venue_econ'] = z_score(elig_bowl['shrunk_delta_venue_econ'])
    elig_bowl['z_wkt_rate'] = z_score(elig_bowl['shrunk_hp_wkt_rate'])
    elig_bowl['z_dot_pct'] = z_score(elig_bowl['hp_dot_pct'])
    elig_bowl['z_cons'] = z_score(elig_bowl['consistency_rate'])
    
    elig_bowl['raw_cbps_v4'] = (
        0.25 * elig_bowl['z_shrunk_econ'] +
        0.25 * elig_bowl['z_delta_venue_econ'] +
        0.20 * elig_bowl['z_wkt_rate'] +
        0.15 * elig_bowl['z_dot_pct'] +
        0.15 * elig_bowl['z_cons']
    )
    elig_bowl['cbps_score_v4'] = (elig_bowl['raw_cbps_v4'] * elig_bowl['sample_confidence']).round(2)
    ranked_bowlers = elig_bowl.sort_values(by='cbps_score_v4', ascending=False).reset_index(drop=True)
    ranked_bowlers['overall_rank'] = ranked_bowlers.index + 1
    
    # 4. ACTIVE ROSTER FILTER (Option 3 & Option 4)
    print("\n[3/4] Applying Verified Active Roster Exclusion Module...")
    confirmed_retired_players = {
        'Mahendra Singh Dhoni': 'Retired & transitioned to CSK Mentor',
        'Dinesh Karthik': 'Retired 1 June 2024 (RCB Batting Coach)',
        'Matthew Wade': 'Retired Oct 2024 (Australia Coaching Staff)',
        'Andre Russell': 'Retired from IPL / Representative Cricket',
        'Ambati Rayudu': 'Retired May 2023',
        'Kieron Pollard': 'Retired Nov 2022 (MI Batting Coach)',
        'Robin Uthappa': 'Retired Sept 2022',
        'Suresh Raina': 'Retired Sept 2022',
        'Murali Vijay': 'Retired Jan 2023',
        'Aaron Finch': 'Retired Feb 2023',
        'Eoin Morgan': 'Retired Feb 2023',
        'Shikhar Dhawan': 'Retired Aug 2024',
        'Dwayne Bravo': 'Retired Sept 2024 (KKR Mentor)',
        'David Wiese': 'Retired June 2024',
        'Varun Aaron': 'Retired Feb 2024',
        'Saurabh Tiwary': 'Retired Feb 2024'
    }
    
    mapping = pd.read_csv('data/competition_team_player_mapping.csv')
    pak_players = set(mapping[mapping['team_name'].str.contains('Pakistan', na=False)]['player_name'].unique())
    
    ranked_batters['is_retired'] = ranked_batters['player_name'].isin(confirmed_retired_players.keys())
    ranked_batters['retirement_note'] = ranked_batters['player_name'].map(confirmed_retired_players).fillna('Active')
    ranked_batters['is_pakistani'] = ranked_batters['player_name'].isin(pak_players)
    
    ranked_bowlers['is_retired'] = ranked_bowlers['player_name'].isin(confirmed_retired_players.keys())
    ranked_bowlers['retirement_note'] = ranked_bowlers['player_name'].map(confirmed_retired_players).fillna('Active')
    ranked_bowlers['is_pakistani'] = ranked_bowlers['player_name'].isin(pak_players)
    
    active_batters = ranked_batters[
        (ranked_batters['hp_balls'] >= 200) & 
        (~ranked_batters['is_retired']) & 
        (~ranked_batters['is_pakistani'])
    ].copy().reset_index(drop=True)
    active_batters['pressure_rank_v4'] = active_batters.index + 1
    
    active_bowlers = ranked_bowlers[
        (ranked_bowlers['hp_balls'] >= 200) & 
        (~ranked_bowlers['is_retired']) & 
        (~ranked_bowlers['is_pakistani'])
    ].copy().reset_index(drop=True)
    active_bowlers['pressure_rank_v4'] = active_bowlers.index + 1
    
    top10_bat_v4 = active_batters.head(10).copy()
    top10_bat_v4['rank'] = range(1, 11)
    
    top10_bowl_v4 = active_bowlers.head(10).copy()
    top10_bowl_v4['rank'] = range(1, 11)
    
    # 5. Save Artifacts
    print("[4/4] Saving v4 Master Datasets and Deliverables...")
    stage4_dir = 'rr-submission/v4/stage4_consistency_scoring'
    deliverables_dir = 'rr-submission/v4/stage5_deliverables'
    
    ranked_batters.to_csv(os.path.join(stage4_dir, 'ranked_batters_v4_master.csv'), index=False)
    ranked_bowlers.to_csv(os.path.join(stage4_dir, 'ranked_bowlers_v4_master.csv'), index=False)
    
    active_batters.to_csv(os.path.join(stage4_dir, 'active_batters_v4_master.csv'), index=False)
    active_bowlers.to_csv(os.path.join(stage4_dir, 'active_bowlers_v4_master.csv'), index=False)
    
    top10_bat_v4.to_csv(os.path.join(stage4_dir, 'top10_batters_v4_final.csv'), index=False)
    top10_bowl_v4.to_csv(os.path.join(stage4_dir, 'top10_bowlers_v4_final.csv'), index=False)
    
    top10_bat_v4.to_csv(os.path.join(deliverables_dir, 'top10_batters_v4.csv'), index=False)
    top10_bowl_v4.to_csv(os.path.join(deliverables_dir, 'top10_bowlers_v4.csv'), index=False)
    
    top10_bat_v4.to_csv('rr-submission/v4/top10_batters_final.csv', index=False)
    top10_bowl_v4.to_csv('rr-submission/v4/top10_bowlers_final.csv', index=False)
    
    print("\n" + "=" * 75)
    print("TOP 10 ACTIVE BATTERS UNDER PRESSURE (v4 - UNIFIED CONTEXTUAL MODEL)")
    print("=" * 75)
    cols_bat = ['rank', 'player_name', 'hp_balls', 'hp_sr', 'hp_opp_sr', 'delta_sr_venue', 'delta_sr_baseline', 'consistency_rate', 'cbps_score_v4']
    print(top10_bat_v4[cols_bat].to_string(index=False))
    
    print("\n" + "=" * 75)
    print("TOP 10 ACTIVE BOWLERS UNDER PRESSURE (v4 - UNIFIED CONTEXTUAL MODEL)")
    print("=" * 75)
    cols_bowl = ['rank', 'player_name', 'hp_balls', 'hp_econ', 'delta_econ_venue', 'delta_econ_baseline', 'hp_wkt_rate', 'consistency_rate', 'cbps_score_v4']
    print(top10_bowl_v4[cols_bowl].to_string(index=False))
    
    summary = {
        'version': 'v4',
        'framework': 'Unified Contextual Pressure Engine (Opposition Tiering + Chase Asymmetry + Tactical Cohort + Venue Par)',
        'top10_batters': top10_bat_v4[['rank', 'player_name', 'cbps_score_v4', 'hp_sr', 'hp_opp_sr', 'delta_sr_venue']].to_dict(orient='records'),
        'top10_bowlers': top10_bowl_v4[['rank', 'player_name', 'cbps_score_v4', 'hp_econ', 'delta_econ_venue']].to_dict(orient='records')
    }
    with open('rr-submission/v4/v4_pipeline_summary.json', 'w') as f:
        json.dump(summary, f, indent=2)
    print("\nSaved v4_pipeline_summary.json successfully.")

if __name__ == '__main__':
    run_stage4_v4()

