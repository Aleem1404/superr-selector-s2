import requests
import json

player_id = '277916'
url = f'https://site.web.api.espn.com/apis/common/v3/sports/cricket/athletes/{player_id}'
r = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
data = r.json()

athlete = data.get('athlete', {})
print('Keys in athlete:', list(athlete.keys()))
print('ID:', athlete.get('id'))
print('Full Name:', athlete.get('fullName'))
print('Display Name:', athlete.get('displayName'))
print('Short Name:', athlete.get('shortName'))
print('Date of Birth:', athlete.get('dateOfBirth'))
print('Gender:', athlete.get('gender'))
print('Batting Style:', athlete.get('battingStyle'))
print('Bowling Style:', athlete.get('bowlingStyle'))
print('Positions:', athlete.get('positions'))
print('Birth Place:', athlete.get('birthPlace'))
print('Citizenship:', athlete.get('citizenship'))
print('Headshot URL:', athlete.get('headshot', {}).get('href'))

