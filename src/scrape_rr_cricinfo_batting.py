import os
import re
import json
import time
import requests
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor, as_completed
import pandas as pd

OUTPUT_DIR = 'cricinfo-data'
CACHE_DIR = os.path.join(OUTPUT_DIR, 'player_profiles_cache')
os.makedirs(CACHE_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
}

def fetch_statsguru_pages():
    base_url = (
        'https://stats.cricinfo.com/ci/engine/stats/index.html?'
        'class=6;filter=advanced;ground=2865;ground=664;orderby=runs;'
        'page={page};size=200;spanmax1=2026;spanmin1=2008;spanval1=span;'
        'template=results;type=batting'
    )
    
    session = requests.Session()
    session.headers.update(HEADERS)
    
    all_batting_records = []
    
    print("=== Step 1: Fetching Statsguru Batting Records across all pages ===")
    for page in range(1, 10):
        url = base_url.format(page=page)
        print(f"Fetching Statsguru Page {page}...")
        try:
            r = session.get(url, timeout=20)
            if r.status_code != 200:
                print(f"Page {page} returned status {r.status_code}, terminating page loop.")
                break
                
            soup = BeautifulSoup(r.text, 'lxml')
            tables = soup.find_all('table', class_='engineTable')
            if len(tables) < 3:
                print(f"No results table found on page {page}, finished.")
                break
                
            table = tables[2] # 'Overall figures'
            trs = table.find_all('tr')
            
            page_records = 0
            current_rec = None
            
            for tr in trs:
                cl = tr.get('class')
                if cl == ['data2']:
                    tds = tr.find_all('td')
                    if len(tds) >= 15:
                        a_tag = tds[0].find('a')
                        short_name = tds[0].get_text(strip=True)
                        href = a_tag['href'] if a_tag else ''
                        m = re.search(r'/player/(\d+)\.html', href)
                        player_id = m.group(1) if m else ''
                        
                        current_rec = {
                            'player_id': player_id,
                            'statsguru_abbrev_name': short_name,
                            'cricinfo_player_url': f"https://www.espncricinfo.com/cricketers/{player_id}" if player_id else '',
                            'teams_at_rr_grounds': '',
                            'span': tds[1].get_text(strip=True),
                            'matches': tds[2].get_text(strip=True),
                            'innings': tds[3].get_text(strip=True),
                            'not_outs': tds[4].get_text(strip=True),
                            'runs': tds[5].get_text(strip=True),
                            'highest_score': tds[6].get_text(strip=True),
                            'batting_average': tds[7].get_text(strip=True),
                            'balls_faced': tds[8].get_text(strip=True),
                            'strike_rate': tds[9].get_text(strip=True),
                            'centuries': tds[10].get_text(strip=True),
                            'half_centuries': tds[11].get_text(strip=True),
                            'ducks': tds[12].get_text(strip=True),
                            'fours': tds[13].get_text(strip=True),
                            'sixes': tds[14].get_text(strip=True),
                        }
                        all_batting_records.append(current_rec)
                        page_records += 1
                elif cl == ['note'] and current_rec is not None:
                    note_text = tr.get_text(strip=True).strip('()')
                    current_rec['teams_at_rr_grounds'] = note_text
                    
            print(f"  -> Extracted {page_records} player batting records from Page {page}.")
            if page_records == 0:
                break
                
            time.sleep(1.0)
        except Exception as e:
            print(f"Error fetching page {page}: {e}")
            break
            
    print(f"Total Batting Records Retrieved: {len(all_batting_records)}")
    return all_batting_records

def get_player_profile(player_id, session):
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
            r = session.get(api_url, timeout=12)
            if r.status_code == 200:
                data = r.json()
                athlete = data.get('athlete', {})
                
                # Extract clean structured profile fields
                bat_style_list = athlete.get('batStyle', [])
                bat_style = bat_style_list[0].get('description', '') if bat_style_list else ''
                
                bowl_style_list = athlete.get('bowlStyle', [])
                bowl_style = bowl_style_list[0].get('description', '') if bowl_style_list else ''
                
                profile = {
                    'full_name': athlete.get('fullName', ''),
                    'short_name': athlete.get('shortName', ''),
                    'display_name': athlete.get('displayName', ''),
                    'first_name': athlete.get('firstName', ''),
                    'last_name': athlete.get('lastName', ''),
                    'date_of_birth': athlete.get('displayDOB', ''),
                    'age': athlete.get('age', ''),
                    'gender': athlete.get('gender', ''),
                    'country': athlete.get('team', {}).get('displayName', '') or athlete.get('team', {}).get('name', ''),
                    'playing_role': athlete.get('position', {}).get('name', ''),
                    'batting_style': bat_style,
                    'bowling_style': bowl_style,
                    'headshot_url': athlete.get('headshot', {}).get('href', ''),
                    'is_active': athlete.get('active', '')
                }
                
                # Save to cache
                with open(cache_file, 'w', encoding='utf-8') as f:
                    json.dump(profile, f, indent=2)
                    
                return profile
            elif r.status_code == 404:
                return {}
        except Exception:
            time.sleep(0.5)
            
    return {}

def enrich_with_player_profiles(records):
    print("\n=== Step 2: Fetching individual player profiles for full name & metadata ===")
    unique_ids = sorted(list(set(r['player_id'] for r in records if r.get('player_id'))))
    print(f"Total Unique Players to Profile: {len(unique_ids)}")
    
    profiles = {}
    session = requests.Session()
    session.headers.update(HEADERS)
    
    start_time = time.time()
    completed = 0
    
    with ThreadPoolExecutor(max_workers=12) as executor:
        future_to_id = {executor.submit(get_player_profile, pid, session): pid for pid in unique_ids}
        for future in as_completed(future_to_id):
            pid = future_to_id[future]
            try:
                prof = future.result()
                profiles[pid] = prof
            except Exception as e:
                profiles[pid] = {}
            completed += 1
            if completed % 100 == 0 or completed == len(unique_ids):
                elapsed = time.time() - start_time
                print(f"  -> Profiled {completed}/{len(unique_ids)} players ({completed/elapsed:.1f} profiles/sec)...")
                
    print(f"Completed profiling in {time.time() - start_time:.1f} seconds.")
    
    # Merge profiles into records
    enriched = []
    for r in records:
        pid = r.get('player_id')
        prof = profiles.get(pid, {})
        
        merged_row = {
            'player_id': pid,
            'full_name': prof.get('full_name') or prof.get('displayName') or r.get('statsguru_abbrev_name'),
            'short_name': prof.get('short_name') or r.get('statsguru_abbrev_name'),
            'statsguru_abbrev_name': r.get('statsguru_abbrev_name'),
            'country': prof.get('country', ''),
            'playing_role': prof.get('playing_role', ''),
            'batting_style': prof.get('batting_style', ''),
            'bowling_style': prof.get('bowling_style', ''),
            'date_of_birth': prof.get('date_of_birth', ''),
            'age': prof.get('age', ''),
            'teams_at_rr_grounds': r.get('teams_at_rr_grounds', ''),
            'span': r.get('span', ''),
            'matches': r.get('matches', ''),
            'innings': r.get('innings', ''),
            'not_outs': r.get('not_outs', ''),
            'runs': r.get('runs', ''),
            'highest_score': r.get('highest_score', ''),
            'batting_average': r.get('batting_average', ''),
            'balls_faced': r.get('balls_faced', ''),
            'strike_rate': r.get('strike_rate', ''),
            'centuries': r.get('centuries', ''),
            'half_centuries': r.get('half_centuries', ''),
            'ducks': r.get('ducks', ''),
            'fours': r.get('fours', ''),
            'sixes': r.get('sixes', ''),
            'cricinfo_player_url': r.get('cricinfo_player_url', ''),
            'headshot_url': prof.get('headshot_url', ''),
        }
        enriched.append(merged_row)
        
    return enriched

def main():
    records = fetch_statsguru_pages()
    enriched_records = enrich_with_player_profiles(records)
    
    df = pd.DataFrame(enriched_records)
    csv_path = os.path.join(OUTPUT_DIR, 'rr_home_grounds_batting_records.csv')
    df.to_csv(csv_path, index=False, encoding='utf-8')
    print(f"\n=== Successfully saved all {len(df)} player records to: {csv_path} ===")
    
    print("\nSample top 10 rows:")
    print(df[['player_id', 'full_name', 'statsguru_abbrev_name', 'country', 'playing_role', 'runs', 'batting_average', 'strike_rate', 'teams_at_rr_grounds']].head(10))

if __name__ == '__main__':
    main()

