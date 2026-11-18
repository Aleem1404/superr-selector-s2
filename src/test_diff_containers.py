from curl_cffi import requests
from bs4 import BeautifulSoup
import re

url = 'https://www.espncricinfo.com/series/ipl-2026-1510719/rajasthan-royals-squad-1511089/series-squads'
r = requests.get(url, impersonate='chrome120')
soup = BeautifulSoup(r.text, 'lxml')

# Find Riyan Parag (who is definitely in RR)
rp_a = soup.find('a', href=re.compile(r'/cricketers/.*1079434'))
print('Riyan Parag tag:', rp_a)

# Find Virat Kohli (who is in RCB, but appeared in sidebar)
vk_a = soup.find('a', href=re.compile(r'/cricketers/.*253802'))
print('Virat Kohli tag:', vk_a)

# Let's inspect the ancestors of Riyan Parag vs Virat Kohli
rp_ancestors = [p for p in rp_a.parents if p.name == 'div']
vk_ancestors = [p for p in vk_a.parents if p.name == 'div']

print('Riyan Parag ancestor classes (first 5):')
for i, a in enumerate(rp_ancestors[:5]):
    print(f'  {i}: {a.get("class")}')

print('Virat Kohli ancestor classes (first 5):')
for i, a in enumerate(vk_ancestors[:5]):
    print(f'  {i}: {a.get("class")}')

