import pdfplumber
import pandas as pd
import numpy as np
import os
import re

def parse_retentions():
    retention_pdf_path = 'cricinfo-data/IPL-2027-retentions/TATA_IPL_2027_-_Retained_Player_List.pdf'
    release_pdf_path = 'cricinfo-data/IPL-2027-retentions/TATA_IPL_2027-_Release_Player_List.pdf'
    clean_squads_path = 'cricinfo-data/IPL-2026-squads/all_ipl_2026_squads_clean.csv'
    
    df_clean = pd.read_csv(clean_squads_path)
    print(f"Loaded {len(df_clean)} reference players from 2026 squads.")
    
    # 1. Parse Retained Players
    with pdfplumber.open(retention_pdf_path) as pdf:
        tables = pdf.pages[0].extract_tables()
        t0 = tables[0]
        t1 = tables[1]
        
    t0_teams = [
        ('Chennai Super Kings', 'CSK'),
        ('Delhi Capitals', 'DC'),
        ('Gujarat Titans', 'GT'),
        ('Kolkata Knight Riders', 'KKR'),
        ('Lucknow Super Giants', 'LSG')
    ]
    t1_teams = [
        ('Mumbai Indians', 'MI'),
        ('Punjab Kings', 'PBKS'),
        ('Rajasthan Royals', 'RR'),
        ('Royal Challengers Bengaluru', 'RCB'),
        ('Sunrisers Hyderabad', 'SRH')
    ]
    
    retained_records = []
    
    def extract_retained_from_table(table, teams, start_row, end_row):
        for col_idx, (t_name, t_code) in enumerate(teams):
            c_star = col_idx * 3
            c_name = col_idx * 3 + 1
            c_sal = col_idx * 3 + 2
            
            for r in table[start_row:end_row]:
                raw_name = r[c_name]
                raw_sal = r[c_sal]
                raw_star = r[c_star]
                
                if raw_name and raw_name.strip() and not raw_name.startswith('No of'):
                    name_str = raw_name.strip()
                    is_traded = '(T)' in name_str
                    clean_name = name_str.replace('(T)', '').strip()
                    is_overseas = (raw_star is not None and '*' in raw_star) or clean_name.startswith('*')
                    if clean_name.startswith('*'):
                        clean_name = clean_name.lstrip('*').strip()
                        
                    sal_val = None
                    if raw_sal and raw_sal.strip():
                        try:
                            sal_val = float(raw_sal.strip())
                        except ValueError:
                            pass
                            
                    sal_cr = (sal_val / 100.0) if sal_val is not None else None
                    if sal_val is not None:
                        if sal_val >= 100:
                            sal_inr = f"₹{sal_cr:.2f} Cr"
                        else:
                            sal_inr = f"₹{int(sal_val)} Lakh"
                    else:
                        sal_inr = "N/A"
                        
                    retained_records.append({
                        'team_name': t_name,
                        'team_code': t_code,
                        'player_name': clean_name,
                        'is_overseas': is_overseas,
                        'is_traded': is_traded,
                        'retention_salary_lakhs': sal_val,
                        'retention_salary_crores': sal_cr,
                        'retention_salary_inr': sal_inr
                    })
                    
    extract_retained_from_table(t0, t0_teams, 3, 26)
    extract_retained_from_table(t1, t1_teams, 2, 23)
    
    df_retained = pd.DataFrame(retained_records)
    print(f"Extracted {len(df_retained)} retained players from PDF.")
    print("Retained counts by team:")
    print(df_retained.groupby(['team_name', 'team_code'])['player_name'].count())
    
    # Enrich with player metadata from df_clean
    df_retained['cricinfo_player_id'] = None
    df_retained['full_name'] = None
    df_retained['official_role'] = None
    df_retained['country'] = None
    df_retained['batting_style'] = None
    df_retained['bowling_style'] = None
    
    for idx, row in df_retained.iterrows():
        pname = row['player_name']
        
        # Match by exact display name or full name
        match = df_clean[df_clean['cricinfo_display_name'].str.lower() == pname.lower()]
        if match.empty:
            match = df_clean[df_clean['full_name'].str.lower() == pname.lower()]
        if match.empty:
            parts = [re.escape(w) for w in pname.split() if len(w) > 2]
            if parts:
                pat = '.*'.join(parts)
                match = df_clean[df_clean['full_name'].str.contains(pat, case=False, na=False) |
                                 df_clean['cricinfo_display_name'].str.contains(pat, case=False, na=False)]
        
        if not match.empty:
            rec = match.iloc[0]
            df_retained.loc[idx, 'cricinfo_player_id'] = rec['player_id']
            df_retained.loc[idx, 'full_name'] = rec['full_name']
            df_retained.loc[idx, 'official_role'] = rec['official_role']
            df_retained.loc[idx, 'batting_style'] = rec['batting_style']
            df_retained.loc[idx, 'bowling_style'] = rec['bowling_style']
            if row['is_overseas']:
                df_retained.loc[idx, 'country'] = rec['country'] if pd.notna(rec['country']) and rec['country'] != 'India' else 'Overseas'
            else:
                df_retained.loc[idx, 'country'] = 'India'
        else:
            df_retained.loc[idx, 'full_name'] = pname
            if row['is_overseas']:
                df_retained.loc[idx, 'country'] = 'Overseas'
            else:
                df_retained.loc[idx, 'country'] = 'India'
                
    # 2. Parse Team Purse and Slot Breakdown
    purse_data = [
        {'team_name': 'Chennai Super Kings', 'team_code': 'CSK', 'retained_players': 19, 'retained_overseas': 6, 'total_money_spent_cr': 101.95, 'retention_deduction_cr': 2.00, 'salary_cap_available_cr': 28.05, 'available_slots': 6, 'available_overseas_slots': 2},
        {'team_name': 'Delhi Capitals', 'team_code': 'DC', 'retained_players': 16, 'retained_overseas': 4, 'total_money_spent_cr': 90.50, 'retention_deduction_cr': 5.50, 'salary_cap_available_cr': 39.50, 'available_slots': 9, 'available_overseas_slots': 4},
        {'team_name': 'Gujarat Titans', 'team_code': 'GT', 'retained_players': 22, 'retained_overseas': 6, 'total_money_spent_cr': 121.25, 'retention_deduction_cr': 0.00, 'salary_cap_available_cr': 8.75, 'available_slots': 3, 'available_overseas_slots': 2},
        {'team_name': 'Kolkata Knight Riders', 'team_code': 'KKR', 'retained_players': 17, 'retained_overseas': 5, 'total_money_spent_cr': 88.35, 'retention_deduction_cr': 6.00, 'salary_cap_available_cr': 41.65, 'available_slots': 8, 'available_overseas_slots': 3},
        {'team_name': 'Lucknow Super Giants', 'team_code': 'LSG', 'retained_players': 18, 'retained_overseas': 5, 'total_money_spent_cr': 82.55, 'retention_deduction_cr': 0.00, 'salary_cap_available_cr': 47.45, 'available_slots': 7, 'available_overseas_slots': 3},
        {'team_name': 'Mumbai Indians', 'team_code': 'MI', 'retained_players': 16, 'retained_overseas': 6, 'total_money_spent_cr': 97.40, 'retention_deduction_cr': 0.00, 'salary_cap_available_cr': 32.60, 'available_slots': 9, 'available_overseas_slots': 2},
        {'team_name': 'Punjab Kings', 'team_code': 'PBKS', 'retained_players': 19, 'retained_overseas': 6, 'total_money_spent_cr': 111.40, 'retention_deduction_cr': 0.00, 'salary_cap_available_cr': 18.60, 'available_slots': 6, 'available_overseas_slots': 2},
        {'team_name': 'Rajasthan Royals', 'team_code': 'RR', 'retained_players': 19, 'retained_overseas': 5, 'total_money_spent_cr': 102.95, 'retention_deduction_cr': 0.00, 'salary_cap_available_cr': 27.05, 'available_slots': 6, 'available_overseas_slots': 3},
        {'team_name': 'Royal Challengers Bengaluru', 'team_code': 'RCB', 'retained_players': 20, 'retained_overseas': 7, 'total_money_spent_cr': 115.85, 'retention_deduction_cr': 0.00, 'salary_cap_available_cr': 14.15, 'available_slots': 5, 'available_overseas_slots': 1},
        {'team_name': 'Sunrisers Hyderabad', 'team_code': 'SRH', 'retained_players': 18, 'retained_overseas': 5, 'total_money_spent_cr': 89.85, 'retention_deduction_cr': 0.00, 'salary_cap_available_cr': 40.15, 'available_slots': 7, 'available_overseas_slots': 3},
    ]
    df_purse = pd.DataFrame(purse_data)
    
    # 3. Save Files
    out_dir = 'cricinfo-data/IPL-2027-retentions'
    os.makedirs(out_dir, exist_ok=True)
    
    # Sort columns
    cols = [
        'team_name', 'team_code', 'player_name', 'full_name', 'is_overseas', 'is_traded',
        'retention_salary_crores', 'retention_salary_lakhs', 'retention_salary_inr',
        'official_role', 'country', 'batting_style', 'bowling_style', 'cricinfo_player_id'
    ]
    df_retained = df_retained[cols].sort_values(
        by=['team_name', 'retention_salary_crores', 'player_name'],
        ascending=[True, False, True]
    ).reset_index(drop=True)
    
    # Master CSVs
    for p in ['IPL-2027-retentions.csv', 'all_ipl_2027_retentions.csv', os.path.join(out_dir, 'all_ipl_2027_retentions.csv')]:
        try:
            df_retained.to_csv(p, index=False, encoding='utf-8')
            print(f"Saved: {p}")
        except PermissionError:
            alt_p = p.replace('.csv', '_clean.csv')
            df_retained.to_csv(alt_p, index=False, encoding='utf-8')
            print(f"Locked by Excel, saved to: {alt_p}")
            
    df_purse.to_csv(os.path.join(out_dir, 'ipl_2027_team_purses_and_slots.csv'), index=False, encoding='utf-8')
    print(f"Saved: {os.path.join(out_dir, 'ipl_2027_team_purses_and_slots.csv')}")
    
    # Team-wise individual retentions files
    print("\nGenerating team-specific retentions files:")
    for (t_name, t_code), grp in df_retained.groupby(['team_name', 'team_code']):
        safe_name = t_code.lower() + "_retentions_2027.csv"
        path = os.path.join(out_dir, safe_name)
        grp.to_csv(path, index=False, encoding='utf-8')
        total_cr = grp['retention_salary_crores'].sum()
        overseas_count = grp['is_overseas'].sum()
        traded_count = grp['is_traded'].sum()
        print(f"  * {t_name} ({t_code}): {len(grp)} players ({overseas_count} overseas, {traded_count} traded) | Total: ₹{total_cr:.2f} Cr -> {path}")

    # 4. Parse Released Players from PDF
    print("\nParsing Released Players from PDF...")
    with pdfplumber.open(release_pdf_path) as pdf:
        rel_table = pdf.pages[0].extract_tables()[0]
        
    released_records = []
    
    def extract_released_from_table(table, teams, start_row, end_row):
        for col_idx, (t_name, t_code) in enumerate(teams):
            c_star = col_idx * 3
            c_name = col_idx * 3 + 1
            c_sal = col_idx * 3 + 2
            
            for r in table[start_row:end_row]:
                raw_name = r[c_name]
                raw_sal = r[c_sal]
                raw_star = r[c_star]
                
                if raw_name and raw_name.strip() and not raw_name.startswith('No of'):
                    text = raw_name.strip()
                    m = re.match(r'^(.*?)\s+(\d+)$', text)
                    if m and not raw_sal:
                        clean_name = m.group(1).strip()
                        raw_sal = m.group(2).strip()
                    else:
                        clean_name = text
                        
                    is_overseas = (raw_star is not None and '*' in raw_star) or clean_name.startswith('*')
                    if clean_name.startswith('*'):
                        clean_name = clean_name.lstrip('*').strip()
                        
                    sal_val = None
                    if raw_sal and str(raw_sal).strip():
                        try:
                            sal_val = float(str(raw_sal).strip())
                        except ValueError:
                            pass
                            
                    sal_cr = (sal_val / 100.0) if sal_val is not None else None
                    if sal_val is not None:
                        if sal_val >= 100:
                            sal_inr = f"₹{sal_cr:.2f} Cr"
                        else:
                            sal_inr = f"₹{int(sal_val)} Lakh"
                    else:
                        sal_inr = "N/A"
                        
                    released_records.append({
                        'team_name': t_name,
                        'team_code': t_code,
                        'player_name': clean_name,
                        'is_overseas': is_overseas,
                        'previous_salary_lakhs': sal_val,
                        'previous_salary_crores': sal_cr,
                        'previous_salary_inr': sal_inr
                    })
                    
    extract_released_from_table(rel_table, t0_teams, 3, 17)
    extract_released_from_table(rel_table, t1_teams, 21, 38)
    
    df_released = pd.DataFrame(released_records)
    print(f"Extracted {len(df_released)} released players from PDF.")
    print("Released counts by team:")
    print(df_released.groupby(['team_name', 'team_code'])['player_name'].count())
    
    # Enrich released players
    df_released['cricinfo_player_id'] = None
    df_released['full_name'] = None
    df_released['official_role'] = None
    df_released['country'] = None
    df_released['batting_style'] = None
    df_released['bowling_style'] = None
    
    for idx, row in df_released.iterrows():
        pname = row['player_name']
        match = df_clean[df_clean['cricinfo_display_name'].str.lower() == pname.lower()]
        if match.empty:
            match = df_clean[df_clean['full_name'].str.lower() == pname.lower()]
        if match.empty:
            parts = [re.escape(w) for w in pname.split() if len(w) > 2]
            if parts:
                pat = '.*'.join(parts)
                match = df_clean[df_clean['full_name'].str.contains(pat, case=False, na=False) |
                                 df_clean['cricinfo_display_name'].str.contains(pat, case=False, na=False)]
        
        if not match.empty:
            rec = match.iloc[0]
            df_released.loc[idx, 'cricinfo_player_id'] = rec['player_id']
            df_released.loc[idx, 'full_name'] = rec['full_name']
            df_released.loc[idx, 'official_role'] = rec['official_role']
            df_released.loc[idx, 'batting_style'] = rec['batting_style']
            df_released.loc[idx, 'bowling_style'] = rec['bowling_style']
            if row['is_overseas']:
                df_released.loc[idx, 'country'] = rec['country'] if pd.notna(rec['country']) and rec['country'] != 'India' else 'Overseas'
            else:
                df_released.loc[idx, 'country'] = 'India'
        else:
            df_released.loc[idx, 'full_name'] = pname
            if row['is_overseas']:
                df_released.loc[idx, 'country'] = 'Overseas'
            else:
                df_released.loc[idx, 'country'] = 'India'
                
    rel_cols = [
        'team_name', 'team_code', 'player_name', 'full_name', 'is_overseas',
        'previous_salary_crores', 'previous_salary_lakhs', 'previous_salary_inr',
        'official_role', 'country', 'batting_style', 'bowling_style', 'cricinfo_player_id'
    ]
    df_released = df_released[rel_cols].sort_values(
        by=['team_name', 'previous_salary_crores', 'player_name'],
        ascending=[True, False, True]
    ).reset_index(drop=True)
    
    # Save released files
    for p in ['IPL-2027-released.csv', 'all_ipl_2027_released.csv', os.path.join(out_dir, 'all_ipl_2027_released.csv')]:
        try:
            df_released.to_csv(p, index=False, encoding='utf-8')
            print(f"Saved: {p}")
        except PermissionError:
            alt_p = p.replace('.csv', '_clean.csv')
            df_released.to_csv(alt_p, index=False, encoding='utf-8')
            print(f"Locked by Excel, saved to: {alt_p}")
            
    for (t_name, t_code), grp in df_released.groupby(['team_name', 'team_code']):
        safe_name = t_code.lower() + "_released_2027.csv"
        path = os.path.join(out_dir, safe_name)
        grp.to_csv(path, index=False, encoding='utf-8')

if __name__ == '__main__':
    parse_retentions()
