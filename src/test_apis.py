import requests

player_id = '277916'
api_urls = [
    f'https://hs-consumer-api.espncricinfo.com/v1/pages/player/home?playerId={player_id}',
    f'https://core.espnuk.org/v2/sports/cricket/athletes/{player_id}',
    f'https://site.api.espn.com/apis/site/v2/sports/cricket/athletes/{player_id}',
    f'https://site.web.api.espn.com/apis/common/v3/sports/cricket/athletes/{player_id}',
    f'https://stats.cricinfo.com/ci/content/player/caps/{player_id}.html',
]

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}

for url in api_urls:
    try:
        r = requests.get(url, headers=headers, timeout=10)
        print(f'{url} -> {r.status_code}, Length: {len(r.text)}')
        if r.status_code == 200:
            print('  Sample:', r.text[:300])
    except Exception as e:
        print(f'{url} -> Error: {e}')

