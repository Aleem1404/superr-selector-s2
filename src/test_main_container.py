from curl_cffi import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.espncricinfo.com/series/ipl-2026-1510719/rajasthan-royals-squad-1511089/series-squads'
r = requests.get(url, impersonate='chrome120')
soup = BeautifulSoup(r.text, 'lxml')

h1 = soup.find('h1')
print('H1:', h1)

# Find the main column container
# Usually under h1, there is a container of player cards
main_container = h1.find_parent('div', class_=re.compile(r'ds-grow|ds-w-full|ds-flex-1', re.I)) or h1.find_parent('div')
print('Main container tag:', main_container.name, 'class:', main_container.get('class'))

players_in_main = []
for a in main_container.find_all('a', href=re.compile(r'/cricketers/')):
    href = a['href']
    name = a.get_text(strip=True)
    if name and href not in [p['href'] for p in players_in_main]:
        players_in_main.append({'name': name, 'href': href})

print(f'Total players in MAIN SQUAD container: {len(players_in_main)}')
for p in players_in_main:
    print('  *', p['name'], p['href'])

