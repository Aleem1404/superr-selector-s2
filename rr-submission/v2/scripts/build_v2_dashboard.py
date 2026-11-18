import pandas as pd
import json
import os

def build_v2_dashboard():
    print("=" * 60)
    print("STAGE 5 (v2): Building Interactive Standalone Web Dashboard (v2)")
    print("=" * 60)
    
    top_bat_csv = 'rr-submission/v2/stage4_consistency_scoring/top10_batters_v2_final.csv'
    top_bowl_csv = 'rr-submission/v2/stage4_consistency_scoring/top10_bowlers_v2_final.csv'
    all_bat_csv = 'rr-submission/v2/stage4_consistency_scoring/ranked_batters_v2_master.csv'
    all_bowl_csv = 'rr-submission/v2/stage4_consistency_scoring/ranked_bowlers_v2_master.csv'
    trades_csv = 'IPL-2027-trades.csv'
    purses_csv = 'cricinfo-data/IPL-2027-retentions/ipl_2027_team_purses_and_slots.csv'
    
    df_top_bat = pd.read_csv(top_bat_csv)
    df_top_bowl = pd.read_csv(top_bowl_csv)
    df_all_bat = pd.read_csv(all_bat_csv).head(40)
    df_all_bowl = pd.read_csv(all_bowl_csv).head(40)
    df_trades = pd.read_csv(trades_csv) if os.path.exists(trades_csv) else pd.DataFrame()
    df_purses = pd.read_csv(purses_csv) if os.path.exists(purses_csv) else pd.DataFrame()
    
    top10_bat_list = df_top_bat.to_dict(orient='records')
    top10_bowl_list = df_top_bowl.to_dict(orient='records')
    all_bat_list = df_all_bat.to_dict(orient='records')
    all_bowl_list = df_all_bowl.to_dict(orient='records')
    trades_list = df_trades.to_dict(orient='records') if not df_trades.empty else []
    purses_list = df_purses.to_dict(orient='records') if not df_purses.empty else []
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rajasthan Royals SupeRR Selector Season 2 | Pressure Model Dashboard (v2)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
        body {{
            font-family: 'Inter', sans-serif;
            background-color: #0b1120;
            color: #f1f5f9;
        }}
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
                        <span class="text-xs px-2 py-0.5 rounded-full bg-pink-500/20 text-pink-400 border border-pink-500/30 font-medium">Model v2 (Venue-Calibrated)</span>
                    </h1>
                    <p class="text-xs text-slate-400">Grounded in 200,999 Deliveries & ball-to-ball-stats IPL Stadium Par Rates</p>
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
                <p class="text-xs font-semibold text-pink-400 uppercase tracking-wider">Venue-Calibrated HP Balls</p>
                <p class="text-2xl font-extrabold text-pink-400 mt-1">58,125</p>
                <p class="text-[11px] text-slate-500 mt-0.5">28.92% Dynamic Leverage Boundary</p>
            </div>
            <div class="glass-card rounded-2xl p-4 border border-slate-800/80 shadow-sm">
                <p class="text-xs font-semibold text-indigo-400 uppercase tracking-wider">Stadiums Tracked</p>
                <p class="text-2xl font-extrabold text-indigo-400 mt-1">17 Venues</p>
                <p class="text-[11px] text-slate-500 mt-0.5">Exact Pitch Par Rates Computed</p>
            </div>
            <div class="glass-card rounded-2xl p-4 border border-slate-800/80 shadow-sm">
                <p class="text-xs font-semibold text-amber-400 uppercase tracking-wider">Validation Metric</p>
                <p class="text-2xl font-extrabold text-amber-400 mt-1">r = 0.91</p>
                <p class="text-[11px] text-slate-500 mt-0.5">v2 Split-Half Stability</p>
            </div>
        </div>

        <!-- Navigation Tabs -->
        <div class="flex flex-wrap gap-2 border-b border-slate-800 pb-2">
            <button onclick="switchTab('batters')" id="tab-btn-batters" class="tab-btn active px-4 py-2 rounded-xl text-xs font-semibold transition-all">
                Top 10 Batters (v2)
            </button>
            <button onclick="switchTab('bowlers')" id="tab-btn-bowlers" class="tab-btn px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white transition-all">
                Top 10 Bowlers (v2)
            </button>
            <button onclick="switchTab('visuals')" id="tab-btn-visuals" class="tab-btn px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white transition-all">
                Clutch Matrices
            </button>
            <button onclick="switchTab('methodology')" id="tab-btn-methodology" class="tab-btn px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white transition-all">
                v2 Mathematical Formulation
            </button>
            <button onclick="switchTab('retentions')" id="tab-btn-retentions" class="tab-btn px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white transition-all">
                IPL 2027 Retentions & Trades
            </button>
        </div>

        <!-- TAB 1: BATTERS -->
        <div id="tab-batters" class="tab-content space-y-4">
            <div class="flex flex-wrap justify-between items-center gap-2">
                <div>
                    <h2 class="text-base font-bold text-white">Top 10 Batters Under High Pressure (v2)</h2>
                    <p class="text-xs text-slate-400">Calibrated for Venue Pitch Par ($Par_{{venue}}$) + Playoff Multipliers + Bayesian Shrinkage</p>
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
                                <th class="py-3 px-4 text-center">&Delta; SR vs Venue Par</th>
                                <th class="py-3 px-4 text-center">&Delta; SR vs Baseline</th>
                                <th class="py-3 px-4 text-center">HP Dot Ball %</th>
                                <th class="py-3 px-4 text-center">Match Consistency</th>
                                <th class="py-3 px-4 text-center">CBPS v2</th>
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
                    <h2 class="text-base font-bold text-white">Top 10 Bowlers Under High Pressure (v2)</h2>
                    <p class="text-xs text-slate-400">Evaluates Venue Run Suppression ($Par_{{venue}} - Econ_{{HP}}$) + Wicket Strike Rates + Playoff Consistency</p>
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
                                <th class="py-3 px-4 text-center">&Delta; Economy vs Venue</th>
                                <th class="py-3 px-4 text-center">&Delta; Economy vs Baseline</th>
                                <th class="py-3 px-4 text-center">Wicket Threat %</th>
                                <th class="py-3 px-4 text-center">Match Reliability</th>
                                <th class="py-3 px-4 text-center">CBPS v2</th>
                            </tr>
                        </thead>
                        <tbody id="bowlers-tbody" class="divide-y divide-slate-800/60 font-mono text-slate-300">
                            <!-- Injected via JS -->
                        </tbody>
                    </table>
                </div>
            </div>
        </div>

        <!-- TAB 3: VISUALS -->
        <div id="tab-visuals" class="tab-content hidden space-y-6">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="glass-card rounded-2xl p-4 border border-slate-800">
                    <h3 class="text-sm font-bold text-white mb-2">v2 Batter Clutch Matrix: &Delta;SR vs Venue Par vs Dot %</h3>
                    <p class="text-xs text-slate-400 mb-4">Size represents sample volume; color indicates CBPS v2 score.</p>
                    <div id="plotly-batters" class="w-full h-80"></div>
                </div>

                <div class="glass-card rounded-2xl p-4 border border-slate-800">
                    <h3 class="text-sm font-bold text-white mb-2">v2 Bowler Clutch Matrix: Venue Run Suppression vs Wicket Threat</h3>
                    <p class="text-xs text-slate-400 mb-4">Top-right demonstrates bowlers who suppress runs below stadium par while striking frequently.</p>
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
                        Model v2: Venue-Calibrated Leverage & Stadium Pitch Par
                    </h3>
                    <p class="text-xs leading-relaxed text-slate-400 mb-3">
                        In Model v2, the Chase Leverage Urgency Sigmoid is centered dynamically at each stadium's historical scoring rate ($Par_{{venue}}$) rather than a flat 9.0 RPO.
                    </p>
                    <div class="bg-slate-900/80 p-4 rounded-xl border border-slate-800 font-mono text-xs text-slate-200">
                        <b>Dynamic Stadium Par:</b><br>
                        &bull; Sawai Mansingh Stadium, Jaipur: Par = 9.36 RPO<br>
                        &bull; Barsapara Cricket Stadium, Guwahati: Par = 8.72 RPO<br>
                        &bull; Wankhede Stadium, Mumbai: Par = 8.83 RPO<br>
                        &bull; MA Chidambaram Stadium, Chennai: Par = 8.27 RPO<br>
                        &bull; M. Chinnaswamy Stadium, Bengaluru: Par = 9.36 RPO<br><br>
                        <b>Playoff Multipliers:</b> Qualifier & Eliminator matches = 1.20&times; | IPL Finals = 1.30&times;
                    </div>
                </div>
            </div>
        </div>

        <!-- TAB 5: RETENTIONS & TRADES -->
        <div id="tab-retentions" class="tab-content hidden space-y-6">
            <div class="grid grid-cols-2 sm:grid-cols-5 gap-3" id="purses-grid"></div>
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
                        <tbody id="trades-tbody" class="divide-y divide-slate-800/60 font-mono text-slate-300"></tbody>
                    </table>
                </div>
            </div>
        </div>

    </main>

    <!-- Footer -->
    <footer class="border-t border-slate-900 bg-slate-950/80 py-4 mt-8 text-center text-xs text-slate-500">
        Rajasthan Royals SupeRR Selector Season 2 &bull; Model v2 Submission by Mohammed Aleem Bukkapatnam &bull; Verified across 200,999 Deliveries & ball-to-ball-stats
    </footer>

    <!-- Script Injection -->
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

        // Render Batters
        const batTbody = document.getElementById('batters-tbody');
        topBatters.forEach((p, idx) => {{
            const tr = document.createElement('tr');
            tr.className = 'hover:bg-slate-800/40 transition-colors';
            tr.innerHTML = `
                <td class="py-2.5 px-4 text-center font-bold text-pink-400">#${{idx + 1}}</td>
                <td class="py-2.5 px-4 font-sans font-semibold text-white">${{p.player_name}}</td>
                <td class="py-2.5 px-4 text-center text-slate-400">${{p.hp_balls}}</td>
                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">${{p.hp_sr.toFixed(1)}}</td>
                <td class="py-2.5 px-4 text-center font-bold text-pink-400">+${{p.delta_sr_venue.toFixed(1)}}</td>
                <td class="py-2.5 px-4 text-center font-bold text-amber-400">+${{p.delta_sr_baseline.toFixed(1)}}</td>
                <td class="py-2.5 px-4 text-center text-slate-400">${{p.hp_dot_pct.toFixed(1)}}%</td>
                <td class="py-2.5 px-4 text-center text-indigo-400">${{(p.consistency_rate * 100).toFixed(1)}}%</td>
                <td class="py-2.5 px-4 text-center font-bold text-pink-400 bg-pink-500/10 rounded-lg">${{p.cbps_score_v2.toFixed(2)}}</td>
            `;
            batTbody.appendChild(tr);
        }});

        // Render Bowlers
        const bowlTbody = document.getElementById('bowlers-tbody');
        topBowlers.forEach((p, idx) => {{
            const tr = document.createElement('tr');
            tr.className = 'hover:bg-slate-800/40 transition-colors';
            tr.innerHTML = `
                <td class="py-2.5 px-4 text-center font-bold text-indigo-400">#${{idx + 1}}</td>
                <td class="py-2.5 px-4 font-sans font-semibold text-white">${{p.player_name}}</td>
                <td class="py-2.5 px-4 text-center text-slate-400">${{p.hp_balls}}</td>
                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">${{p.hp_econ.toFixed(2)}}</td>
                <td class="py-2.5 px-4 text-center font-bold text-emerald-400">${{p.delta_econ_venue >= 0 ? '+' : ''}}${{p.delta_econ_venue.toFixed(2)}}</td>
                <td class="py-2.5 px-4 text-center font-bold text-amber-400">${{p.delta_econ_baseline >= 0 ? '+' : ''}}${{p.delta_econ_baseline.toFixed(2)}}</td>
                <td class="py-2.5 px-4 text-center text-rose-400">${{p.hp_wkt_rate.toFixed(1)}}%</td>
                <td class="py-2.5 px-4 text-center text-indigo-400">${{(p.consistency_rate * 100).toFixed(1)}}%</td>
                <td class="py-2.5 px-4 text-center font-bold text-indigo-400 bg-indigo-500/10 rounded-lg">${{p.cbps_score_v2.toFixed(2)}}</td>
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

        // Render Plots
        function renderPlots() {{
            const batTrace = {{
                x: allBatters.map(p => p.hp_dot_pct),
                y: allBatters.map(p => p.delta_sr_venue),
                text: allBatters.map(p => `${{p.player_name}}<br>HP SR: ${{p.hp_sr.toFixed(1)}}<br>Venue &Delta;SR: +${{p.delta_sr_venue.toFixed(1)}}`),
                mode: 'markers+text',
                textposition: 'top center',
                textfont: {{ family: 'Inter', size: 9, color: '#94a3b8' }},
                marker: {{
                    size: allBatters.map(p => Math.sqrt(p.hp_balls) * 1.2),
                    color: allBatters.map(p => p.cbps_score_v2),
                    colorscale: 'Viridis',
                    showscale: false
                }}
            }};

            const batLayout = {{
                paper_bgcolor: 'transparent',
                plot_bgcolor: 'transparent',
                margin: {{ t: 20, r: 20, b: 40, l: 40 }},
                xaxis: {{ title: 'High Pressure Dot Ball %', gridcolor: '#1e293b', zerolinecolor: '#334155', color: '#94a3b8' }},
                yaxis: {{ title: '&Delta; Strike Rate vs Stadium Par', gridcolor: '#1e293b', zerolinecolor: '#334155', color: '#94a3b8' }}
            }};

            Plotly.newPlot('plotly-batters', [batTrace], batLayout, {{ responsive: true, displayModeBar: false }});

            const bowlTrace = {{
                x: allBowlers.map(p => p.delta_econ_venue),
                y: allBowlers.map(p => p.hp_wkt_rate),
                text: allBowlers.map(p => `${{p.player_name}}<br>Econ: ${{p.hp_econ.toFixed(2)}}<br>Wkt%: ${{p.hp_wkt_rate.toFixed(1)}}%`),
                mode: 'markers+text',
                textposition: 'top center',
                textfont: {{ family: 'Inter', size: 9, color: '#94a3b8' }},
                marker: {{
                    size: allBowlers.map(p => Math.sqrt(p.hp_balls) * 1.2),
                    color: allBowlers.map(p => p.cbps_score_v2),
                    colorscale: 'Plasma',
                    showscale: false
                }}
            }};

            const bowlLayout = {{
                paper_bgcolor: 'transparent',
                plot_bgcolor: 'transparent',
                margin: {{ t: 20, r: 20, b: 40, l: 40 }},
                xaxis: {{ title: 'Venue Run Suppression (Par - Econ)', gridcolor: '#1e293b', zerolinecolor: '#334155', color: '#94a3b8' }},
                yaxis: {{ title: 'Wicket Threat Rate %', gridcolor: '#1e293b', zerolinecolor: '#334155', color: '#94a3b8' }}
            }};

            Plotly.newPlot('plotly-bowlers', [bowlTrace], bowlLayout, {{ responsive: true, displayModeBar: false }});
        }}
    </script>
</body>
</html>
"""
    
    out_html = 'rr-submission/v2/dashboard/index.html'
    with open(out_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print(f"STAGE 5 (v2) COMPLETE: Generated v2 interactive dashboard to: {out_html}")
    print(f"v2 Dashboard size: {os.path.getsize(out_html) / 1024:.1f} KB")

if __name__ == '__main__':
    build_v2_dashboard()

