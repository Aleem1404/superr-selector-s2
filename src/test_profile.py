import urllib.request
from bs4 import BeautifulSoup
import json

url = 'https://stats.cricinfo.com/ci/content/player/277916.html'
req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})

try:
    with urllib.request.urlopen(req, timeout=15) as resp:
        final_url = resp.geturl()
        html = resp.read().decode('utf-8', errors='ignore')
        print('Final URL:', final_url)
        print('HTML length:', len(html))
        
        soup = BeautifulSoup(html, 'lxml')
        
        # Check classic layout or modern layout
        # Classic layout often has p.ciPlayerinformationtxt
        player_info = {}
        for p in soup.find_all('p', class_='ciPlayerinformationtxt'):
            b = p.find('b')
            span = p.find('span')
            if b and span:
                player_info[b.get_text(strip=True)] = span.get_text(strip=True)
            elif b:
                player_info[b.get_text(strip=True)] = p.get_text(strip=True).replace(b.get_text(strip=True), '').strip()
                
        print('Classic player info:', player_info)
        
        # If modern layout, check next_data or specific containers
        if not player_info:
            print('Trying modern cricinfo layout...')
            # check title or h1
            h1 = soup.find('h1')
            print('H1:', h1.get_text(strip=True) if h1 else None)
            # check script with __NEXT_DATA__
            next_data = soup.find('script', id='__NEXT_DATA__')
            if next_data:
                data = json.loads(next_data.string)
                print('Found __NEXT_DATA__ keys:', list(data.keys()))
except Exception as e:
    print('Error:', e)

