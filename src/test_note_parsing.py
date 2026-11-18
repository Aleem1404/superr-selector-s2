import requests
from bs4 import BeautifulSoup
import re

url = 'https://stats.cricinfo.com/ci/engine/stats/index.html?class=6;filter=advanced;ground=2865;ground=664;orderby=runs;page=1;size=200;spanmax1=2026;spanmin1=2008;spanval1=span;template=results;type=batting'
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
soup = BeautifulSoup(r.text, 'lxml')
table = soup.find_all('table', class_='engineTable')[2]

trs = table.find_all('tr')
records = []
current_player = None

for tr in trs:
    cl = tr.get('class')
    if cl == ['data2']:
        tds = tr.find_all('td')
        if len(tds) >= 15:
            a_tag = tds[0].find('a')
            name = tds[0].get_text(strip=True)
            href = a_tag['href'] if a_tag else ''
            m = re.search(r'/player/(\d+)\.html', href)
            pid = m.group(1) if m else ''
            current_player = {
                'id': pid,
                'name': name,
                'runs': tds[5].get_text(strip=True),
                'teams': ''
            }
            records.append(current_player)
    elif cl == ['note'] and current_player is not None:
        note_text = tr.get_text(strip=True).strip('()')
        current_player['teams'] = note_text

print(f'Parsed {len(records)} records from page 1.')
print('Sample records with teams:')
for rec in records[:5]:
    print(rec)

