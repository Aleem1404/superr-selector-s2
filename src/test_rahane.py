import requests
from bs4 import BeautifulSoup

url = 'https://stats.cricinfo.com/ci/engine/player/277916.html?class=6;template=results;type=allround'
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
soup = BeautifulSoup(r.text, 'lxml')

# Check text around player name
for tag in soup.find_all(['h1', 'h2', 'h3', 'b', 'p']):
    t = tag.get_text(strip=True)
    if 'Rahane' in t:
        print(f'{tag.name} ({tag.get("class")}): {t}')

