import pandas as pd
import json
import os

def build_v4_dashboard():
    print("=" * 60)
    print("STAGE 5 (v4): Building Interactive Dashboard with Direct Table Toggle")
    print("=" * 60)
    
    top_bat_csv = 'rr-submission/v4/stage4_consistency_scoring/top10_batters_v4_final.csv'
    top_bowl_csv = 'rr-submission/v4/stage4_consistency_scoring/top10_bowlers_v4_final.csv'
    active_bat_csv = 'rr-submission/v4/stage4_consistency_scoring/active_batters_v4_master.csv'
    active_bowl_csv = 'rr-submission/v4/stage4_consistency_scoring/active_bowlers_v4_master.csv'
    
    df_top_bat = pd.read_csv(top_bat_csv)
    df_top_bowl = pd.read_csv(top_bowl_csv)
    df_active_bat = pd.read_csv(active_bat_csv)
    df_active_bowl = pd.read_csv(active_bowl_csv)
    
    top10_bat_list = df_top_bat.to_dict(orient='records')
    top10_bowl_list = df_top_bowl.to_dict(orient='records')
    all_bat_list = df_active_bat.to_dict(orient='records')
    all_bowl_list = df_active_bowl.to_dict(orient='records')
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rajasthan Royals SupeRR Selector Season 2 | Unified Pressure Model Dashboard (v4)</title>
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
                        <span class="text-xs px-2.5 py-0.5 rounded-full bg-pink-500/20 text-pink-400 border border-pink-500/30 font-semibold">Model v4 (Unified Contextual Engine)</span>
                    </h1>
                    <p class="text-xs text-slate-400">Opposition Tiering &bull; Chase Asymmetry &bull; Tactical Cohorts &bull; 17 Stadium Pars</p>
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

        <!-- Unified Architecture Banner -->
        <div class="glass-card rounded-2xl p-4 border border-pink-500/30 bg-pink-950/10 flex flex-wrap items-center justify-between gap-4">
            <div class="flex items-start space-x-3">
                <div class="p-2 rounded-xl bg-pink-500/20 text-pink-400 border border-pink-500/30 font-bold text-lg">
                    ★
                </div>
                <div>
                    <h3 class="text-sm font-bold text-pink-300">Model v4 Unified Architecture with Direct Table Toggles</h3>
                    <p class="text-xs text-slate-300 mt-0.5 leading-relaxed">
                        Default view displays the <b>Round 1 Official Rankings</b> (100% active contracted players, MS Dhoni & Dinesh Karthik excluded). Use the toggle switches directly on top of the tables or the bar below to filter for <b>Free / Unretained Players</b> and <b>RR Home Ground Calibration (Jaipur SMS & Guwahati)</b>.
                    </p>
                </div>
            </div>
            <div class="text-xs font-semibold px-3 py-1.5 rounded-lg bg-slate-900 text-slate-300 border border-slate-700">
                Production Scouting Grade
            </div>
        </div>

        <!-- Venue Baseline Bar -->
        <div class="glass-card rounded-2xl p-3.5 border border-slate-800 bg-slate-900/80 flex flex-wrap items-center justify-between gap-4">
            <div class="flex items-center gap-3">
                <span class="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
                    <span class="w-2 h-2 rounded-full bg-indigo-500"></span>
                    Stadium Par Calibration:
                </span>
                <div class="inline-flex rounded-xl p-1 bg-slate-950 border border-slate-800 text-xs">
                    <button onclick="setVenueScope('all')" id="venue-all" class="px-3.5 py-1 rounded-lg font-bold bg-indigo-600 text-white shadow transition-all">
                        All 17 IPL Stadiums (Standard)
                    </button>
                    <button onclick="setVenueScope('rr_home')" id="venue-rr" class="px-3.5 py-1 rounded-lg font-medium text-slate-400 hover:text-white transition-all">
                        RR Home Fortress (Jaipur SMS & Guwahati)
                    </button>
                </div>
            </div>

            <div id="mode-text" class="text-xs text-slate-400 font-medium">
                Scope: <b class="text-pink-400">All Active Candidates</b> &bull; <b class="text-indigo-400">All 17 Stadiums</b>
            </div>
        </div>

        <!-- Navigation Tabs -->
        <div class="flex items-center space-x-2 border-b border-slate-800 pb-2">
            <button onclick="switchTab('batters')" id="tab-batters" class="tab-btn active px-4 py-2 rounded-xl text-xs font-semibold transition-all">
                Top 10 Batters
            </button>
            <button onclick="switchTab('bowlers')" id="tab-bowlers" class="tab-btn px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white transition-all">
                Top 10 Bowlers
            </button>
            <button onclick="switchTab('quadrant')" id="tab-quadrant" class="tab-btn px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white transition-all">
                Clutch Quadrants (v4)
            </button>
            <button onclick="switchTab('methodology')" id="tab-methodology" class="tab-btn px-4 py-2 rounded-xl text-xs font-semibold text-slate-400 hover:text-white transition-all">
                v4 Methodology & Verification
            </button>
        </div>

        <!-- BATTERS TAB -->
        <section id="sec-batters" class="space-y-6">
            <div class="glass-card rounded-2xl p-5 border border-slate-800">
                <!-- Table Header with DIRECT FREE PLAYERS TOGGLE -->
                <div class="flex flex-wrap justify-between items-center gap-3 mb-4 pb-3 border-b border-slate-800/80">
                    <div>
                        <h2 class="text-base font-bold text-white flex items-center gap-2" id="batters-header-title">
                            Top 10 Batters Performing Under Pressure (Model v4)
                        </h2>
                        <p class="text-xs text-slate-400" id="batters-header-desc">
                            Blends Opposition-Adjusted SR, Venue Par Outperformance, Baseline Delta, Dot Minimization & Match Consistency.
                        </p>
                    </div>

                    <!-- Direct Toggle for Free / Unretained Players -->
                    <div class="flex items-center gap-2.5 bg-slate-950/90 px-3.5 py-1.5 rounded-xl border border-slate-800 shadow-sm">
                        <span class="text-xs font-bold text-slate-300 flex items-center gap-1.5">
                            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                            Show Free / Unretained Players:
                        </span>
                        <button onclick="toggleFreeOnly()" id="free-toggle-batters" class="px-3.5 py-1 rounded-lg text-xs font-extrabold transition-all bg-slate-800 text-slate-400 border border-slate-700 hover:border-slate-500">
                            OFF
                        </button>
                    </div>
                </div>

                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs">
                        <thead class="bg-slate-900/80 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
                            <tr>
                                <th class="p-3">Rank</th>
                                <th class="p-3">Player Name</th>
                                <th class="p-3">Roster Status</th>
                                <th class="p-3">HP Balls</th>
                                <th class="p-3">HP Strike Rate</th>
                                <th class="p-3 text-pink-400">Opp-Adjusted SR</th>
                                <th class="p-3 text-indigo-400">&Delta; Venue Par</th>
                                <th class="p-3">&Delta; Baseline</th>
                                <th class="p-3">Consistency</th>
                                <th class="p-3 text-right">Effective Score</th>
                            </tr>
                        </thead>
                        <tbody id="batters-tbody" class="divide-y divide-slate-800/60 font-medium">
                        </tbody>
                    </table>
                </div>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4" id="batters-cards">
            </div>
        </section>

        <!-- BOWLERS TAB -->
        <section id="sec-bowlers" class="space-y-6 hidden">
            <div class="glass-card rounded-2xl p-5 border border-slate-800">
                <!-- Table Header with DIRECT FREE PLAYERS TOGGLE -->
                <div class="flex flex-wrap justify-between items-center gap-3 mb-4 pb-3 border-b border-slate-800/80">
                    <div>
                        <h2 class="text-base font-bold text-white flex items-center gap-2" id="bowlers-header-title">
                            Top 10 Bowlers Performing Under Pressure (Model v4)
                        </h2>
                        <p class="text-xs text-slate-400" id="bowlers-header-desc">
                            Evaluates Venue Economy Suppression, Top/Middle-Order Wicket Threat, Dot Pressure & Match Reliability.
                        </p>
                    </div>

                    <!-- Direct Toggle for Free / Unretained Players -->
                    <div class="flex items-center gap-2.5 bg-slate-950/90 px-3.5 py-1.5 rounded-xl border border-slate-800 shadow-sm">
                        <span class="text-xs font-bold text-slate-300 flex items-center gap-1.5">
                            <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                            Show Free / Unretained Players:
                        </span>
                        <button onclick="toggleFreeOnly()" id="free-toggle-bowlers" class="px-3.5 py-1 rounded-lg text-xs font-extrabold transition-all bg-slate-800 text-slate-400 border border-slate-700 hover:border-slate-500">
                            OFF
                        </button>
                    </div>
                </div>

                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs">
                        <thead class="bg-slate-900/80 text-slate-400 uppercase text-[10px] tracking-wider border-b border-slate-800">
                            <tr>
                                <th class="p-3">Rank</th>
                                <th class="p-3">Player Name</th>
                                <th class="p-3">Roster Status</th>
                                <th class="p-3">HP Balls</th>
                                <th class="p-3">HP Economy</th>
                                <th class="p-3 text-emerald-400">&Delta; Venue Par Econ</th>
                                <th class="p-3 text-indigo-400">&Delta; Baseline Econ</th>
                                <th class="p-3">Quality Wkt Rate</th>
                                <th class="p-3">Consistency</th>
                                <th class="p-3 text-right">Effective Score</th>
                            </tr>
                        </thead>
                        <tbody id="bowlers-tbody" class="divide-y divide-slate-800/60 font-medium">
                        </tbody>
                    </table>
                </div>
            </div>

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
                    <h3 class="text-sm font-bold text-white mb-2">Bowler Clutch Matrix (Venue Economy Suppression vs Quality Wickets)</h3>
                    <p class="text-xs text-slate-400 mb-4">Upper-right quadrant represents rare hybrid run-stranglers and wicket-takers.</p>
                    <div id="plot-bowlers-matrix" style="height: 420px;"></div>
                </div>
            </div>
        </section>

        <!-- METHODOLOGY & AUDIT TAB -->
        <section id="sec-methodology" class="space-y-6 hidden">
            <div class="glass-card rounded-2xl p-6 border border-slate-800 space-y-4">
                <h2 class="text-base font-bold text-pink-400">Methodology Architecture & Dual-Toggle Engine (Model v4)</h2>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs text-slate-300">
                    <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
                        <span class="font-bold text-white block text-sm">1. Opposition Quality Tiering</span>
                        <p>Batters facing 53 elite bowlers receive an opposition quality uplift (1.15&times;), while dismissals of tailenders (#7–#11) are discounted (0.70&times;) for bowlers:</p>
                        <code class="block bg-slate-950 p-2 rounded text-[11px] text-pink-300">Runs_opp = Runs &times; BowlerTierMult</code>
                    </div>

                    <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
                        <span class="font-bold text-white block text-sm">2. Rajasthan Royals Home Fortress</span>
                        <p>Calibrates player output on Sawai Mansingh Stadium (Jaipur SMS) and Barsapara (Guwahati) tracks:</p>
                        <code class="block bg-slate-950 p-2 rounded text-[11px] text-indigo-300">Score_RR = 0.65&times;CBPS + 0.35&times;&Delta;Jaipur</code>
                        <p>Rewards long-boundary power and spin containment.</p>
                    </div>

                    <div class="p-4 rounded-xl bg-slate-900/60 border border-slate-800 space-y-2">
                        <span class="font-bold text-white block text-sm">3. Dynamic Free / Unretained Player Toggle</span>
                        <p>Allows scouts to toggle seamlessly between the official Round 1 global rankings and an unretained auction target radar.</p>
                    </div>
                </div>
            </div>
        </section>

    </main>

    <!-- Footer -->
    <footer class="border-t border-slate-800 bg-slate-950/80 py-4 text-center text-xs text-slate-500">
        <p>Rajasthan Royals SupeRR Selector Season 2 | Round 1 Submission Model v4</p>
        <p class="mt-1">Candidate: <b>Mohammed Aleem Bukkapatnam</b> (M.S. in Artificial Intelligence) | Email: <a href="mailto:mohammedaleem1404@gmail.com" class="text-pink-400 hover:underline">mohammedaleem1404@gmail.com</a></p>
    </footer>

    <!-- Client-side Interactive Filter Engine -->
    <script>
        const allBatters = {json.dumps(all_bat_list)};
        const allBowlers = {json.dumps(all_bowl_list)};

        let isFreeOnly = false;
        let currentVenueScope = 'all';  // 'all' or 'rr_home'

        function toggleFreeOnly() {{
            isFreeOnly = !isFreeOnly;
            updateToggleButtons();
            updateViews();
        }}

        function updateToggleButtons() {{
            const btns = ['free-toggle-batters', 'free-toggle-bowlers'];
            btns.forEach(id => {{
                const el = document.getElementById(id);
                if (el) {{
                    if (isFreeOnly) {{
                        el.innerText = 'ON';
                        el.className = 'px-3.5 py-1 rounded-lg text-xs font-extrabold transition-all bg-emerald-500 text-slate-950 shadow-lg shadow-emerald-500/30 border border-emerald-400';
                    }} else {{
                        el.innerText = 'OFF';
                        el.className = 'px-3.5 py-1 rounded-lg text-xs font-extrabold transition-all bg-slate-800 text-slate-400 border border-slate-700 hover:border-slate-500';
                    }}
                }}
            }});
        }}

        function setVenueScope(scope) {{
            currentVenueScope = scope;
            document.getElementById('venue-all').className = scope === 'all' 
                ? 'px-3.5 py-1 rounded-lg font-bold bg-indigo-600 text-white shadow transition-all'
                : 'px-3.5 py-1 rounded-lg font-medium text-slate-400 hover:text-white transition-all';
            document.getElementById('venue-rr').className = scope === 'rr_home' 
                ? 'px-3.5 py-1 rounded-lg font-bold bg-indigo-600 text-white shadow transition-all'
                : 'px-3.5 py-1 rounded-lg font-medium text-slate-400 hover:text-white transition-all';
            updateViews();
        }}

        function getFilteredBatters() {{
            let pool = allBatters.filter(b => b.hp_balls >= 180);
            if (isFreeOnly) {{
                pool = pool.filter(b => b.is_auction_target);
            }}
            const scoreKey = currentVenueScope === 'rr_home' ? 'rr_home_score' : 'cbps_score_v4';
            return pool.sort((a, b) => b[scoreKey] - a[scoreKey]).slice(0, 10);
        }}

        function getFilteredBowlers() {{
            let pool = allBowlers.filter(b => b.hp_balls >= 180);
            if (isFreeOnly) {{
                pool = pool.filter(b => b.is_auction_target);
            }}
            const scoreKey = currentVenueScope === 'rr_home' ? 'rr_home_score' : 'cbps_score_v4';
            return pool.sort((a, b) => b[scoreKey] - a[scoreKey]).slice(0, 10);
        }}

        function updateViews() {{
            const scoreKey = currentVenueScope === 'rr_home' ? 'rr_home_score' : 'cbps_score_v4';
            const rosterLabel = isFreeOnly ? 'Free / Unretained Players Only' : 'All Active Contenders (Round 1 Official)';
            const venueLabel = currentVenueScope === 'all' ? 'All 17 Stadiums' : 'RR Home Grounds (Jaipur SMS & Guwahati)';
            
            document.getElementById('mode-text').innerHTML = `Scope: <b class="${{isFreeOnly ? 'text-emerald-400' : 'text-pink-400'}}">${{rosterLabel}}</b> &bull; <b class="text-indigo-400">${{venueLabel}}</b>`;
            
            document.getElementById('batters-header-title').innerHTML = isFreeOnly 
                ? 'Top 10 Free / Unretained Batters in Auction Pool (RR Targets)'
                : 'Top 10 Batters Performing Under Pressure (Model v4)';

            document.getElementById('bowlers-header-title').innerHTML = isFreeOnly 
                ? 'Top 10 Free / Unretained Bowlers in Auction Pool (RR Targets)'
                : 'Top 10 Bowlers Performing Under Pressure (Model v4)';

            renderBatters(getFilteredBatters(), scoreKey);
            renderBowlers(getFilteredBowlers(), scoreKey);
            renderQuadrantCharts();
        }}

        function renderBatters(batters, scoreKey) {{
            const tbody = document.getElementById('batters-tbody');
            const cards = document.getElementById('batters-cards');
            tbody.innerHTML = '';
            cards.innerHTML = '';

            batters.forEach((b, idx) => {{
                const rank = idx + 1;
                const score = b[scoreKey];
                const isRR = b.team_status && b.team_status.includes('RR');
                const isAuction = b.is_auction_target;

                const row = document.createElement('tr');
                row.className = isRR ? 'bg-pink-950/20 text-white border-l-4 border-pink-500' : 'hover:bg-slate-900/50';
                row.innerHTML = `
                    <td class="p-3 font-bold text-slate-400">${{rank}}</td>
                    <td class="p-3 font-bold text-white flex items-center gap-1.5">
                        ${{b.player_name}}
                        ${{isRR ? '<span class="px-1.5 py-0.5 rounded text-[9px] bg-pink-500/20 text-pink-400 border border-pink-500/30">RR</span>' : ''}}
                    </td>
                    <td class="p-3">
                        <span class="px-2 py-0.5 rounded text-[10px] font-medium ${{isAuction ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-slate-800 text-slate-300'}}">
                            ${{b.team_status || 'Active'}}
                        </span>
                    </td>
                    <td class="p-3 text-slate-300">${{b.hp_balls}}</td>
                    <td class="p-3 text-slate-300">${{b.hp_sr.toFixed(1)}}</td>
                    <td class="p-3 font-bold text-pink-400">${{b.hp_opp_sr.toFixed(1)}}</td>
                    <td class="p-3 text-pink-400 font-semibold">+${{b.delta_sr_venue.toFixed(1)}}</td>
                    <td class="p-3 text-indigo-400 font-semibold">+${{b.delta_sr_baseline.toFixed(1)}}</td>
                    <td class="p-3 text-emerald-400 font-semibold">${{(b.consistency_rate * 100).toFixed(0)}}%</td>
                    <td class="p-3 text-right font-extrabold text-pink-400 text-sm">+${{score.toFixed(2)}}</td>
                `;
                tbody.appendChild(row);

                if (rank <= 6) {{
                    const card = document.createElement('div');
                    card.className = 'glass-card p-4 rounded-xl border border-slate-800 space-y-2';
                    card.innerHTML = `
                        <div class="flex justify-between items-start">
                            <div>
                                <span class="text-[10px] text-pink-400 font-bold uppercase tracking-wider">Rank #${{rank}}</span>
                                <h4 class="text-sm font-bold text-white">${{b.player_name}}</h4>
                                <span class="text-[10px] text-slate-400">${{b.team_status || 'Active'}}</span>
                            </div>
                            <span class="text-xs px-2 py-0.5 rounded bg-pink-500/10 text-pink-400 border border-pink-500/20 font-bold">
                                +${{score.toFixed(2)}}
                            </span>
                        </div>
                        <div class="grid grid-cols-3 gap-2 pt-1 text-center">
                            <div class="bg-slate-900/60 p-2 rounded-lg">
                                <p class="text-[10px] text-slate-400">Opp-SR</p>
                                <p class="text-xs font-bold text-white">${{b.hp_opp_sr.toFixed(1)}}</p>
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

        function renderBowlers(bowlers, scoreKey) {{
            const tbody = document.getElementById('bowlers-tbody');
            const cards = document.getElementById('bowlers-cards');
            tbody.innerHTML = '';
            cards.innerHTML = '';

            bowlers.forEach((b, idx) => {{
                const rank = idx + 1;
                const score = b[scoreKey];
                const isRR = b.team_status && b.team_status.includes('RR');
                const isAuction = b.is_auction_target;

                const row = document.createElement('tr');
                row.className = rank === 1 ? 'bg-emerald-950/20 text-white border-l-4 border-emerald-500' : 'hover:bg-slate-900/50';
                row.innerHTML = `
                    <td class="p-3 font-bold text-slate-400">${{rank}}</td>
                    <td class="p-3 font-bold text-white">${{b.player_name}}</td>
                    <td class="p-3">
                        <span class="px-2 py-0.5 rounded text-[10px] font-medium ${{isAuction ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' : 'bg-slate-800 text-slate-300'}}">
                            ${{b.team_status || 'Active'}}
                        </span>
                    </td>
                    <td class="p-3 text-slate-300">${{b.hp_balls}}</td>
                    <td class="p-3 font-bold text-white">${{b.hp_econ.toFixed(2)}}</td>
                    <td class="p-3 text-emerald-400 font-semibold">+${{b.delta_econ_venue.toFixed(2)}}</td>
                    <td class="p-3 text-indigo-400 font-semibold">${{b.delta_econ_baseline > 0 ? '+' : ''}}${{b.delta_econ_baseline.toFixed(2)}}</td>
                    <td class="p-3 text-slate-300">${{b.hp_wkt_rate.toFixed(1)}}%</td>
                    <td class="p-3 text-emerald-400 font-semibold">${{(b.consistency_rate * 100).toFixed(0)}}%</td>
                    <td class="p-3 text-right font-extrabold text-emerald-400 text-sm">+${{score.toFixed(2)}}</td>
                `;
                tbody.appendChild(row);

                if (rank <= 6) {{
                    const card = document.createElement('div');
                    card.className = 'glass-card p-4 rounded-xl border border-slate-800 space-y-2';
                    card.innerHTML = `
                        <div class="flex justify-between items-start">
                            <div>
                                <span class="text-[10px] text-emerald-400 font-bold uppercase tracking-wider">Rank #${{rank}}</span>
                                <h4 class="text-sm font-bold text-white">${{b.player_name}}</h4>
                                <span class="text-[10px] text-slate-400">${{b.team_status || 'Active'}}</span>
                            </div>
                            <span class="text-xs px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-bold">
                                +${{score.toFixed(2)}}
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
                                <p class="text-[10px] text-indigo-400">Quality Wkt%</p>
                                <p class="text-xs font-bold text-indigo-400">${{b.hp_wkt_rate.toFixed(1)}}%</p>
                            </div>
                        </div>
                    `;
                    cards.appendChild(card);
                }}
            }});
        }}

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

        function renderQuadrantCharts() {{
            const currentBatters = getFilteredBatters();
            const currentBowlers = getFilteredBowlers();

            const batTracePool = {{
                x: allBatters.map(d => d.delta_sr_baseline),
                y: allBatters.map(d => d.delta_sr_venue),
                text: allBatters.map(d => d.player_name + ' (' + (d.team_status || 'Active') + ')'),
                mode: 'markers',
                marker: {{ size: 8, color: '#64748b', opacity: 0.5 }},
                name: 'Player Pool'
            }};
            const batTraceTop = {{
                x: currentBatters.map(d => d.delta_sr_baseline),
                y: currentBatters.map(d => d.delta_sr_venue),
                text: currentBatters.map(d => '<b>' + d.player_name + '</b><br>' + (d.team_status || '')),
                mode: 'markers+text',
                textposition: 'top center',
                textfont: {{ family: 'Inter', size: 10, color: '#f8fafc' }},
                marker: {{ size: 14, color: '#e4007c', line: {{ color: '#ffffff', width: 1.5 }} }},
                name: isFreeOnly ? 'Top 10 Free / Unretained Batters' : 'Top 10 Batters (Official)'
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

            const bowlTracePool = {{
                x: allBowlers.map(d => d.hp_wkt_rate),
                y: allBowlers.map(d => d.delta_econ_venue),
                text: allBowlers.map(d => d.player_name + ' (' + (d.team_status || 'Active') + ')'),
                mode: 'markers',
                marker: {{ size: 8, color: '#64748b', opacity: 0.5 }},
                name: 'Player Pool'
            }};
            const bowlTraceTop = {{
                x: currentBowlers.map(d => d.hp_wkt_rate),
                y: currentBowlers.map(d => d.delta_econ_venue),
                text: currentBowlers.map(d => '<b>' + d.player_name + '</b><br>' + (d.team_status || '')),
                mode: 'markers+text',
                textposition: 'top center',
                textfont: {{ family: 'Inter', size: 10, color: '#f8fafc' }},
                marker: {{ size: 14, color: '#10b981', line: {{ color: '#ffffff', width: 1.5 }} }},
                name: isFreeOnly ? 'Top 10 Free / Unretained Bowlers' : 'Top 10 Bowlers (Official)'
            }};
            const layoutBowl = {{
                paper_bgcolor: 'transparent',
                plot_bgcolor: 'transparent',
                margin: {{ t: 20, r: 20, b: 50, l: 50 }},
                xaxis: {{ title: 'Quality Wicket Rate (% per Ball)', gridcolor: '#1e293b', zerolinecolor: '#475569', color: '#94a3b8' }},
                yaxis: {{ title: 'Venue Econ Suppression (&Delta;Econ)', gridcolor: '#1e293b', zerolinecolor: '#475569', color: '#94a3b8' }},
                legend: {{ font: {{ color: '#94a3b8' }}, x: 0.70, y: 0.95 }}
            }};
            Plotly.newPlot('plot-bowlers-matrix', [bowlTracePool, bowlTraceTop], layoutBowl, {{ responsive: true, displayModeBar: false }});
        }}

        document.addEventListener('DOMContentLoaded', () => {{
            updateViews();
        }});
    </script>
</body>
</html>
"""
    dash_path = 'rr-submission/v4/dashboard/index.html'
    with open(dash_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    print(f"Interactive Web Dashboard (v4 with Direct Table Toggles) successfully created at: {dash_path}")

if __name__ == '__main__':
    build_v4_dashboard()
