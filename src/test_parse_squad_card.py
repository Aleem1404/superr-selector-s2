from curl_cffi import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.espncricinfo.com/series/ipl-2026-1510719/rajasthan-royals-squad-1511089/series-squads'
r = requests.get(url, impersonate='chrome120')
soup = BeautifulSoup(r.text, 'lxml')

cards = []
for a in soup.find_all('a', href=re.compile(r'/cricketers/')):
    href = a['href']
    # Check if this link has player name
    name = a.get_text(strip=True)
    if not name:
        continue
        
    # The container for this player usually contains age, batting, etc.
    # Let's find the card container
    parent = a
    for _ in range(6):
        if parent.parent:
            parent = parent.parent
            text = parent.get_text(strip=True)
            if 'Age' in text and 'Batting' in text:
                break
                
    m = re.search(r'/cricketers/.*?(\d+)$', href)
    pid = m.group(1) if m else ''
    
    # Avoid duplicate links of the same player
    if any(c['player_id'] == pid for c in cards):
        continue
        
    cards.append({
        'player_id': pid,
        'name': name,
        'href': href,
        'card_text': parent.get_text(separator=' | ', strip=True)
    })

print(f'Total unique player cards extracted for RR: {len(cards)}')
for c in cards[:5]:
    print('Player:', c['name'], c['player_id'])
    print('Card text:', c['card_text'][:150])
    print()

