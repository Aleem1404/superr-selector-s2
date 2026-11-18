import requests
from bs4 import BeautifulSoup
import re

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
})

base_url = 'https://stats.cricinfo.com/ci/engine/stats/index.html?class=6;filter=advanced;ground=2865;ground=664;orderby=runs;page={page};size=200;spanmax1=2026;spanmin1=2008;spanval1=span;template=results;type=batting'

all_players = []

for page in range(1, 10):
    url = base_url.format(page=page)
    print(f'Fetching page {page}...')
    r = session.get(url, timeout=15)
    soup = BeautifulSoup(r.text, 'lxml')
    
    tables = soup.find_all('table', class_='engineTable')
    if len(tables) < 3:
        print(f'No table on page {page}, stopping.')
        break
        
    table = tables[2] # Overall figures
    trs = table.find_all('tr')
    
    page_count = 0
    for tr in trs:
        # Check if it is a data2 row
        if tr.get('class') == ['data2']:
            tds = tr.find_all('td')
            if len(tds) >= 15:
                a_tag = tds[0].find('a')
                player_cricinfo_name = tds[0].get_text(strip=True)
                player_href = a_tag['href'] if a_tag else ''
                # Extract player id from href e.g. /ci/content/player/277916.html
                m = re.search(r'/player/(\d+)\.html', player_href)
                player_id = m.group(1) if m else ''
                
                span = tds[1].get_text(strip=True)
                mat = tds[2].get_text(strip=True)
                inns = tds[3].get_text(strip=True)
                no = tds[4].get_text(strip=True)
                runs = tds[5].get_text(strip=True)
                hs = tds[6].get_text(strip=True)
                ave = tds[7].get_text(strip=True)
                bf = tds[8].get_text(strip=True)
                sr = tds[9].get_text(strip=True)
                hundreds = tds[10].get_text(strip=True)
                fifties = tds[11].get_text(strip=True)
                ducks = tds[12].get_text(strip=True)
                fours = tds[13].get_text(strip=True)
                sixes = tds[14].get_text(strip=True)
                
                all_players.append({
                    'player_id': player_id,
                    'cricinfo_short_name': player_cricinfo_name,
                    'player_profile_url': f'https://www.espncricinfo.com/cricketers/{player_id}' if player_id else '',
                    'span': span,
                    'matches': mat,
                    'innings': inns,
                    'not_outs': no,
                    'runs': runs,
                    'highest_score': hs,
                    'batting_average': ave,
                    'balls_faced': bf,
                    'strike_rate': sr,
                    'centuries': hundreds,
                    'half_centuries': fifties,
                    'ducks': ducks,
                    'fours': fours,
                    'sixes': sixes,
                })
                page_count += 1
                
    print(f'Page {page}: found {page_count} players.')
    if page_count == 0:
        break

print(f'Total player batting records fetched: {len(all_players)}')

