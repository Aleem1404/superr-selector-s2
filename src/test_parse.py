from bs4 import BeautifulSoup

with open('cricinfo_results.html', 'r', encoding='utf-8') as f:
    soup = BeautifulSoup(f.read(), 'lxml')

tables = soup.find_all('table', class_='engineTable')
table = tables[2]
all_trs = table.find_all('tr')
print(f'Total trs in table 2: {len(all_trs)}')
for i, tr in enumerate(all_trs[:8]):
    print(f'tr {i}: class={tr.get("class")}, tds={len(tr.find_all("td"))}, ths={len(tr.find_all("th"))}')
    print('   sample:', [td.get_text(strip=True) for td in tr.find_all(['td', 'th'])][:6])

