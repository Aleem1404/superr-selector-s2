import pandas as pd
import numpy as np
import os

def enrich_v4():
    print("=" * 70)
    print("ENRICHING MODEL v4: Adding Dual Toggles (Auction Targets & RR Home Ground)")
    print("=" * 70)
    
    bbb = pd.read_csv('rr-submission/v4/stage1_ball_leverage/ball_by_ball_pressure_v4.csv')
    bat_csv = 'rr-submission/v4/stage4_consistency_scoring/active_batters_v4_master.csv'
    bowl_csv = 'rr-submission/v4/stage4_consistency_scoring/active_bowlers_v4_master.csv'
    ret_csv = 'IPL-2027-retentions.csv'
    
    df_bat = pd.read_csv(bat_csv)
    df_bowl = pd.read_csv(bowl_csv)
    ret = pd.read_csv(ret_csv) if os.path.exists(ret_csv) else pd.DataFrame()
    
    # 1. Retention & Team Mapping
    retained_map = {
        'nitish reddy': 'SRH',
        'nitish kumar reddy': 'SRH',
        'kaki nitish kumar reddy': 'SRH',
    }
    if not ret.empty:
        for _, row in ret.iterrows():
            code = str(row['team_code'])
            pname = str(row['player_name']).lower().strip()
            retained_map[pname] = code
            if pd.notna(row['full_name']):
                retained_map[str(row['full_name']).lower().strip()] = code
                
    def get_team_status(name):
        n = str(name).lower().strip()
        if n in retained_map:
            return f"{retained_map[n]} (Retained)"
        for k, team in retained_map.items():
            if k == n or (len(k) > 5 and k in n) or (len(n) > 5 and n in k):
                return f"{team} (Retained)"
        return "Available in Auction"
        
    df_bat['team_status'] = df_bat['player_name'].apply(get_team_status)
    df_bat['is_auction_target'] = df_bat['team_status'] == "Available in Auction"
    
    df_bowl['team_status'] = df_bowl['player_name'].apply(get_team_status)
    df_bowl['is_auction_target'] = df_bowl['team_status'] == "Available in Auction"
    
    # 2. RR Home Grounds Stats (Sawai Mansingh Stadium, Jaipur & Barsapara Stadium, Guwahati)
    bbb['is_rr_home'] = bbb['venue'].isin(['Sawai Mansingh Stadium, Jaipur', 'Barsapara Cricket Stadium, Guwahati'])
    
    # Batters at RR Home
    rr_bat = bbb[bbb['is_rr_home']].groupby('striker_id').agg(
        rr_home_balls=('runs', 'count'),
        rr_home_runs=('runs', 'sum')
    ).reset_index()
    rr_bat['rr_home_sr'] = ((rr_bat['rr_home_runs'] / np.maximum(1, rr_bat['rr_home_balls'])) * 100.0).round(1)
    
    df_bat = df_bat.merge(rr_bat, left_on='player_id', right_on='striker_id', how='left')
    df_bat['rr_home_balls'] = df_bat['rr_home_balls'].fillna(0).astype(int)
    df_bat['rr_home_sr'] = df_bat['rr_home_sr'].fillna(df_bat['hp_sr']).round(1)
    # RR Home Score: Blends CBPS v4 with home venue SR
    df_bat['rr_home_score'] = np.where(
        df_bat['rr_home_balls'] >= 20,
        (0.65 * df_bat['cbps_score_v4'] + 0.35 * (df_bat['rr_home_sr'] - 142.0) / 30.0).round(2),
        df_bat['cbps_score_v4']
    )
    
    # Bowlers at RR Home
    rr_bowl = bbb[bbb['is_rr_home']].groupby('bowler_id').agg(
        rr_home_balls=('is_legal', 'sum'),
        rr_home_runs=('bowler_runs', 'sum'),
        rr_home_wkts=('is_wicket', 'sum')
    ).reset_index()
    rr_bowl['rr_home_econ'] = ((rr_bowl['rr_home_runs'] / np.maximum(1, rr_bowl['rr_home_balls'])) * 6.0).round(2)
    
    df_bowl = df_bowl.merge(rr_bowl, left_on='player_id', right_on='bowler_id', how='left')
    df_bowl['rr_home_balls'] = df_bowl['rr_home_balls'].fillna(0).astype(int)
    df_bowl['rr_home_econ'] = df_bowl['rr_home_econ'].fillna(df_bowl['hp_econ']).round(2)
    # RR Home Score: Blends CBPS v4 with home venue economy suppression
    df_bowl['rr_home_score'] = np.where(
        df_bowl['rr_home_balls'] >= 20,
        (0.65 * df_bowl['cbps_score_v4'] + 0.35 * (8.80 - df_bowl['rr_home_econ']) / 1.5).round(2),
        df_bowl['cbps_score_v4']
    )
    
    # Save enriched master
    df_bat.to_csv(bat_csv, index=False)
    df_bowl.to_csv(bowl_csv, index=False)
    
    # Update Top 10 with enriched fields
    top10_bat = df_bat.head(10).copy()
    top10_bat.to_csv('rr-submission/v4/stage4_consistency_scoring/top10_batters_v4_final.csv', index=False)
    top10_bat.to_csv('rr-submission/v4/stage5_deliverables/top10_batters_v4.csv', index=False)
    top10_bat.to_csv('rr-submission/v4/top10_batters_final.csv', index=False)
    
    top10_bowl = df_bowl.head(10).copy()
    top10_bowl.to_csv('rr-submission/v4/stage4_consistency_scoring/top10_bowlers_v4_final.csv', index=False)
    top10_bowl.to_csv('rr-submission/v4/stage5_deliverables/top10_bowlers_v4.csv', index=False)
    top10_bowl.to_csv('rr-submission/v4/top10_bowlers_final.csv', index=False)
    
    # Generate Bonus: Auction Targets Top 10
    auction_bat = df_bat[df_bat['is_auction_target']].sort_values(by='cbps_score_v4', ascending=False).head(10).copy()
    auction_bat['auction_rank'] = range(1, len(auction_bat) + 1)
    auction_bat.to_csv('rr-submission/v4/stage5_deliverables/top10_auction_target_batters.csv', index=False)
    
    auction_bowl = df_bowl[df_bowl['is_auction_target']].sort_values(by='cbps_score_v4', ascending=False).head(10).copy()
    auction_bowl['auction_rank'] = range(1, len(auction_bowl) + 1)
    auction_bowl.to_csv('rr-submission/v4/stage5_deliverables/top10_auction_target_bowlers.csv', index=False)
    
    print("Enrichment complete:")
    print(f"  * Batters: {len(df_bat)} active players enriched with auction & RR home stats.")
    print(f"  * Bowlers: {len(df_bowl)} active players enriched with auction & RR home stats.")
    print(f"  * Top Auction Target Batters: {list(auction_bat['player_name'].head(5))}")
    print(f"  * Top Auction Target Bowlers: {list(auction_bowl['player_name'].head(5))}")

if __name__ == '__main__':
    enrich_v4()

