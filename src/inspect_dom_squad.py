from curl_cffi import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.espncricinfo.com/series/ipl-2026-1510719/rajasthan-royals-squad-1511089/series-squads'
r = requests.get(url, impersonate='chrome120')
soup = BeautifulSoup(r.text, 'lxml')

for a in soup.find_all('a', href=re.compile(r'/cricketers/.*253802')):
    curr = a
    for i in range(12):
        if curr.parent:
            curr = curr.parent
            print(f'Level {i}: tag={curr.name}, class={curr.get("class")}')
            h = curr.find(['h1', 'h2', 'h3', 'h4'])
            if h:
                print('   Heading in container:', h.get_text(strip=True))
    break

