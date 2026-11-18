import pandas as pd
import json
import os

def build_dashboard():
    print("=" * 60)
    print("STAGE 5: Building Interactive Standalone Web Dashboard")
    print("=" * 60)
    
    # Load Stage 4 data
    bat_csv = 'rr-submission/stage4_consistency_scoring/ranked_batters_master.csv'
    bowl_csv = 'rr-submission/stage4_consistency_scoring/ranked_bowlers_master.csv'
    top_bat_csv = 'rr-submission/stage4_consistency_scoring/top10_batters_final.csv'
    top_bowl_csv = 'rr-submission/stage4_consistency_scoring/top10_bowlers_final.csv'
    trades_csv = 'IPL-2027-trades.csv'
    retentions_csv = 'cricinfo-data/IPL-2027-retentions/all_ipl_2027_retentions.csv'
    purses_csv = 'cricinfo-data/IPL-2027-retentions/ipl_2027_team_purses_and_slots.csv'
    
    df_bat = pd.read_csv(bat_csv)
    df_bowl = pd.read_csv(bowl_csv)
    df_top_bat = pd.read_csv(top_bat_csv)
    df_top_bowl = pd.read_csv(top_bowl_csv)
    df_trades = pd.read_csv(trades_csv) if os.path.exists(trades_csv) else pd.DataFrame()
    df_ret = pd.read_csv(retentions_csv) if os.path.exists(retentions_csv) else pd.DataFrame()
    df_purses = pd.read_csv(purses_csv) if os.path.exists(purses_csv) else pd.DataFrame()
    
    # Filter out Pakistan players for IPL eligibility benchmark
    mapping = pd.read_csv('data/competition_team_player_mapping.csv')
    pak_players = set(mapping[mapping['team_name'].str.contains('Pakistan', na=False)]['player_name'].unique())
    
    df_bat_ipl = df_bat[~df_bat['player_name'].isin(pak_players)].copy().reset_index(drop=True)
    df_bat_ipl['ipl_rank'] = df_bat_ipl.index + 1
    
    df_bowl_ipl = df_bowl[~df_bowl['player_name'].isin(pak_players)].copy().reset_index(drop=True)
    df_bowl_ipl['ipl_rank'] = df_bowl_ipl.index + 1
    
    top10_bat_list = df_bat_ipl.head(10).to_dict(orient='records')
    top10_bowl_list = df_bowl_ipl.head(10).to_dict(orient='records')
    all_bat_list = df_bat_ipl.head(50).to_dict(orient='records')
    all_bowl_list = df_bowl_ipl.head(50).to_dict(orient='records')
    trades_list = df_trades.to_dict(orient='records') if not df_trades.empty else []
    purses_list = df_purses.to_dict(orient='records') if not df_purses.empty else []
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rajasthan Royals SupeRR Selector Season 2 | Pressure Model Dashboard</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Plotly JS CDN -->
    <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
    <!-- Lucide Icons CDN -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #0b1120;
            color: #f1f5f9;
        }}
        .rr-pink {{ color: #e4007c; }}
        .bg-rr-pink {{ background-color: #e4007c; }}
        .bg-rr-navy {{ background-color: #001d48; }}
        .border-rr-pink {{ border-color: #e4007c; }}
        .glass-card {{
            background: rgba(15, 23, 42, 0.75);
            backdrop-filter: blur(12px);
            border: 1px solid rgba(255, 255, 255, 0.08);
        }}
        .tab-btn.active {{
            background-color: #e4007c;
            color: white;
            box-shadow: 0 4px 14px 0 rgba(228, 0, 124, 0.39);
        }}
    </style>
</head>
<body class="min-h-screen flex flex-col">

    <!-- Top Header -->
    <header class="border-b border-slate-800 bg-slate-950/80 sticky top-0 z-50 backdrop-blur-md">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex flex-wrap justify-between items-center gap-4">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-pink-600 to-indigo-900 flex items-center justify-center font-bold text-white shadow-lg">
                    RR
                </div>
                <div>
                    <h1 class="text-lg font-bold text-white flex items-center gap-2">
                        SupeRR Selector Season 2 
                        <span class="text-xs px-2 py-0.5 rounded-full bg-pink-500/20 text-pink-400 border border-pink-500/30 font-medium">Round 1</span>
                    </h1>
                    <p class="text-xs text-slate-400">High-Pressure Performance Modeling & Dynamic Leverage Index</p>
                </div>
            </div>
            
            <div class="flex items-center space-x-3 text-xs text-slate-300">
                <div class="bg-slate-900 border border-slate-800 px-3 py-1.5 rounded-lg flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                    <span>Candidate: <b class="text-white">Mohammed Aleem Bukkapatnam</b> (M.S. in AI)</span>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-1 w-full space-y-6">

        <!-- KPI Summary Ribbon -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div class="glass-card rounded-2xl p-4 border border-slate-800/80 shadow-sm">
                <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Total Deliveries</p>
                <p class="text-2xl font-extrabold text-white mt-1">200,999</p>
                <p class="text-[11px] text-slate-500 mt-0.5">867 Matches (IPL & T20I)</p>
            </div>
            <div class="glass-card rounded-2xl p-4 border border-slate-800/80 shadow-sm">
                <p class="text-xs font-semibold text-pink-400 uppercase tracking-wider">High-Pressure Balls</p>
                <p class="text-2xl font-extrabold text-pink-400 mt-1">58,447</p>
                <p class="text-[11px] text-slate-500 mt-0.5">29.08% Leverage Threshold (PI &ge; 0.60)</p>
            </div>
            <div class="glass-card rounded-2xl p-4 border border-slate-800/80 shadow-sm">
                <p class="text-xs font-semibold text-indigo-400 uppercase tracking-wider">Eligible Sample Pool</p>
                <p class="text-2xl font-extrabold text-indigo-400 mt-1">217 Players</p>
                <p class="text-[11px] text-slate-500 mt-0.5">&ge; 150 HP Deliveries Tracked</p>
            </div>
            <div class="glass-card rounded-2xl p-4 border border-slate-800/80 shadow-sm">
                <p class="text-xs font-semibold text-amber-400 uppercase tracking-wider">Model Validation</p>
                <p class="text-2xl font-extrabold text-amber-400 mt-1">r = 0.89</p>
                <p class="text-[11px] text-slate-500 mt-0.5">Split-Half Reliability Metric</p>
            </div>
        </div>

        <!-- Navigation Tabs -->
        <div class="flex flex-wrap gap-2 border-b border-slate-800 pb-2">
            <button onclick="switchTab('batters')" id="tab-btn-batters" class="tab-btn active px-4 py-2 rounded-xl text-xs font-semibold transition-all">
                Top 10 Batters
            </button>
            <button onclick="switchTab('bowlers')" id="tab-btn-bowlers" class="tab-btn px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white transition-all">
                Top 10 Bowlers
            </button>
            <button onclick="switchTab('visuals')" id="tab-btn-visuals" class="tab-btn px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white transition-all">
                Interactive Clutch Matrices
            </button>
            <button onclick="switchTab('methodology')" id="tab-btn-methodology" class="tab-btn px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white transition-all">
                Methodology & Mathematical Formulas
            </button>
            <button onclick="switchTab('retentions')" id="tab-btn-retentions" class="tab-btn px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white transition-all">
                IPL 2027 Retentions & Trades (184 Players)
            </button>
        </div>

        <!-- TAB 1: BATTERS -->
        <div id="tab-batters" class="tab-content space-y-4">
            <div class="flex flex-wrap justify-between items-center gap-2">
                <div>
                    <h2 class="text-base font-bold text-white">Top 10 Batters Under High Pressure</h2>
                    <p class="text-xs text-slate-400">Scored via Composite Batter Pressure Score (CBPS): 30% Shrunk SR + 25% &Delta;SR + 20% Dot Suppression + 15% Boundary % + 10% Consistency</p>
                </div>
                <div class="text-xs text-pink-400 font-medium bg-pink-500/10 px-3 py-1 rounded-lg border border-pink-500/20">
                    Official Unstop Dropdown Selections
                </div>
            </div>

            <div class="glass-card rounded-2xl overflow-hidden border border-slate-800">
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs">
                        <thead class="bg-slate-900/90 text-slate-400 uppercase tracking-wider text-[10px] border-b border-slate-800">
                            <tr>
                                <th class="py-3 px-4 text-center">Rank</th>
                                <th class="py-3 px-4">Player Name</th>
                                <th class="py-3 px-4 text-center">HP Balls</th>
                                <th class="py-3 px-4 text-center">HP Strike Rate</th>
                                <th class="py-3 px-4 text-center">Base Strike Rate</th>
                                <th class="py-3 px-4 text-center">&Delta; SR Elevation</th>
                                <th class="py-3 px-4 text-center">HP Dot Ball %</th>
                                <th class="py-3 px-4 text-center">Match Consistency</th>
                                <th class="py-3 px-4 text-center">CBPS Score</th>
                            </tr>
                        </thead>
                        <tbody id="batters-tbody" class="divide-y divide-slate-800/60 font-mono text-slate-300">
                            <!-- Injected via JS -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB 2: BOWLERS -->
        <div id="tab-bowlers" class="tab-content hidden space-y-4">
            <div class="flex flex-wrap justify-between items-center gap-2">
                <div>
                    <h2 class="text-base font-bold text-white">Top 10 Bowlers Under High Pressure</h2>
                    <p class="text-xs text-slate-400">Scored via Composite Bowler Pressure Score (CBPS): 30% Economy Suppression + 25% Wicket Threat + 15% Dot Pressure + 15% Boundary Suppression + 15% Consistency</p>
                </div>
                <div class="text-xs text-indigo-400 font-medium bg-indigo-500/10 px-3 py-1 rounded-lg border border-indigo-500/20">
                    Official Unstop Dropdown Selections
                </div>
            </div>

            <div class="glass-card rounded-2xl overflow-hidden border border-slate-800">
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs">
                        <thead class="bg-slate-900/90 text-slate-400 uppercase tracking-wider text-[10px] border-b border-slate-800">
                            <tr>
                                <th class="py-3 px-4 text-center">Rank</th>
                                <th class="py-3 px-4">Player Name</th>
                                <th class="py-3 px-4 text-center">HP Balls</th>
                                <th class="py-3 px-4 text-center">HP Economy</th>
                                <th class="py-3 px-4 text-center">Base Economy</th>
                                <th class="py-3 px-4 text-center">&Delta; Economy (Tighter)</th>
                                <th class="py-3 px-4 text-center">Wicket Threat %</th>
                                <th class="py-3 px-4 text-center">Match Reliability</th>
                                <th class="py-3 px-4 text-center">CBPS Score</th>
                            </tr>
                        </thead>
                        <tbody id="bowlers-tbody" class="divide-y divide-slate-800/60 font-mono text-slate-300">
                            <!-- Injected via JS -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB 3: VISUALIZATIONS -->
        <div id="tab-visuals" class="tab-content hidden space-y-6">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="glass-card rounded-2xl p-4 border border-slate-800">
                    <h3 class="text-sm font-bold text-white mb-2">Batter Clutch Matrix: &Delta; Strike Rate vs Dot Ball %</h3>
                    <p class="text-xs text-slate-400 mb-4">Top-right quadrant indicates elite boundary elevation combined with dot ball reduction.</p>
                    <div id="plotly-batters" class="w-full h-80"></div>
                </div>

                <div class="glass-card rounded-2xl p-4 border border-slate-800">
                    <h3 class="text-sm font-bold text-white mb-2">Bowler Clutch Matrix: Economy Suppression vs Wicket Threat</h3>
                    <p class="text-xs text-slate-400 mb-4">Top-left indicates supreme high-leverage execution (sub-7.5 economy & high wicket rate).</p>
                    <div id="plotly-bowlers" class="w-full h-80"></div>
                </div>
            </div>
        </div>

        <!-- TAB 4: METHODOLOGY -->
        <div id="tab-methodology" class="tab-content hidden space-y-6">
            <div class="glass-card rounded-2xl p-6 border border-slate-800 space-y-6 text-sm text-slate-300">
                <div>
                    <h3 class="text-lg font-bold text-white mb-2 flex items-center gap-2">
                        <span class="w-2.5 h-2.5 rounded-full bg-pink-500"></span>
                        1. Mathematical Definition of Pressure: Dynamic Leverage Index (PI)
                    </h3>
                    <p class="text-xs leading-relaxed text-slate-400 mb-3">
                        Pressure is calculated ball-by-ball ($PI_t \in [0, 1]$) based on match architecture rather than arbitrary over cutoffs:
                    </p>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-800 font-mono text-xs text-slate-200">
                            <b class="text-pink-400">Innings 2 (The Chase):</b><br><br>
                            &bull; <i>U<sub>RRR</sub></i> = 1 / (1 + e<sup>-0.5 &times; (RRR - 9.0)</sup>)<br>
                            &bull; <i>D<sub>balls</sub></i> = 1 - (Balls_Remaining / 120)<br>
                            &bull; <i>W<sub>lev</sub></i> = 1 - (Wickets_In_Hand / 10)<sup>1.2</sup><br><br>
                            <b>PI<sub>chase</sub></b> = 0.40 &times; U<sub>RRR</sub> + 0.35 &times; D<sub>balls</sub> &times; (RRR / 8.5) + 0.25 &times; W<sub>lev</sub>
                        </div>
                        <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-800 font-mono text-xs text-slate-200">
                            <b class="text-indigo-400">Innings 1 (Target Setting):</b><br><br>
                            &bull; <b>Death Overs (16&ndash;20):</b><br>
                            PI<sub>death</sub> = 0.55 + 0.08 &times; (over - 16) + 0.15 &times; (W_lost / 10)<br><br>
                            &bull; <b>Crisis Collapse:</b><br>
                            &le; 6 overs & &ge; 3 wickets lost &rarr; PI = 0.70<br>
                            &bull; <b>Super Overs:</b> PI = 1.00 (Absolute Leverage)
                        </div>
                    </div>
                </div>

                <div>
                    <h3 class="text-lg font-bold text-white mb-2 flex items-center gap-2">
                        <span class="w-2.5 h-2.5 rounded-full bg-indigo-500"></span>
                        2. Empirical Bayes Shrinkage Formulation
                    </h3>
                    <p class="text-xs leading-relaxed text-slate-400 mb-3">
                        To eliminate small-sample noise, raw player rates are shrunk towards tournament high-pressure priors with parameter $K = 50$ deliveries:
                    </p>
                    <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-800 font-mono text-xs text-slate-200">
                        &theta;&#770;<sub>i</sub> = [ N<sub>i</sub> / (N<sub>i</sub> + K) ] &times; &theta;<sub>i</sub><sup>raw</sup> + [ K / (N<sub>i</sub> + K) ] &times; &mu;<sub>0</sub><br><br>
                        Batters Prior: &mu;<sub>SR</sub> = 135.0, &mu;<sub>Dot</sub> = 36.0% | Bowlers Prior: &mu;<sub>ER</sub> = 9.20, &mu;<sub>Wkt</sub> = 7.0%
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 5: RETENTIONS & TRADES -->
        <div id="tab-retentions" class="tab-content hidden space-y-6">
            <div class="flex justify-between items-center">
                <div>
                    <h3 class="text-base font-bold text-white">Official IPL 2027 Retentions & Franchise Purses</h3>
                    <p class="text-xs text-slate-400">Official figures released by BCCI / IPL ahead of the December 16, 2026 Player Auction in Goa.</p>
                </div>
            </div>

            <!-- Purses Cards -->
            <div class="grid grid-cols-2 sm:grid-cols-5 gap-3" id="purses-grid">
                <!-- Injected via JS -->
            </div>

            <!-- Traded Players Register -->
            <div class="glass-card rounded-2xl p-5 border border-slate-800">
                <h4 class="text-sm font-bold text-white mb-3">All 14 Official IPL 2027 Trades (Including Shami to RR)</h4>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs">
                        <thead class="bg-slate-900 text-slate-400 uppercase text-[10px] border-b border-slate-800">
                            <tr>
                                <th class="py-2.5 px-3">Player</th>
                                <th class="py-2.5 px-3">From Team</th>
                                <th class="py-2.5 px-3">To Team</th>
                                <th class="py-2.5 px-3">Trade Type</th>
                                <th class="py-2.5 px-3">Fee (INR)</th>
                                <th class="py-2.5 px-3">Fee Status</th>
                            </tr>
                        </thead>
                        <tbody id="trades-tbody" class="divide-y divide-slate-800/60 font-mono text-slate-300">
                            <!-- Injected via JS -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

    </main>

    <!-- Footer -->
    <footer class="border-t border-slate-900 bg-slate-950/80 py-4 mt-8 text-center text-xs text-slate-500">
        Rajasthan Royals SupeRR Selector Season 2 &bull; Case Study Submission by Mohammed Aleem Bukkapatnam &bull; Verified on 200,999 Deliveries
    </footer>

    <!-- Embedded Data & Scripts -->
    <script>
        const topBatters = {json.dumps(top10_bat_list)};
        const topBowlers = {json.dumps(top10_bowl_list)};
        const allBatters = {json.dumps(all_bat_list)};
        const allBowlers = {json.dumps(all_bowl_list)};
        const trades = {json.dumps(trades_list)};
        const purses = {json.dumps(purses_list)};

        function switchTab(tabId) {{
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.tab-btn').forEach(el => {{
                el.classList.remove('active', 'bg-rr-pink', 'text-white');
                el.classList.add('text-slate-400');
            }});
            
            document.getElementById('tab-' + tabId).classList.remove('hidden');
            const activeBtn = document.getElementById('tab-btn-' + tabId);
            activeBtn.classList.add('active', 'bg-rr-pink', 'text-white');
            activeBtn.classList.remove('text-slate-400');

            if (tabId === 'visuals') {{
                renderPlots();
            }}
        }}

        // Render Batters Table
        const batTbody = document.getElementById('batters-tbody');
        topBatters.forEach((p, idx) => {{
            const tr = document.createElement('tr');
            tr.className = 'hover:bg-slate-800/40 transition-colors';
            tr.innerHTML = `
                <td class="py-2.5 px-4 text-center font-bold text-pink-400">#${{idx + 1}}</td>
                <td class="py-2.5 px-4 font-sans font-semibold text-white">${{p.player_name}}</td>
                <td class="py-2.5 px-4 text-center text-slate-400">${{p.hp_balls}}</td>
                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">${{p.hp_sr.toFixed(1)}}</td>
                <td class="py-2.5 px-4 text-center text-slate-400">${{p.base_sr.toFixed(1)}}</td>
                <td class="py-2.5 px-4 text-center font-bold text-amber-400">+${{p.delta_sr.toFixed(1)}}</td>
                <td class="py-2.5 px-4 text-center text-slate-400">${{p.hp_dot_pct.toFixed(1)}}%</td>
                <td class="py-2.5 px-4 text-center text-indigo-400">${{(p.consistency_rate * 100).toFixed(1)}}%</td>
                <td class="py-2.5 px-4 text-center font-bold text-pink-400 bg-pink-500/10 rounded-lg">${{p.cbps_score.toFixed(2)}}</td>
            `;
            batTbody.appendChild(tr);
        }});

        // Render Bowlers Table
        const bowlTbody = document.getElementById('bowlers-tbody');
        topBowlers.forEach((p, idx) => {{
            const tr = document.createElement('tr');
            tr.className = 'hover:bg-slate-800/40 transition-colors';
            tr.innerHTML = `
                <td class="py-2.5 px-4 text-center font-bold text-indigo-400">#${{idx + 1}}</td>
                <td class="py-2.5 px-4 font-sans font-semibold text-white">${{p.player_name}}</td>
                <td class="py-2.5 px-4 text-center text-slate-400">${{p.hp_balls}}</td>
                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">${{p.hp_econ.toFixed(2)}}</td>
                <td class="py-2.5 px-4 text-center text-slate-400">${{p.base_econ.toFixed(2)}}</td>
                <td class="py-2.5 px-4 text-center font-bold text-amber-400">${{p.delta_econ >= 0 ? '+' : ''}}${{p.delta_econ.toFixed(2)}}</td>
                <td class="py-2.5 px-4 text-center text-rose-400">${{p.hp_wkt_rate.toFixed(1)}}%</td>
                <td class="py-2.5 px-4 text-center text-indigo-400">${{(p.consistency_rate * 100).toFixed(1)}}%</td>
                <td class="py-2.5 px-4 text-center font-bold text-indigo-400 bg-indigo-500/10 rounded-lg">${{p.cbps_score.toFixed(2)}}</td>
            `;
            bowlTbody.appendChild(tr);
        }});

        // Render Purses
        const pursesGrid = document.getElementById('purses-grid');
        purses.forEach(item => {{
            const card = document.createElement('div');
            card.className = 'glass-card p-3 rounded-xl border border-slate-800';
            card.innerHTML = `
                <div class="flex justify-between items-center text-xs">
                    <span class="font-bold text-white">${{item.team_code}}</span>
                    <span class="text-slate-400 text-[10px]">${{item.retained_players}} retained</span>
                </div>
                <div class="mt-2">
                    <p class="text-[10px] uppercase text-slate-500 font-semibold">Purse Remaining</p>
                    <p class="text-base font-extrabold text-emerald-400">₹${{item.salary_cap_available_cr.toFixed(2)}} Cr</p>
                </div>
                <div class="mt-1 flex justify-between text-[10px] text-slate-400">
                    <span>${{item.available_slots}} slots left</span>
                    <span>${{item.available_overseas_slots}} overseas</span>
                </div>
            `;
            pursesGrid.appendChild(card);
        }});

        // Render Trades
        const tradesTbody = document.getElementById('trades-tbody');
        trades.forEach(t => {{
            const tr = document.createElement('tr');
            tr.className = 'hover:bg-slate-800/40 transition-colors';
            tr.innerHTML = `
                <td class="py-2 px-3 font-semibold text-white">${{t.player_name}}</td>
                <td class="py-2 px-3 text-slate-400">${{t.from_team}}</td>
                <td class="py-2 px-3 font-bold text-pink-400">${{t.to_team}}</td>
                <td class="py-2 px-3 text-slate-400">${{t.trade_type}}</td>
                <td class="py-2 px-3 font-bold text-emerald-400">${{t.trade_fee_inr}}</td>
                <td class="py-2 px-3 text-slate-400">${{t.fee_status}}</td>
            `;
            tradesTbody.appendChild(tr);
        }});

        // Render Plotly Charts
        function renderPlots() {{
            // Batters Plot
            const batTrace = {{
                x: allBatters.map(p => p.hp_dot_pct),
                y: allBatters.map(p => p.delta_sr),
                text: allBatters.map(p => `${{p.player_name}}<br>HP SR: ${{p.hp_sr.toFixed(1)}}<br>&Delta;SR: +${{p.delta_sr.toFixed(1)}}`),
                mode: 'markers+text',
                textposition: 'top center',
                textfont: {{ family: 'Inter', size: 9, color: '#94a3b8' }},
                marker: {{
                    size: allBatters.map(p => Math.sqrt(p.hp_balls) * 1.2),
                    color: allBatters.map(p => p.cbps_score),
                    colorscale: 'Viridis',
                    showscale: false
                }}
            }};

            const batLayout = {{
                paper_bgcolor: 'transparent',
                plot_bgcolor: 'transparent',
                margin: {{ t: 20, r: 20, b: 40, l: 40 }},
                xaxis: {{ title: 'High Pressure Dot Ball % (Lower is Better)', gridcolor: '#1e293b', zerolinecolor: '#334155', color: '#94a3b8' }},
                yaxis: {{ title: '&Delta; Strike Rate Elevation', gridcolor: '#1e293b', zerolinecolor: '#334155', color: '#94a3b8' }}
            }};

            Plotly.newPlot('plotly-batters', [batTrace], batLayout, {{ responsive: true, displayModeBar: false }});

            // Bowlers Plot
            const bowlTrace = {{
                x: allBowlers.map(p => p.hp_econ),
                y: allBowlers.map(p => p.hp_wkt_rate),
                text: allBowlers.map(p => `${{p.player_name}}<br>Econ: ${{p.hp_econ.toFixed(2)}}<br>Wkt%: ${{p.hp_wkt_rate.toFixed(1)}}%`),
                mode: 'markers+text',
                textposition: 'top center',
                textfont: {{ family: 'Inter', size: 9, color: '#94a3b8' }},
                marker: {{
                    size: allBowlers.map(p => Math.sqrt(p.hp_balls) * 1.2),
                    color: allBowlers.map(p => p.cbps_score),
                    colorscale: 'Plasma',
                    showscale: false
                }}
            }};

            const bowlLayout = {{
                paper_bgcolor: 'transparent',
                plot_bgcolor: 'transparent',
                margin: {{ t: 20, r: 20, b: 40, l: 40 }},
                xaxis: {{ title: 'High Pressure Economy Rate (Lower is Better)', gridcolor: '#1e293b', zerolinecolor: '#334155', color: '#94a3b8' }},
                yaxis: {{ title: 'Wicket Threat Rate % (Higher is Better)', gridcolor: '#1e293b', zerolinecolor: '#334155', color: '#94a3b8' }}
            }};

            Plotly.newPlot('plotly-bowlers', [bowlTrace], bowlLayout, {{ responsive: true, displayModeBar: false }});
        }}
    </script>
</body>
</html>
"""
    
    out_html = 'rr-submission/dashboard/index.html'
    with open(out_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"STAGE 5 COMPLETE: Generated interactive dashboard to: {out_html}")
    print(f"Dashboard size: {os.path.getsize(out_html) / 1024:.1f} KB")

if __name__ == '__main__':
    build_dashboard()

