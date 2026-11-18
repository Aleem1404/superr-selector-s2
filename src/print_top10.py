import pandas as pd

batters = pd.read_csv('output/top_batters_under_pressure.csv')
bowlers = pd.read_csv('output/top_bowlers_under_pressure.csv')
mapping = pd.read_csv('data/competition_team_player_mapping.csv')
pak_teams = set(mapping[mapping['team_name'].str.contains('Pakistan', na=False)]['player_name'].unique())

bat_top = batters[(batters['hp_balls'] >= 200) & (~batters['striker_name'].isin(pak_teams))].head(10).copy()
bat_top['rank'] = range(1, 11)

bowl_top = bowlers[(bowlers['hp_balls'] >= 200) & (~bowlers['bowler_name'].isin(pak_teams))].head(10).copy()
bowl_top['rank'] = range(1, 11)

print('=== FINAL TOP 10 BATTERS ===')
for _, r in bat_top.iterrows():
    print(f"{r['rank']}. {r['striker_name']} | HP Balls: {int(r['hp_balls'])} | HP SR: {r['raw_hp_sr']:.1f} | Base SR: {r['base_sr']:.1f} | Delta SR: +{r['delta_sr']:.1f} | Dot%: {r['raw_hp_dot_pct']:.1f}% | Consistency: {r['consistency_rate']*100:.1f}% | Score: {r['cbps']:.2f}")

print('\n=== FINAL TOP 10 BOWLERS ===')
for _, r in bowl_top.iterrows():
    print(f"{r['rank']}. {r['bowler_name']} | HP Balls: {int(r['hp_balls'])} | HP Econ: {r['raw_hp_econ']:.2f} | Base Econ: {r['base_econ']:.2f} | Delta Econ: {r['delta_econ']:+.2f} | Wkt Rate: {r['raw_hp_wkt_rate']:.1f}% | Dot%: {r['raw_hp_dot_pct']:.1f}% | Consistency: {r['consistency_rate']*100:.1f}% | Score: {r['cbps']:.2f}")

