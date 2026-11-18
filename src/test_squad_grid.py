from curl_cffi import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.espncricinfo.com/series/ipl-2026-1510719/rajasthan-royals-squad-1511089/series-squads'
r = requests.get(url, impersonate='chrome120')
soup = BeautifulSoup(r.text, 'lxml')

squad_grids = soup.find_all('div', class_=re.compile(r'ds-grid.*lg:ds-grid-cols-2'))
print(f'Squad grids found: {len(squad_grids)}')

squad_players = []
for grid in squad_grids:
    cards = grid.find_all('div', class_=re.compile(r'ds-relative.*ds-flex-row.*ds-space-x-4'))
    print(f'Cards in grid: {len(cards)}')
    for card in cards:
        a_tag = card.find('a', href=re.compile(r'/cricketers/'))
        if not a_tag:
            continue
        href = a_tag['href']
        # Find player name link (usually has text)
        name_links = [a.get_text(strip=True) for a in card.find_all('a') if a.get_text(strip=True)]
        pname = name_links[0] if name_links else ''
        m = re.search(r'/cricketers/.*?(\d+)$', href)
        pid = m.group(1) if m else ''
        card_text = card.get_text(separator=' | ', strip=True)
        squad_players.append({
            'name': pname,
            'id': pid,
            'href': href,
            'text': card_text
        })

print(f'\nTotal verified players in Rajasthan Royals squad: {len(squad_players)}')
for p in squad_players:
    print('  *', p['name'], f"(ID: {p['id']})")

# Verify if Virat Kohli is in RR squad:
print('Is Virat Kohli in RR squad?', any('Kohli' in p['name'] for p in squad_players))

