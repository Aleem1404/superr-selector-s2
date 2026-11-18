from curl_cffi import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.espncricinfo.com/series/ipl-2026-1510719/rajasthan-royals-squad-1511089/series-squads'
r = requests.get(url, impersonate='chrome120')
soup = BeautifulSoup(r.text, 'lxml')

# Find all headings h1, h2, h3, h4 on the page
for h in soup.find_all(['h1', 'h2', 'h3', 'h4', 'span']):
    t = h.get_text(strip=True)
    if any(k in t.lower() for k in ['squad', 'most runs', 'most wickets', 'top performers', 'key stats', 'recent', 'stats']):
        print(f'{h.name}: {t}')

