import requests

series_id = '1510719'

urls = [
    f'https://site.web.api.espn.com/apis/site/v2/sports/cricket/leagues/ipl/teams',
    f'https://site.web.api.espn.com/apis/site/v2/sports/cricket/series/{series_id}/teams',
    f'https://site.api.espn.com/apis/site/v2/sports/cricket/series/{series_id}/teams',
    f'https://site.web.api.espn.com/apis/common/v3/sports/cricket/leagues/{series_id}/teams',
    f'https://site.web.api.espn.com/apis/site/v2/sports/cricket/series/{series_id}',
    f'https://site.api.espn.com/apis/site/v2/sports/cricket/series/{series_id}',
    f'https://hs-consumer-api.espncricinfo.com/v1/pages/series/squads?lang=en&seriesId={series_id}',
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

for u in urls:
    try:
        r = requests.get(u, headers=headers, timeout=5)
        print(f'{u} -> {r.status_code}, len={len(r.text)}')
        if r.status_code == 200:
            print('   sample:', r.text[:200])
    except Exception as e:
        print(f'{u} -> error: {e}')

