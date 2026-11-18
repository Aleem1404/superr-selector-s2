import pandas as pd
import json
import os

def build_v3_dashboard():
    print("=" * 60)
    print("STAGE 5 (v3): Building Interactive Standalone Web Dashboard (v3)")
    print("=" * 60)
    
    top_bat_csv = 'rr-submission/v3/stage4_consistency_scoring/top10_batters_v3_final.csv'
    top_bowl_csv = 'rr-submission/v3/stage4_consistency_scoring/top10_bowlers_v3_final.csv'
    active_bat_csv = 'rr-submission/v3/stage4_consistency_scoring/active_batters_v3_master.csv'
    active_bowl_csv = 'rr-submission/v3/stage4_consistency_scoring/active_bowlers_v3_master.csv'
    trades_csv = 'IPL-2027-trades.csv'
    purses_csv = 'cricinfo-data/IPL-2027-retentions/ipl_2027_team_purses_and_slots.csv'
    
    df_top_bat = pd.read_csv(top_bat_csv)
    df_top_bowl = pd.read_csv(top_bowl_csv)
    df_active_bat = pd.read_csv(active_bat_csv).head(35)
    df_active_bowl = pd.read_csv(active_bowl_csv).head(35)
    df_trades = pd.read_csv(trades_csv) if os.path.exists(trades_csv) else pd.DataFrame()
    df_purses = pd.read_csv(purses_csv) if os.path.exists(purses_csv) else pd.DataFrame()
    
    top10_bat_list = df_top_bat.to_dict(orient='records')
    top10_bowl_list = df_top_bowl.to_dict(orient='records')
    all_bat_list = df_active_bat.to_dict(orient='records')
    all_bowl_list = df_active_bowl.to_dict(orient='records')
    trades_list = df_trades.to_dict(orient='records') if not df_trades.empty else []
    purses_list = df_purses.to_dict(orient='records') if not df_purses.empty else []
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rajasthan Royals SupeRR Selector Season 2 | Pressure Model Dashboard (v3)</title>
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
                        <span class="text-xs px-2.5 py-0.5 rounded-full bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-semibold">Model v3 (Active Roster Calibrated)</span>
                    </h1>
                    <p class="text-xs text-slate-400">Venue Par Baseline + Cricinfo & Announcement Retirement Filter</p>
                </div>
            </div>
            
            <div class="flex items-center space-x-3 text-xs text-slate-300">
                <div class="bg-slate-900 border border-slate-800 px-3 py-1.5 rounded-lg flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-pink-500 animate-pulse"></span>
                    <span>Candidate: <b class="text-white">Mohammed Aleem Bukkapatnam</b> (M.S. in AI)</span>
                </div>
            </div>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-1 w-full space-y-6">

        <!-- Active Roster & Retirement Criteria Banner -->
        <div class="glass-card rounded-2xl p-4 border border-emerald-500/30 bg-emerald-950/10 flex flex-wrap items-center justify-between gap-4">
            <div class="flex items-start space-x-3">
                <div class="p-2 rounded-xl bg-emerald-500/20 text-emerald-400 border border-emerald-500/30 font-bold text-lg">
                    ✓
                </div>
                <div>
                    <h3 class="text-sm font-bold text-emerald-300">Criteria 1 Implementation: Official Retirement Filter Enforced</h3>
                    <p class="text-xs text-slate-300 mt-0.5 leading-relaxed">
                        Confirmed retired veterans (<b>MS Dhoni</b> - retired & transitioned to CSK Mentor; <b>Dinesh Karthik</b> - retired 1 June 2024, RCB coach; <b>Matthew Wade</b> - retired Oct 2024, Australia coach) are strictly excluded based on <b>Option 3 (Cricinfo Profile Status)</b> and <b>Option 4 (Official Announcements)</b>. All active contracted and retained superstars (<b>Jos Buttler</b>, <b>Dhruv Jurel</b>, <b>Jasprit Bumrah</b>, <b>Sunil Narine</b>, <b>Tim David</b>) are verified and preserved.
                    </p>
                </div>
            </div>
            <div class="text-xs font-semibold px-3 py-1.5 rounded-lg bg-slate-900 text-slate-300 border border-slate-700">
                100% Active Candidates
            </div>
        </div>

        <!-- KPI Summary Ribbon -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4">
            <div class="glass-card rounded-2xl p-4 border border-slate-800/80 shadow-sm">
                <p class="text-xs font-semibold text-slate-400 uppercase tracking-wider">Total Deliveries</p>
                <p class="text-2xl font-extrabold text-white mt-1">200,999</p>
                <p class="text-[11px] text-slate-500 mt-0.5">867 Matches (IPL & T20I)</p>
            </div>
            <div class="glass-card rounded-2xl p-4 border border-slate-800/80 shadow-sm">
                <p class="text-xs font-semibold text-pink-400 uppercase tracking-wider">High-Pressure Balls</p>
                <p class="text-2xl font-extrabold text-pink-400 mt-1">58,125</p>
                <p class="text-[11px] text-slate-500 mt-0.5">28.92% Dynamic LI &ge; 1.50</p>
            </div>
            <div class="glass-card rounded-2xl p-4 border border-slate-800/80 shadow-sm">
                <p class="text-xs font-semibold text-indigo-400 uppercase tracking-wider">Venue Par Calibrations</p>
                <p class="text-2xl font-extrabold text-indigo-400 mt-1">17 Stadiums</p>
                <p class="text-[11px] text-slate-500 mt-0.5">Chinnaswamy (10.15) to Jaipur (8.54)</p>
            </div>
            <div class="glass-card rounded-2xl p-4 border border-slate-800/80 shadow-sm">
                <p class="text-xs font-semibold text-emerald-400 uppercase tracking-wider">Active Qualified Pool</p>
                <p class="text-2xl font-extrabold text-emerald-400 mt-1">72 Bat / 68 Bowl</p>
                <p class="text-[11px] text-slate-500 mt-0.5">Filtered for Active Contracts</p>
            </div>
        </div>

        <!-- Navigation Tabs -->
        <div class="flex items-center space-x-2 border-b border-slate-800 pb-2">
            <button onclick="switchTab('batters')" id="tab-batters" class="tab-btn active px-4 py-2 rounded-xl text-xs font-semibold transition-all">
                Top 10 Active Batters
            </button>
            <button onclick="switchTab('bowlers')" id="tab-bowlers" class="tab-btn px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white transition-all">
                Top 10 Active Bowlers
            </button>
            <button onclick="switchTab('quadrant')" id="tab-quadrant" class="tab-btn px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white transition-all">
                Clutch Quadrant Matrices
            </button>
            <button onclick="switchTab('methodology')" id="tab-methodology" class="tab-btn px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white transition-all">
                v3 Methodology & Verification
            </button>
        </div>

        <!-- BATTERS TAB -->
        <section id="sec-batters" class="space-y-6">
            <div class="glass-card rounded-2xl p-5 border border-slate-800">
                <div class="flex flex-wrap justify-between items-center gap-2 mb-4">
                    <div>
                        <h2 class="text-base font-bold text-white flex items-center gap-2">
                            Top 10 Batters Performing Under Pressure (Model v3)
                            <span class="text-xs font-normal text-slate-400">(Ranked by CBPS v3)</span>
                        </h2>
                        <p class="text-xs text-slate-400">Blends Absolute HP SR, Venue Par Outperformance, Baseline Delta, Dot Minimization & Match Consistency.</p>
                    </div>
                </div>

                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs">
                        <thead class="bg-slate-900/80 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
                            <tr>
                                <th class="p-3">Rank</th>
                                <th class="p-3">Player Name</th>
                                <th class="p-3">HP Balls</th>
                                <th class="p-3">HP Strike Rate</th>
                                <th class="p-3 text-pink-400">&Delta; Venue Par SR</th>
                                <th class="p-3 text-indigo-400">&Delta; Baseline SR</th>
                                <th class="p-3">Dot Ball %</th>
                                <th class="p-3">Consistency</th>
                                <th class="p-3 text-right">CBPS (v3)</th>
                            </tr>
                        </thead>
                        <tbody id="batters-tbody" class="divide-y divide-slate-800/60 font-medium">
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Batters Quick Cards -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" id="batters-cards">
            </div>
        </section>

        <!-- BOWLERS TAB -->
        <section id="sec-bowlers" class="space-y-6 hidden">
            <div class="glass-card rounded-2xl p-5 border border-slate-800">
                <div class="flex flex-wrap justify-between items-center gap-2 mb-4">
                    <div>
                        <h2 class="text-base font-bold text-white flex items-center gap-2">
                            Top 10 Bowlers Performing Under Pressure (Model v3)
                            <span class="text-xs font-normal text-slate-400">(Ranked by CBPS v3)</span>
                        </h2>
                        <p class="text-xs text-slate-400">Evaluates Economy Suppression vs Venue Par, Baseline Delta, High-Leverage Wicket Strike Rate & Reliability.</p>
                    </div>
                </div>

                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs">
                        <thead class="bg-slate-900/80 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
                            <tr>
                                <th class="p-3">Rank</th>
                                <th class="p-3">Player Name</th>
                                <th class="p-3">HP Balls</th>
                                <th class="p-3">HP Economy</th>
                                <th class="p-3 text-emerald-400">&Delta; Venue Par Econ</th>
                                <th class="p-3 text-indigo-400">&Delta; Baseline Econ</th>
                                <th class="p-3">Wicket Rate</th>
                                <th class="p-3">Consistency</th>
                                <th class="p-3 text-right">CBPS (v3)</th>
                            </tr>
                        </thead>
                        <tbody id="bowlers-tbody" class="divide-y divide-slate-800/60 font-medium">
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Bowlers Quick Cards -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" id="bowlers-cards">
            </div>
        </section>

        <!-- QUADRANT TAB -->
        <section id="sec-quadrant" class="space-y-6 hidden">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <div class="glass-card rounded-2xl p-5 border border-slate-800">
                    <h3 class="text-sm font-bold text-white mb-2">Batter Clutch Matrix (Venue Outperformance vs Baseline Delta)</h3>
                    <p class="text-xs text-slate-400 mb-4">Top-right quadrant indicates elite dual-engine clutch performers.</p>
                    <div id="plot-batters-matrix" style="height: 420px;"></div>
                </div>
                <div class="glass-card rounded-2xl p-5 border border-slate-800">
                    <h3 class="text-sm font-bold text-white mb-2">Bowler Clutch Matrix (Venue Economy Suppression vs Wicket Threat)</h3>
                    <p class="text-xs text-slate-400 mb-4">Upper-right quadrant represents rare hybrid run-stranglers and wicket-takers.</p>
                    <div id="plot-bowlers-matrix" style="height: 420px;"></div>
                </div>
            </div>
        </section>

        <!-- METHODOLOGY & AUDIT TAB -->
        <section id="sec-methodology" class="space-y-6 hidden">
            <div class="glass-card rounded-2xl p-6 border border-slate-800 space-y-4">
                <h2 class="text-base font-bold text-pink-400">Methodology Architecture & Mathematical Formulation (Model v3)</h2>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs text-slate-300">
                    <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
                        <span class="font-bold text-white block text-sm">1. Dynamic Leverage Index</span>
                        <p>Each delivery is tagged with a Leverage Index (LI) based on required run rate, balls remaining, wickets in hand, and match stage:</p>
                        <code class="block bg-slate-950 p-2 rounded text-[11px] text-pink-300">LI = RRR / (Wkts * Factor) &times; StageMult</code>
                        <p>Balls with LI &ge; 1.50 define high-pressure contexts.</p>
                    </div>

                    <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
                        <span class="font-bold text-white block text-sm">2. 17 Stadium Par Baselines</span>
                        <p>Calibrates player strike rates and economies against venue-specific high-pressure benchmarks derived from 87,074 balls across 5 IPL seasons:</p>
                        <code class="block bg-slate-950 p-2 rounded text-[11px] text-indigo-300">&Delta;SR_venue = SR_hp - Par_venue</code>
                        <p>Chinnaswamy (10.15) vs Jaipur (8.54) ensures cross-stadium equity.</p>
                    </div>

                    <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
                        <span class="font-bold text-white block text-sm">3. Active Roster Verification</span>
                        <p>Multi-source verification via Cricinfo Profile Status and Official Announcements:</p>
                        <code class="block bg-slate-950 p-2 rounded text-[11px] text-emerald-300">Active = Status != Retired & Contracted</code>
                        <p>Removes retired veterans (MS Dhoni, Karthik, Wade) while preserving active contracted stars (Buttler, Surya, Jurel, Tim David).</p>
                    </div>
                </div>

                <div class="p-4 rounded-xl bg-slate-900/80 border border-slate-800 text-xs text-slate-400">
                    <h4 class="font-bold text-white mb-1">Composite Ball Pressure Score (CBPS v3) Weighting Matrix</h4>
                    <p class="leading-relaxed">
                        <b>Batters:</b> 25% Shrunk High-Pressure Strike Rate + 25% Venue Par Delta + 20% Baseline Delta + 15% Dot Ball Reduction + 15% Match-Level Reliability.<br>
                        <b>Bowlers:</b> 25% Shrunk Economy Suppression + 25% Venue Par Delta + 20% Wicket Take Rate + 15% Dot Ball Pressure + 15% Match-Level Reliability.<br>
                        Both metrics incorporate Bayesian empirical prior shrinkage (k=50) and sample confidence dampening: <code>Confidence = min(1.0, sqrt(N / 250))</code>.
                    </p>
                </div>
            </div>
        </section>

    </main>

    <!-- Footer -->
    <footer class="border-t border-slate-800 bg-slate-950/80 py-4 text-center text-xs text-slate-500">
        <p>Rajasthan Royals SupeRR Selector Season 2 | Round 1 Submission Model v3</p>
        <p class="mt-1">Candidate: <b>Mohammed Aleem Bukkapatnam</b> (M.S. in Artificial Intelligence) | Email: <a href="mailto:mohammedaleem1404@gmail.com" class="text-pink-400 hover:underline">mohammedaleem1404@gmail.com</a></p>
    </footer>

    <!-- Client-side Data Injection -->
    <script>
        const top10Batters = {json.dumps(top10_bat_list)};
        const top10Bowlers = {json.dumps(top10_bowl_list)};
        const allActiveBatters = {json.dumps(all_bat_list)};
        const allActiveBowlers = {json.dumps(all_bowl_list)};

        function switchTab(tabId) {{
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active', 'text-white'));
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.add('text-slate-400'));
            
            const activeBtn = document.getElementById('tab-' + tabId);
            activeBtn.classList.add('active', 'text-white');
            activeBtn.classList.remove('text-slate-400');

            ['batters', 'bowlers', 'quadrant', 'methodology'].forEach(id => {{
                document.getElementById('sec-' + id).classList.add('hidden');
            }});
            document.getElementById('sec-' + tabId).classList.remove('hidden');

            if (tabId === 'quadrant') {{
                renderQuadrantCharts();
            }}
        }}

        function populateBatters() {{
            const tbody = document.getElementById('batters-tbody');
            const cards = document.getElementById('batters-cards');
            tbody.innerHTML = '';
            cards.innerHTML = '';

            top10Batters.forEach(b => {{
                const isRR = b.player_name === 'Dhruv Jurel';
                const row = document.createElement('tr');
                row.className = isRR ? 'bg-pink-950/20 text-white border-l-4 border-pink-500' : 'hover:bg-slate-900/50';
                row.innerHTML = `
                    <td class="p-3 font-bold text-slate-400">${{b.rank}}</td>
                    <td class="p-3 font-bold text-white flex items-center gap-1.5">
                        ${{b.player_name}}
                        ${{isRR ? '<span class="px-1.5 py-0.5 rounded text-[9px] bg-pink-500/20 text-pink-400 border border-pink-500/30">RR Retained</span>' : ''}}
                        ${{b.player_name === 'Tim David' ? '<span class="px-1.5 py-0.5 rounded text-[9px] bg-indigo-500/20 text-indigo-400 border border-indigo-500/30">Top 10 Entry</span>' : ''}}
                    </td>
                    <td class="p-3 text-slate-300">${{b.hp_balls}}</td>
                    <td class="p-3 font-bold text-white">${{b.hp_sr.toFixed(1)}}</td>
                    <td class="p-3 text-pink-400 font-semibold">+${{b.delta_sr_venue.toFixed(1)}}</td>
                    <td class="p-3 text-indigo-400 font-semibold">+${{b.delta_sr_baseline.toFixed(1)}}</td>
                    <td class="p-3 text-slate-300">${{b.hp_dot_pct.toFixed(1)}}%</td>
                    <td class="p-3 text-emerald-400 font-semibold">${{(b.consistency_rate * 100).toFixed(0)}}%</td>
                    <td class="p-3 text-right font-extrabold text-pink-400 text-sm">+${{b.cbps_score_v3.toFixed(2)}}</td>
                `;
                tbody.appendChild(row);

                if (b.rank <= 6) {{
                    const card = document.createElement('div');
                    card.className = 'glass-card p-4 rounded-xl border border-slate-800 space-y-2';
                    card.innerHTML = `
                        <div class="flex justify-between items-start">
                            <div>
                                <span class="text-[10px] text-pink-400 font-bold uppercase tracking-wider">Rank #${{b.rank}}</span>
                                <h4 class="text-sm font-bold text-white">${{b.player_name}}</h4>
                            </div>
                            <span class="text-xs px-2 py-0.5 rounded bg-pink-500/10 text-pink-400 border border-pink-500/20 font-bold">
                                +${{b.cbps_score_v3.toFixed(2)}}
                            </span>
                        </div>
                        <div class="grid grid-cols-3 gap-2 pt-1 text-center">
                            <div class="bg-slate-900/60 p-2 rounded-lg">
                                <p class="text-[10px] text-slate-400">HP SR</p>
                                <p class="text-xs font-bold text-white">${{b.hp_sr.toFixed(1)}}</p>
                            </div>
                            <div class="bg-slate-900/60 p-2 rounded-lg">
                                <p class="text-[10px] text-pink-400">&Delta;Venue</p>
                                <p class="text-xs font-bold text-pink-400">+${{b.delta_sr_venue.toFixed(1)}}</p>
                            </div>
                            <div class="bg-slate-900/60 p-2 rounded-lg">
                                <p class="text-[10px] text-emerald-400">Reliability</p>
                                <p class="text-xs font-bold text-emerald-400">${{(b.consistency_rate*100).toFixed(0)}}%</p>
                            </div>
                        </div>
                    `;
                    cards.appendChild(card);
                }}
            }});
        }}

        function populateBowlers() {{
            const tbody = document.getElementById('bowlers-tbody');
            const cards = document.getElementById('bowlers-cards');
            tbody.innerHTML = '';
            cards.innerHTML = '';

            top10Bowlers.forEach(b => {{
                const row = document.createElement('tr');
                row.className = b.rank === 1 ? 'bg-emerald-950/20 text-white border-l-4 border-emerald-500' : 'hover:bg-slate-900/50';
                row.innerHTML = `
                    <td class="p-3 font-bold text-slate-400">${{b.rank}}</td>
                    <td class="p-3 font-bold text-white">${{b.player_name}}</td>
                    <td class="p-3 text-slate-300">${{b.hp_balls}}</td>
                    <td class="p-3 font-bold text-white">${{b.hp_econ.toFixed(2)}}</td>
                    <td class="p-3 text-emerald-400 font-semibold">+${{b.delta_econ_venue.toFixed(2)}}</td>
                    <td class="p-3 text-indigo-400 font-semibold">${{b.delta_econ_baseline > 0 ? '+' : ''}}${{b.delta_econ_baseline.toFixed(2)}}</td>
                    <td class="p-3 text-slate-300">${{b.hp_wkt_rate.toFixed(1)}}%</td>
                    <td class="p-3 text-emerald-400 font-semibold">${{(b.consistency_rate * 100).toFixed(0)}}%</td>
                    <td class="p-3 text-right font-extrabold text-emerald-400 text-sm">+${{b.cbps_score_v3.toFixed(2)}}</td>
                `;
                tbody.appendChild(row);

                if (b.rank <= 6) {{
                    const card = document.createElement('div');
                    card.className = 'glass-card p-4 rounded-xl border border-slate-800 space-y-2';
                    card.innerHTML = `
                        <div class="flex justify-between items-start">
                            <div>
                                <span class="text-[10px] text-emerald-400 font-bold uppercase tracking-wider">Rank #${{b.rank}}</span>
                                <h4 class="text-sm font-bold text-white">${{b.player_name}}</h4>
                            </div>
                            <span class="text-xs px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-bold">
                                +${{b.cbps_score_v3.toFixed(2)}}
                            </span>
                        </div>
                        <div class="grid grid-cols-3 gap-2 pt-1 text-center">
                            <div class="bg-slate-900/60 p-2 rounded-lg">
                                <p class="text-[10px] text-slate-400">HP Econ</p>
                                <p class="text-xs font-bold text-white">${{b.hp_econ.toFixed(2)}}</p>
                            </div>
                            <div class="bg-slate-900/60 p-2 rounded-lg">
                                <p class="text-[10px] text-emerald-400">&Delta;Venue</p>
                                <p class="text-xs font-bold text-emerald-400">+${{b.delta_econ_venue.toFixed(2)}}</p>
                            </div>
                            <div class="bg-slate-900/60 p-2 rounded-lg">
                                <p class="text-[10px] text-indigo-400">Wicket%</p>
                                <p class="text-xs font-bold text-indigo-400">${{b.hp_wkt_rate.toFixed(1)}}%</p>
                            </div>
                        </div>
                    `;
                    cards.appendChild(card);
                }}
            }});
        }}

        function renderQuadrantCharts() {{
            // Batters Plot
            const batTracePool = {{
                x: allActiveBatters.map(d => d.delta_sr_baseline),
                y: allActiveBatters.map(d => d.delta_sr_venue),
                text: allActiveBatters.map(d => d.player_name + ' (HP Balls: ' + d.hp_balls + ')'),
                mode: 'markers',
                marker: {{ size: 8, color: '#64748b', opacity: 0.5 }},
                name: 'Active Pool'
            }};
            const batTraceTop = {{
                x: top10Batters.map(d => d.delta_sr_baseline),
                y: top10Batters.map(d => d.delta_sr_venue),
                text: top10Batters.map(d => '<b>' + d.player_name + '</b><br>CBPS: +' + d.cbps_score_v3),
                mode: 'markers+text',
                textposition: 'top center',
                textfont: {{ family: 'Inter', size: 10, color: '#f8fafc' }},
                marker: {{ size: 14, color: '#e4007c', line: {{ color: '#ffffff', width: 1.5 }} }},
                name: 'Top 10 Active Batters'
            }};
            const layoutBat = {{
                paper_bgcolor: 'transparent',
                plot_bgcolor: 'transparent',
                margin: {{ t: 20, r: 20, b: 50, l: 50 }},
                xaxis: {{ title: 'Baseline Delta (&Delta;SR)', gridcolor: '#1e293b', zerolinecolor: '#475569', color: '#94a3b8' }},
                yaxis: {{ title: 'Venue Par Delta (&Delta;SR)', gridcolor: '#1e293b', zerolinecolor: '#475569', color: '#94a3b8' }},
                legend: {{ font: {{ color: '#94a3b8' }}, x: 0.05, y: 0.95 }}
            }};
            Plotly.newPlot('plot-batters-matrix', [batTracePool, batTraceTop], layoutBat, {{ responsive: true, displayModeBar: false }});

            // Bowlers Plot
            const bowlTracePool = {{
                x: allActiveBowlers.map(d => d.hp_wkt_rate),
                y: allActiveBowlers.map(d => d.delta_econ_venue),
                text: allActiveBowlers.map(d => d.player_name + ' (HP Balls: ' + d.hp_balls + ')'),
                mode: 'markers',
                marker: {{ size: 8, color: '#64748b', opacity: 0.5 }},
                name: 'Active Pool'
            }};
            const bowlTraceTop = {{
                x: top10Bowlers.map(d => d.hp_wkt_rate),
                y: top10Bowlers.map(d => d.delta_econ_venue),
                text: top10Bowlers.map(d => '<b>' + d.player_name + '</b><br>CBPS: +' + d.cbps_score_v3),
                mode: 'markers+text',
                textposition: 'top center',
                textfont: {{ family: 'Inter', size: 10, color: '#f8fafc' }},
                marker: {{ size: 14, color: '#10b981', line: {{ color: '#ffffff', width: 1.5 }} }},
                name: 'Top 10 Active Bowlers'
            }};
            const layoutBowl = {{
                paper_bgcolor: 'transparent',
                plot_bgcolor: 'transparent',
                margin: {{ t: 20, r: 20, b: 50, l: 50 }},
                xaxis: {{ title: 'Wicket Take Rate (% per Ball)', gridcolor: '#1e293b', zerolinecolor: '#475569', color: '#94a3b8' }},
                yaxis: {{ title: 'Venue Econ Suppression (&Delta;Econ)', gridcolor: '#1e293b', zerolinecolor: '#475569', color: '#94a3b8' }},
                legend: {{ font: {{ color: '#94a3b8' }}, x: 0.70, y: 0.95 }}
            }};
            Plotly.newPlot('plot-bowlers-matrix', [bowlTracePool, bowlTraceTop], layoutBowl, {{ responsive: true, displayModeBar: false }});
        }}

        // Initialize
        document.addEventListener('DOMContentLoaded', () => {{
            populateBatters();
            populateBowlers();
        }});
    </script>
</body>
</html>
"""
    dash_path = 'rr-submission/v3/dashboard/index.html'
    with open(dash_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Interactive Web Dashboard (v3) successfully created at: {dash_path}")

if __name__ == '__main__':
    build_v3_dashboard()

