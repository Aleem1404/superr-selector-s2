import os
import re
import json
import time
from curl_cffi import requests
from bs4 import BeautifulSoup
import pandas as pd

BASE_DIR = 'cricinfo-data'
SQUADS_DIR = os.path.join(BASE_DIR, 'IPL-2026-squads')
CACHE_DIR = os.path.join(BASE_DIR, 'player_profiles_cache')
os.makedirs(SQUADS_DIR, exist_ok=True)
os.makedirs(CACHE_DIR, exist_ok=True)

MAIN_SQUADS_URL = 'https://www.espncricinfo.com/series/ipl-2026-1510719/squads'

def get_player_full_profile(player_id, session):
    if not player_id:
        return {}
        
    cache_file = os.path.join(CACHE_DIR, f"{player_id}.json")
    if os.path.exists(cache_file):
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            pass
            
    api_url = f"https://site.web.api.espn.com/apis/common/v3/sports/cricket/athletes/{player_id}"
    for attempt in range(3):
        try:
            r = session.get(api_url, timeout=10)
            if r.status_code == 200:
                data = r.json()
                athlete = data.get('athlete', {})
                
                bat_style_list = athlete.get('batStyle', [])
                bat_style = bat_style_list[0].get('description', '') if bat_style_list else ''
                
                bowl_style_list = athlete.get('bowlStyle', [])
                bowl_style = bowl_style_list[0].get('description', '') if bowl_style_list else ''
                
                profile = {
                    'full_name': athlete.get('fullName', ''),
                    'short_name': athlete.get('shortName', ''),
                    'display_name': athlete.get('displayName', ''),
                    'date_of_birth': athlete.get('displayDOB', ''),
                    'age': athlete.get('age', ''),
                    'gender': athlete.get('gender', ''),
                    'country': athlete.get('team', {}).get('displayName', '') or athlete.get('team', {}).get('name', ''),
                    'playing_role': athlete.get('position', {}).get('name', ''),
                    'batting_style': bat_style,
                    'bowling_style': bowl_style,
                    'headshot_url': athlete.get('headshot', {}).get('href', ''),
                }
                
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(profile, f, indent=2)
                    
                return profile
        except Exception:
            time.sleep(0.4)
            
    return {}

def scrape_squads():
    print(f"Fetching main squads page: {MAIN_SQUADS_URL}...")
    r = requests.get(MAIN_SQUADS_URL, impersonate='chrome120')
    if r.status_code != 200:
        print(f"Failed to fetch squads page, status: {r.status_code}")
        return
        
    soup = BeautifulSoup(r.text, 'lxml')
    links = soup.find_all('a', href=re.compile(r'/series/ipl-2026-1510719/.*squad'))
    
    squad_teams = []
    seen_hrefs = set()
    
    for a in links:
        href = a['href']
        txt = a.get_text(strip=True)
        if '/squads' in href and not '/series-squads' in href:
            continue
        if href not in seen_hrefs:
            seen_hrefs.add(href)
            team_name = txt.replace(' Squad', '').strip()
            if not team_name:
                m = re.search(r'/([^/]+)-squad-', href)
                team_name = m.group(1).replace('-', ' ').title() if m else 'Team'
            full_url = f"https://www.espncricinfo.com{href}" if href.startswith('/') else href
            squad_teams.append({
                'team_name': team_name,
                'url': full_url
            })
            
    print(f"Discovered {len(squad_teams)} team squads to fetch:")
    for t in squad_teams:
        print(f" - {t['team_name']}: {t['url']}")
        
    all_squad_rows = []
    
    import requests as py_requests
    api_session = py_requests.Session()
    api_session.headers.update({'User-Agent': 'Mozilla/5.0'})
    
    for team in squad_teams:
        tname = team['team_name']
        turl = team['url']
        print(f"\nProcessing verified squad: {tname}...")
        
        try:
            resp = requests.get(turl, impersonate='chrome120')
            if resp.status_code != 200:
                print(f"  Error fetching {tname}, status {resp.status_code}")
                continue
                
            s_soup = BeautifulSoup(resp.text, 'lxml')
            
            # CRITICAL FIX: Only select cards inside the squad grids (Batters, All-rounders, Bowlers)
            # This completely excludes the right-side tournament stats leaderboard widget!
            squad_grids = s_soup.find_all('div', class_=re.compile(r'ds-grid.*lg:ds-grid-cols-2'))
            
            team_players = []
            seen_pids = set()
            
            for grid in squad_grids:
                cards = grid.find_all('div', class_=re.compile(r'ds-relative.*ds-flex-row.*ds-space-x-4'))
                for card in cards:
                    a_tag = card.find('a', href=re.compile(r'/cricketers/'))
                    if not a_tag:
                        continue
                        
                    href = a_tag['href']
                    m = re.search(r'/cricketers/.*?(\d+)$', href)
                    pid = m.group(1) if m else ''
                    if not pid or pid in seen_pids:
                        continue
                    seen_pids.add(pid)
                    
                    card_text = card.get_text(separator=' | ', strip=True)
                    name_links = [a.get_text(strip=True) for a in card.find_all('a') if a.get_text(strip=True)]
                    display_name = name_links[0] if name_links else ''
                    
                    is_captain = '(c)' in card_text or '(C)' in card_text
                    is_wk = '†' in card_text or 'Wicketkeeper' in card_text
                    
                    # Extract role
                    role = ''
                    for r_candidate in ['Top order Batter', 'Opening Batter', 'Middle order Batter', 'Wicketkeeper Batter', 'Batter', 'Bowling Allrounder', 'Batting Allrounder', 'Allrounder', 'Bowler']:
                        if r_candidate in card_text:
                            role = r_candidate
                            break
                            
                    age_match = re.search(r'Age\s*\|\s*:\s*\|\s*([^|]+)', card_text)
                    age_str = age_match.group(1).strip() if age_match else ''
                    
                    bat_match = re.search(r'Batting\s*\|\s*:\s*\|\s*([^|]+)', card_text)
                    bat_style = bat_match.group(1).strip() if bat_match else ''
                    
                    bowl_match = re.search(r'Bowling\s*\|\s*:\s*\|\s*([^|]+)', card_text)
                    bowl_style = bowl_match.group(1).strip() if bowl_match else ''
                    
                    # Enrich profile
                    prof = get_player_full_profile(pid, api_session)
                    full_name = prof.get('full_name') or prof.get('displayName') or display_name
                    country = prof.get('country') or ''
                    official_role = prof.get('playing_role') or role
                    
                    player_entry = {
                        'team_name': tname,
                        'player_id': pid,
                        'full_name': full_name,
                        'cricinfo_display_name': display_name,
                        'is_captain': is_captain,
                        'is_wicketkeeper': is_wk,
                        'squad_role': role,
                        'official_role': official_role,
                        'country': country,
                        'age': age_str or prof.get('age', ''),
                        'date_of_birth': prof.get('date_of_birth', ''),
                        'batting_style': bat_style or prof.get('batting_style', ''),
                        'bowling_style': bowl_style or prof.get('bowling_style', ''),
                        'cricinfo_player_url': f"https://www.espncricinfo.com{href}" if href.startswith('/') else href,
                        'headshot_url': prof.get('headshot_url', ''),
                    }
                    
                    team_players.append(player_entry)
                    all_squad_rows.append(player_entry)
                    
            print(f"  -> Extracted {len(team_players)} verified players for {tname}")
            
            safe_team_name = re.sub(r'[^a-zA-Z0-9]+', '_', tname.lower()).strip('_')
            team_csv = os.path.join(SQUADS_DIR, f"{safe_team_name}_squad_2026.csv")
            pd.DataFrame(team_players).to_csv(team_csv, index=False, encoding='utf-8')
            print(f"  -> Saved {team_csv}")
            
            time.sleep(0.8)
        except Exception as e:
            print(f"Error scraping {tname}: {e}")
            
    master_csv = os.path.join(SQUADS_DIR, 'all_ipl_2026_squads.csv')
    df_all = pd.DataFrame(all_squad_rows)
    df_all.to_csv(master_csv, index=False, encoding='utf-8')
    print(f"\n=== Successfully saved all {len(df_all)} verified IPL 2026 players across {len(squad_teams)} teams to {master_csv} ===")
    
    print("\nVerified squad counts per team in IPL 2026:")
    print(df_all.groupby('team_name')['full_name'].count())
    
    # Check for any duplicates across teams
    dups = df_all.groupby('player_id')['team_name'].apply(list)
    multi = dups[dups.apply(len) > 1]
    print(f"\nCheck for multi-team duplicates: {len(multi)} players found in multiple teams.")
    if len(multi) > 0:
        for pid, tms in multi.items():
            print(f"  * {pid}: {tms}")

if __name__ == '__main__':
    scrape_squads()
