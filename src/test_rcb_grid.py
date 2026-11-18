from curl_cffi import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.espncricinfo.com/series/ipl-2026-1510719/royal-challengers-bengaluru-squad-1511134/series-squads'
r = requests.get(url, impersonate='chrome120')
soup = BeautifulSoup(r.text, 'lxml')

squad_grids = soup.find_all('div', class_=re.compile(r'ds-grid.*lg:ds-grid-cols-2'))
print(f'Squad grids found: {len(squad_grids)}')

squad_players = []
for grid in squad_grids:
    cards = grid.find_all('div', class_=re.compile(r'ds-relative.*ds-flex-row.*ds-space-x-4'))
    for card in cards:
        a_tag = card.find('a', href=re.compile(r'/cricketers/'))
        if not a_tag:
            continue
        href = a_tag['href']
        name_links = [a.get_text(strip=True) for a in card.find_all('a') if a.get_text(strip=True)]
        pname = name_links[0] if name_links else ''
        m = re.search(r'/cricketers/.*?(\d+)$', href)
        pid = m.group(1) if m else ''
        squad_players.append({'name': pname, 'id': pid})

print(f'Total players in RCB squad: {len(squad_players)}')
for p in squad_players:
    print('  *', p['name'])

print('Is Virat Kohli in RCB squad?', any('Kohli' in p['name'] for p in squad_players))
print('Is Vaibhav Sooryavanshi in RCB squad?', any('Sooryavanshi' in p['name'] for p in squad_players))

