from curl_cffi import requests
from bs4 import BeautifulSoup
import json

trade_articles = [
    '/news/article/hardik-pandya-and-arshdeep-singh-complete-major-trade-between-pbks-and-mi',
    '/news/article/csk-and-srh-agree-to-four-player-trade',
    '/news/article/t-natarajan-returns-to-sunrisers-hyderabad-zeeshan-ansari-moves-to-delhi-capitals',
    '/news/article/rishabh-pant-and-kuldeep-yadav-complete-high-profile-trade-between-dc-and-lsg',
]

for path in trade_articles:
    url = f'https://www.iplt20.com{path}'
    r = requests.get(url, impersonate='chrome120')
    soup = BeautifulSoup(r.text, 'lxml')
    h1 = soup.find('h1')
    title = h1.get_text(strip=True) if h1 else 'No title'
    # Find article body or paragraphs
    ps = [p.get_text(strip=True) for p in soup.find_all('p') if len(p.get_text(strip=True)) > 20]
    print('====================================')
    print('URL:', url)
    print('TITLE:', title)
    print('BODY PARAGRAPHS:')
    for p in ps:
        print('  *', p)
    print()

