import requests
from bs4 import BeautifulSoup

session = requests.Session()
session.headers.update({
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'
})

test_urls = [
    'https://stats.cricinfo.com/ci/engine/player/277916.html',
    'https://stats.cricinfo.com/ci/engine/player/277916.html?template=results;type=batting;class=6',
    'https://stats.cricinfo.com/ci/engine/player/277916.html?class=6;template=results;type=allround',
]

for url in test_urls:
    r = session.get(url, allow_redirects=False)
    print(f'URL: {url} -> Status: {r.status_code}, Location: {r.headers.get("Location")}')
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'lxml')
        h1 = soup.find('h1')
        print('  Title/H1:', h1.get_text(strip=True) if h1 else soup.title.string)

