import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Referer': 'https://stats.cricinfo.com/',
}

session = requests.Session()
session.headers.update(headers)

# Test 1: classic URL
r1 = session.get('https://stats.cricinfo.com/ci/content/player/277916.html', allow_redirects=True)
print('Test 1 status:', r1.status_code, 'Final URL:', r1.url)

# Test 2: mobile / engine / API if needed
r2 = session.get('https://www.espncricinfo.com/cricketers/ajinkya-rahane-277916')
print('Test 2 status:', r2.status_code, 'Final URL:', r2.url)

