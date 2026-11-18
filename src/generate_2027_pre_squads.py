import pandas as pd
import os
import re

def build_2027_pre_squads():
    squads_2026_clean = 'cricinfo-data/IPL-2026-squads/all_ipl_2026_squads_clean.csv'
    trades_path = 'IPL-2027-trades.csv'
    
    df_squads = pd.read_csv(squads_2026_clean)
    df_trades = pd.read_csv(trades_path)
    
    print(f"Loaded {len(df_squads)} verified players from clean 2026 squads.")
    print(f"Loaded {len(df_trades)} trade records from IPL-2027-trades.csv.")
    
    trade_map = {}
    for _, tr in df_trades.iterrows():
        pname = tr['player_name']
        trade_map[pname] = tr
        
    name_alias = {
        'T. Natarajan': ['T Natarajan', 'Thangarasu Natarajan'],
        'Hardik Pandya': ['Hardik Pandya', 'Hardik Himanshu Pandya'],
        'Arshdeep Singh': ['Arshdeep Singh'],
        'Liam Livingstone': ['Liam Livingstone', 'Liam Stephen Livingstone'],
        'Jack Edwards': ['Jack Edwards', 'Jack Richard Edwards'],
        'Khaleel Ahmed': ['Khaleel Ahmed', 'Khaleel Khursheed Ahmed'],
        'Nathan Ellis': ['Nathan Ellis'],
        'Zeeshan Ansari': ['Zeeshan Ansari'],
        'Rishabh Pant': ['Rishabh Pant', 'Rishabh Rajendra Pant'],
        'Kuldeep Yadav': ['Kuldeep Yadav'],
        'Mohd Shami': ['Mohd Shami', 'Mohammed Shami', 'Mohammed Shami Ahmed'],
        'M. Siddharth': ['M. Siddharth', 'M Siddharth', 'Manimaran Siddharth'],
        'Sam Curran': ['Sam Curran', 'Samuel Matthew Curran'],
        'Harshal Patel': ['Harshal Patel', 'Harshal Vikram Patel']
    }
    
    df_2027 = df_squads.copy()
    df_2027['season'] = 2027
    df_2027['team_name_2026'] = df_2027['team_name']
    df_2027['team_name_2027'] = df_2027['team_name']
    df_2027['is_traded_for_2027'] = False
    df_2027['trade_type'] = 'Retained in Squad'
    df_2027['trade_fee_crores'] = None
    df_2027['trade_fee_inr'] = None
    df_2027['trade_fee_status'] = 'N/A (Standard Contract / Retained)'
    df_2027['trade_notes'] = ''
    
    applied_trades = 0
    for trade_key, aliases in name_alias.items():
        tr_info = trade_map.get(trade_key)
        if tr_info is None:
            continue
            
        mask = df_2027['cricinfo_display_name'].isin(aliases) | df_2027['full_name'].isin(aliases)
        idx_list = df_2027[mask].index.tolist()
        
        if not idx_list:
            sub_mask = df_2027['full_name'].str.contains(trade_key.replace('.', ''), case=False, na=False)
            idx_list = df_2027[sub_mask].index.tolist()
            
        for idx in idx_list:
            old_team = df_2027.loc[idx, 'team_name_2026']
            new_team = tr_info['to_team']
            
            df_2027.loc[idx, 'team_name_2027'] = new_team
            df_2027.loc[idx, 'is_traded_for_2027'] = True
            df_2027.loc[idx, 'trade_type'] = tr_info['trade_type']
            df_2027.loc[idx, 'trade_fee_crores'] = tr_info['trade_fee_crores']
            df_2027.loc[idx, 'trade_fee_inr'] = tr_info['trade_fee_inr']
            df_2027.loc[idx, 'trade_fee_status'] = tr_info['fee_status']
            df_2027.loc[idx, 'trade_notes'] = tr_info['notes']
            
            if df_2027.loc[idx, 'is_captain']:
                df_2027.loc[idx, 'is_captain'] = False
                
            applied_trades += 1
            print(f"Applied trade: {df_2027.loc[idx, 'full_name']} | {old_team} -> {new_team} ({tr_info['trade_fee_inr']})")
            
    print(f"\nTotal trades successfully applied: {applied_trades}/{len(df_trades)}")
    
    df_2027['team_name'] = df_2027['team_name_2027']
    
    col_order = [
        'season',
        'team_name_2027',
        'team_name_2026',
        'player_id',
        'full_name',
        'cricinfo_display_name',
        'country',
        'official_role',
        'squad_role',
        'batting_style',
        'bowling_style',
        'is_captain',
        'is_wicketkeeper',
        'is_traded_for_2027',
        'trade_type',
        'trade_fee_crores',
        'trade_fee_inr',
        'trade_fee_status',
        'trade_notes',
        'age',
        'date_of_birth',
        'cricinfo_player_url',
        'headshot_url'
    ]
    
    df_2027 = df_2027[col_order].sort_values(by=['team_name_2027', 'is_traded_for_2027', 'official_role', 'full_name'], ascending=[True, False, True, True]).reset_index(drop=True)
    
    # Verify duplicates
    dups_2027 = df_2027.groupby('player_id')['team_name_2027'].apply(list)
    multi_2027 = dups_2027[dups_2027.apply(len) > 1]
    print(f"\nCheck for multi-team duplicates in 2027 pre-squads: {len(multi_2027)} duplicates.")
    
    # Save locations
    out_dir_2027 = 'cricinfo-data/IPL-2027-pre-squads'
    os.makedirs(out_dir_2027, exist_ok=True)
    
    csv_destinations = [
        'all_ipl_2027_pre-squads.csv',
        'cricinfo-data/all_ipl_2027_pre-squads.csv',
        os.path.join(out_dir_2027, 'all_ipl_2027_pre-squads.csv')
    ]
    
    for path in csv_destinations:
        try:
            df_2027.to_csv(path, index=False, encoding='utf-8')
            print(f"Saved: {path}")
        except PermissionError:
            alt_path = path.replace('.csv', '_clean.csv')
            df_2027.to_csv(alt_path, index=False, encoding='utf-8')
            print(f"File locked by another app, saved to: {alt_path}")
            
    # Save team-specific 2027 pre-squad files
    print("\nGenerating team-specific 2027 pre-squad files:")
    for team, grp in df_2027.groupby('team_name_2027'):
        safe_team = re.sub(r'[^a-zA-Z0-9]+', '_', team.lower()).strip('_')
        team_file = os.path.join(out_dir_2027, f"{safe_team}_pre_squad_2027.csv")
        grp.to_csv(team_file, index=False, encoding='utf-8')
        traded_count = grp['is_traded_for_2027'].sum()
        print(f"  * {team}: {len(grp)} players ({traded_count} traded-in) -> {team_file}")

if __name__ == '__main__':
    build_2027_pre_squads()
