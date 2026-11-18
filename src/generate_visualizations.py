import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

os.makedirs('output/figures', exist_ok=True)

# Set clean aesthetic styling
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.sans-serif'] = 'Helvetica, Arial, DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#cccccc'
plt.rcParams['axes.linewidth'] = 0.8

# Load pipeline outputs
batters = pd.read_csv('output/top_batters_under_pressure.csv')
bowlers = pd.read_csv('output/top_bowlers_under_pressure.csv')
mapping = pd.read_csv('data/competition_team_player_mapping.csv')
pak_teams = set(mapping[mapping['team_name'].str.contains('Pakistan', na=False)]['player_name'].unique())

# Filter for >= 200 HP balls and auction-actionable players
bat_top = batters[(batters['hp_balls'] >= 200) & (~batters['striker_name'].isin(pak_teams))].head(10).copy()
bat_top['rank'] = range(1, 11)

bowl_top = bowlers[(bowlers['hp_balls'] >= 200) & (~bowlers['bowler_name'].isin(pak_teams))].head(10).copy()
bowl_top['rank'] = range(1, 11)

# --- FIGURE 1: TOP 10 BATTERS UNDER PRESSURE ---
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
colors = ['#E4007C' if r <= 3 else '#1E398A' for r in bat_top['rank']]
bars = ax.barh(bat_top['striker_name'][::-1], bat_top['cbps'][::-1], color=colors[::-1], height=0.65)

ax.set_title("Rajasthan Royals SupeRR Selector: Top 10 Batters Under Pressure", fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel("Composite Batter Pressure Score (CBPS)", fontsize=11, labelpad=10)
ax.grid(axis='y', linestyle='', alpha=0.3)
ax.grid(axis='x', linestyle='--', alpha=0.7)

# Add data callouts on bars
for bar in bars:
    w = bar.get_width()
    ax.text(w + 0.03, bar.get_y() + bar.get_height()/2, f'{w:.2f}', va='center', ha='left', fontsize=9, fontweight='bold', color='#333333')

plt.tight_layout()
plt.savefig('output/figures/top_10_batters_cbps.png')
plt.close()

# --- FIGURE 2: TOP 10 BOWLERS UNDER PRESSURE ---
fig, ax = plt.subplots(figsize=(10, 6), dpi=300)
colors = ['#E4007C' if r <= 3 else '#1E398A' for r in bowl_top['rank']]
bars = ax.barh(bowl_top['bowler_name'][::-1], bowl_top['cbps'][::-1], color=colors[::-1], height=0.65)

ax.set_title("Rajasthan Royals SupeRR Selector: Top 10 Bowlers Under Pressure", fontsize=14, fontweight='bold', pad=15)
ax.set_xlabel("Composite Bowler Pressure Score (CBPS)", fontsize=11, labelpad=10)
ax.grid(axis='y', linestyle='', alpha=0.3)
ax.grid(axis='x', linestyle='--', alpha=0.7)

for bar in bars:
    w = bar.get_width()
    ax.text(w + 0.03, bar.get_y() + bar.get_height()/2, f'{w:.2f}', va='center', ha='left', fontsize=9, fontweight='bold', color='#333333')

plt.tight_layout()
plt.savefig('output/figures/top_10_bowlers_cbps.png')
plt.close()

# --- FIGURE 3: BATTER CLUTCH QUADRANT (Delta SR vs Dot Ball % Under Pressure) ---
fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
sub_bat = batters[(batters['hp_balls'] >= 180) & (~batters['striker_name'].isin(pak_teams))].copy()

scatter = ax.scatter(sub_bat['raw_hp_dot_pct'], sub_bat['delta_sr'], s=sub_bat['hp_balls']*0.5, c=sub_bat['cbps'], cmap='viridis', alpha=0.85, edgecolors='black', linewidth=0.5)
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Composite Pressure Score (CBPS)', rotation=270, labelpad=15)

# Label top performers
for _, row in bat_top.head(8).iterrows():
    ax.annotate(row['striker_name'], (row['raw_hp_dot_pct'], row['delta_sr']), 
                xytext=(5, 5), textcoords='offset points', fontsize=9, fontweight='bold')

ax.axhline(0, color='gray', linestyle='--', alpha=0.6)
ax.axvline(36, color='gray', linestyle='--', alpha=0.6)
ax.set_xlabel('Dot Ball % Under Pressure (Lower is Better)', fontsize=11, labelpad=10)
ax.set_ylabel('Delta Strike Rate (Pressure SR - Baseline SR)', fontsize=11, labelpad=10)
ax.set_title('Clutch Hitting Matrix: Delta Strike Rate vs Dot Ball Resistance', fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('output/figures/batter_clutch_matrix.png')
plt.close()

# --- FIGURE 4: BOWLER CLUTCH QUADRANT (Pressure Economy vs Pressure Wicket Rate) ---
fig, ax = plt.subplots(figsize=(10, 7), dpi=300)
sub_bowl = bowlers[(bowlers['hp_balls'] >= 180) & (~bowlers['bowler_name'].isin(pak_teams))].copy()

scatter = ax.scatter(sub_bowl['raw_hp_econ'], sub_bowl['raw_hp_wkt_rate'], s=sub_bowl['hp_balls']*0.4, c=sub_bowl['cbps'], cmap='plasma', alpha=0.85, edgecolors='black', linewidth=0.5)
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Composite Pressure Score (CBPS)', rotation=270, labelpad=15)

for _, row in bowl_top.head(8).iterrows():
    ax.annotate(row['bowler_name'], (row['raw_hp_econ'], row['raw_hp_wkt_rate']), 
                xytext=(5, 5), textcoords='offset points', fontsize=9, fontweight='bold')

ax.axvline(9.2, color='gray', linestyle='--', alpha=0.6)
ax.axhline(7.0, color='gray', linestyle='--', alpha=0.6)
ax.set_xlabel('Economy Rate Under High Pressure (Lower is Better)', fontsize=11, labelpad=10)
ax.set_ylabel('Wicket-Taking Rate % Under High Pressure (Higher is Better)', fontsize=11, labelpad=10)
ax.set_title('Clutch Bowling Matrix: Pressure Economy vs Wicket Threat', fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('output/figures/bowler_clutch_matrix.png')
plt.close()

print("Generated all publication figures in output/figures/")

