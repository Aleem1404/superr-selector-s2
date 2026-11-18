from curl_cffi import requests
from bs4 import BeautifulSoup

urls = [
    'https://www.iplt20.com/news/article/mohd-shami-and-m-siddharth-traded-to-rajasthan-royals-sam-curran-traded-to-lucknow-super-giants',
    'https://www.iplt20.com/news/article/harshal-patel-traded-to-gujarat-titans-from-sunrisers-hyderabad',
    'https://www.iplt20.com/news/article/tata-ipl-2027-player-retentions-announced'
]

for url in urls:
    r = requests.get(url, impersonate='chrome120')
    soup = BeautifulSoup(r.text, 'lxml')
    print('========================================')
    print('URL:', url)
    h1 = soup.find('h1')
    print('H1:', h1.get_text(strip=True) if h1 else None)
    ps = [p.get_text(strip=True) for p in soup.find_all('p') if len(p.get_text(strip=True)) > 20]
    for p in ps:
        if not p.startswith('© IPL') and not 'TATA IPL Fan Parks' in p:
            print('  *', p)
    print()

