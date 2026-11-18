import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Set styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Arial'
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['figure.dpi'] = 300

fig_dir = 'rr-submission/v4/stage5_deliverables/figures'
os.makedirs(fig_dir, exist_ok=True)

df_bat = pd.read_csv('rr-submission/v4/stage5_deliverables/top10_batters_v4.csv')
df_bowl = pd.read_csv('rr-submission/v4/stage5_deliverables/top10_bowlers_v4.csv')
active_bat = pd.read_csv('rr-submission/v4/stage4_consistency_scoring/active_batters_v4_master.csv')
active_bowl = pd.read_csv('rr-submission/v4/stage4_consistency_scoring/active_bowlers_v4_master.csv')

# Colors
RR_PINK = '#E91E63'
RR_BLUE = '#0D1B2A'
RR_GOLD = '#D4AF37'

# 1. Top 10 Batters CBPS Bar Chart
fig, ax = plt.subplots(figsize=(10, 6))
df_bat_sorted = df_bat.sort_values(by='cbps_score_v4', ascending=True)

colors = [RR_PINK if p == 'Jos Buttler' else ('#1E88E5' if p in ['Suryakumar Yadav', 'Shreyas Iyer', 'Naman Dhir'] else '#3949AB') 
          for p in df_bat_sorted['player_name']]

bars = ax.barh(df_bat_sorted['player_name'], df_bat_sorted['cbps_score_v4'], color=colors, height=0.65, edgecolor='black', linewidth=0.5)

for bar, score, sr, opp_sr, d_sr in zip(bars, df_bat_sorted['cbps_score_v4'], df_bat_sorted['hp_sr'], df_bat_sorted['hp_opp_sr'], df_bat_sorted['delta_sr_venue']):
    ax.text(score + 0.03, bar.get_y() + bar.get_height()/2, 
            f"+{score:.2f}  (Opp-SR: {opp_sr:.1f} | ΔVenue: +{d_sr:.1f})", 
            va='center', ha='left', fontsize=9, fontweight='bold', color='#1A237E')

ax.set_xlim(0, 1.95)
ax.set_xlabel('Composite Ball Pressure Score (CBPS v4 Z-Score Units)', fontsize=11, fontweight='bold', labelpad=10)
ax.set_title('Top 10 Active Batters Under Pressure (Model v4: Unified Contextual Architecture)\nCalibrated for Opposition Quality, Chase Asymmetry & Venue Pars', 
             fontsize=12, fontweight='bold', pad=15, color=RR_BLUE)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'top_10_batters_cbps.png'), dpi=300)
plt.close()

# 2. Top 10 Bowlers CBPS Bar Chart
fig, ax = plt.subplots(figsize=(10, 6))
df_bowl_sorted = df_bowl.sort_values(by='cbps_score_v4', ascending=True)

colors_bowl = ['#2E7D32' if p == 'Sunil Narine' else ('#00838F' if p in ['Matheesha Pathirana', 'Mitchell Santner', 'Jasprit Bumrah'] else '#1565C0')
               for p in df_bowl_sorted['player_name']]

bars = ax.barh(df_bowl_sorted['player_name'], df_bowl_sorted['cbps_score_v4'], color=colors_bowl, height=0.65, edgecolor='black', linewidth=0.5)

for bar, score, econ, wkt in zip(bars, df_bowl_sorted['cbps_score_v4'], df_bowl_sorted['hp_econ'], df_bowl_sorted['hp_wkt_rate']):
    ax.text(score + 0.03, bar.get_y() + bar.get_height()/2, 
            f"+{score:.2f}  (HP Econ: {econ:.2f} | Wkt%: {wkt:.1f}%)", 
            va='center', ha='left', fontsize=9, fontweight='bold', color='#1B5E20')

ax.set_xlim(0, 1.75)
ax.set_xlabel('Composite Ball Pressure Score (CBPS v4 Z-Score Units)', fontsize=11, fontweight='bold', labelpad=10)
ax.set_title('Top 10 Active Bowlers Under Pressure (Model v4: Unified Contextual Architecture)\nCalibrated for Wicket Quality, Venue Pars & Match Reliability', 
             fontsize=12, fontweight='bold', pad=15, color=RR_BLUE)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'top_10_bowlers_cbps.png'), dpi=300)
plt.close()

# 3. Batters Clutch Matrix: Venue Delta vs Baseline Delta
fig, ax = plt.subplots(figsize=(9, 7))
pool_bat = active_bat[active_bat['hp_balls'] >= 200]
top10_names = set(df_bat['player_name'])

scatter_bg = ax.scatter(pool_bat['delta_sr_baseline'], pool_bat['delta_sr_venue'], 
                        c='#CFD8DC', s=pool_bat['hp_balls']/3, alpha=0.6, edgecolors='none', label='Active Player Pool (N=50+)')

top10_data = pool_bat[pool_bat['player_name'].isin(top10_names)]
scatter_fg = ax.scatter(top10_data['delta_sr_baseline'], top10_data['delta_sr_venue'], 
                        c=RR_PINK, s=top10_data['hp_balls']/2.5, alpha=0.9, edgecolors='black', linewidth=1.2, label='Top 10 Active Clutch Batters')

for _, row in top10_data.iterrows():
    offset_x = 2
    offset_y = 1
    if row['player_name'] == 'Naman Dhir':
        offset_x = 2
        offset_y = 2
    elif row['player_name'] == 'Tim David':
        offset_x = -12
        offset_y = 2
    ax.annotate(row['player_name'], (row['delta_sr_baseline'] + offset_x, row['delta_sr_venue'] + offset_y),
                fontsize=8.5, fontweight='bold', color=RR_BLUE)

ax.axhline(0, color='grey', linestyle='--', linewidth=0.8)
ax.axvline(0, color='grey', linestyle='--', linewidth=0.8)
ax.set_xlabel('Baseline Acceleration (HP Opp-SR - Non-HP Strike Rate)', fontsize=11, fontweight='bold', labelpad=10)
ax.set_ylabel('Venue Par Outperformance (HP Opp-SR - Venue Par Strike Rate)', fontsize=11, fontweight='bold', labelpad=10)
ax.set_title('Batter Clutch Quadrant Analysis (Unified Model v4)\nBubble Size Proportional to High-Pressure Deliveries Faced', 
             fontsize=12, fontweight='bold', pad=15, color=RR_BLUE)
ax.legend(loc='upper left', frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'batter_clutch_matrix.png'), dpi=300)
plt.close()

# 4. Bowlers Clutch Matrix: Economy Suppression vs Wicket Threat
fig, ax = plt.subplots(figsize=(9, 7))
pool_bowl = active_bowl[active_bowl['hp_balls'] >= 200]
top10_bowl_names = set(df_bowl['player_name'])

scatter_bg_bowl = ax.scatter(pool_bowl['hp_wkt_rate'], pool_bowl['delta_econ_venue'], 
                             c='#CFD8DC', s=pool_bowl['hp_balls']/3, alpha=0.6, edgecolors='none', label='Active Player Pool')

top10_bowl_data = pool_bowl[pool_bowl['player_name'].isin(top10_bowl_names)]
scatter_fg_bowl = ax.scatter(top10_bowl_data['hp_wkt_rate'], top10_bowl_data['delta_econ_venue'], 
                             c='#00897B', s=top10_bowl_data['hp_balls']/2.5, alpha=0.9, edgecolors='black', linewidth=1.2, label='Top 10 Active Clutch Bowlers')

for _, row in top10_bowl_data.iterrows():
    offset_x = 0.3
    offset_y = 0.08
    if row['player_name'] == 'Sunil Narine':
        offset_y = -0.15
    ax.annotate(row['player_name'], (row['hp_wkt_rate'] + offset_x, row['delta_econ_venue'] + offset_y),
                fontsize=8.5, fontweight='bold', color=RR_BLUE)

ax.axhline(0, color='grey', linestyle='--', linewidth=0.8)
ax.set_xlabel('Quality-Weighted Wicket Rate (% per Ball)', fontsize=11, fontweight='bold', labelpad=10)
ax.set_ylabel('Venue Economy Suppression (Venue Par Econ - HP Econ)', fontsize=11, fontweight='bold', labelpad=10)
ax.set_title('Bowler Clutch Quadrant Analysis (Unified Model v4)\nBubble Size Proportional to High-Pressure Deliveries Bowled', 
             fontsize=12, fontweight='bold', pad=15, color=RR_BLUE)
ax.legend(loc='upper right', frameon=True)
plt.tight_layout()
plt.savefig(os.path.join(fig_dir, 'bowler_clutch_matrix.png'), dpi=300)
plt.close()

print('All 4 publication-grade figures successfully generated in v4.')

