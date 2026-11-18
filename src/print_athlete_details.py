import requests
import json

url = 'https://site.web.api.espn.com/apis/common/v3/sports/cricket/athletes/277916'
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
athlete = r.json().get('athlete', {})
for k, v in athlete.items():
    if k not in ['links']:
        print(f'{k}: {v}')

