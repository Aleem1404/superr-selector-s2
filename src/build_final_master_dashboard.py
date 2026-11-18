import pandas as pd
import json
import os

def build_final_master_dashboard():
    print("=" * 60)
    print("Building FINAL MASTER DASHBOARD with Full Multi-Version Comparison")
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
    
    # Version comparison data
    v_batters = [
        {"rank": 1, "v1": "MS Dhoni", "v1_s": 1.64, "v2": "Naman Dhir", "v2_s": 1.48, "v3": "Naman Dhir", "v3_s": 1.48, "v4": "Naman Dhir", "v4_s": 1.60, "note": "Retains #1: Opp-Adjusted SR rises to 200.17 (+51.9 vs par)"},
        {"rank": 2, "v1": "Naman Dhir", "v1_s": 1.49, "v2": "Ashutosh Sharma", "v2_s": 1.38, "v3": "Ashutosh Sharma", "v3_s": 1.38, "v4": "Ashutosh Sharma", "v4_s": 1.27, "note": "Crisis Enforcer (+85.2 baseline elevation in chases)"},
        {"rank": 3, "v1": "Jos Buttler", "v1_s": 1.38, "v2": "Jos Buttler", "v2_s": 1.36, "v3": "Jos Buttler", "v3_s": 1.36, "v4": "Suryakumar Yadav", "v4_s": 1.25, "note": "Climbs to #3: 190.31 Opp-Adjusted SR across 669 HP balls"},
        {"rank": 4, "v1": "Ashutosh Sharma", "v1_s": 1.35, "v2": "MS Dhoni", "v2_s": 1.32, "v3": "Suryakumar Yadav", "v3_s": 1.26, "v4": "Jos Buttler", "v4_s": 1.11, "note": "Elite Anchor: 182.57 Opp-Adjusted SR, 88.2% consistency"},
        {"rank": 5, "v1": "Dinesh Karthik", "v1_s": 1.30, "v2": "Suryakumar Yadav", "v2_s": 1.26, "v3": "Shreyas Iyer", "v3_s": 1.00, "v4": "Glenn Phillips", "v4_s": 1.07, "note": "Climbs to #5: 184.71 Opp-SR (+36.44 vs venue par)"},
        {"rank": 6, "v1": "Suryakumar Yadav", "v1_s": 1.12, "v2": "Dinesh Karthik", "v2_s": 1.15, "v3": "Glenn Phillips", "v3_s": 0.90, "v4": "Donovan Ferreira", "v4_s": 1.07, "note": "New Entry in Top 6: +58.82 baseline elevation vs pace"},
        {"rank": 7, "v1": "Matthew Wade", "v1_s": 0.82, "v2": "Shreyas Iyer", "v2_s": 1.00, "v3": "Dhruv Jurel", "v3_s": 0.89, "v4": "Shreyas Iyer", "v4_s": 0.97, "note": "Championship Anchor: 177.30 Opp-SR across 459 balls"},
        {"rank": 8, "v1": "Donovan Ferreira", "v1_s": 0.80, "v2": "Glenn Phillips", "v2_s": 0.90, "v3": "Marcus Stoinis", "v3_s": 0.82, "v4": "Sai Sudharsan", "v4_s": 0.84, "note": "New Entry in Top 8: 90.9% match reliability anchor"},
        {"rank": 9, "v1": "Shashank Singh", "v1_s": 0.75, "v2": "Dhruv Jurel", "v2_s": 0.89, "v3": "Tristan Stubbs", "v3_s": 0.81, "v4": "Shashank Singh", "v4_s": 0.84, "note": "Finisher: 174.10 Opp-SR (+52.67 baseline delta)"},
        {"rank": 10, "v1": "Sai Sudharsan", "v1_s": 0.74, "v2": "Matthew Wade", "v2_s": 0.84, "v3": "Tim David", "v3_s": 0.76, "v4": "Tim David", "v4_s": 0.81, "note": "Death Finisher: 729 HP balls, 181.47 Opp-SR, 82.1% consistency"}
    ]
    
    v_bowlers = [
        {"rank": 1, "v1": "Sunil Narine", "v1_s": 1.32, "v2": "Sunil Narine", "v2_s": 1.61, "v3": "Sunil Narine", "v3_s": 1.61, "v4": "Sunil Narine", "v4_s": 1.38, "note": "Undisputed #1: 6.63 HP Econ (+2.45 below venue par)"},
        {"rank": 2, "v1": "Matheesha Pathirana", "v1_s": 1.00, "v2": "Matheesha Pathirana", "v2_s": 1.08, "v3": "Matheesha Pathirana", "v3_s": 1.08, "v4": "Matheesha Pathirana", "v4_s": 1.13, "note": "Slingshot Yorker Enforcer: 9.4% quality wicket rate"},
        {"rank": 3, "v1": "Jasprit Bumrah", "v1_s": 0.94, "v2": "Jasprit Bumrah", "v2_s": 0.97, "v3": "Jasprit Bumrah", "v3_s": 0.97, "v4": "Mitchell Santner", "v4_s": 1.12, "note": "Climbs to #3: 7.30 Econ (+1.97 vs par), 96.2% consistency"},
        {"rank": 4, "v1": "Wanindu Hasaranga", "v1_s": 0.94, "v2": "Mitchell Santner", "v2_s": 0.89, "v3": "Mitchell Santner", "v3_s": 0.89, "v4": "Akeal Hosein", "v4_s": 0.99, "note": "New Entry in Top 4: 7.38 Econ (+1.84 vs par), 8.07% wkt rate"},
        {"rank": 5, "v1": "Mitchell Santner", "v1_s": 0.83, "v2": "Rashid Khan", "v2_s": 0.81, "v3": "Rashid Khan", "v3_s": 0.81, "v4": "Rashid Khan", "v4_s": 0.93, "note": "High-Leverage Strike Spinner over 910 pressure balls"},
        {"rank": 6, "v1": "Rashid Khan", "v1_s": 0.79, "v2": "Varun Chakravarthy", "v2_s": 0.79, "v3": "Varun Chakravarthy", "v3_s": 0.79, "v4": "Jasprit Bumrah", "v4_s": 0.92, "note": "Gold Standard: 7.42 HP Econ (+1.68 below venue par)"},
        {"rank": 7, "v1": "Taskin Ahmed", "v1_s": 0.79, "v2": "Taskin Ahmed", "v2_s": 0.75, "v3": "Taskin Ahmed", "v3_s": 0.75, "v4": "Wanindu Hasaranga", "v4_s": 0.81, "note": "Returns to Top 7: 9.52% wicket rate in middle overs"},
        {"rank": 8, "v1": "Mitchell Starc", "v1_s": 0.75, "v2": "Jamie Overton", "v2_s": 0.69, "v3": "Jamie Overton", "v3_s": 0.69, "v4": "Taskin Ahmed", "v4_s": 0.77, "note": "Hard-Length Enforcer: 8.61 Econ, 8.91% wicket rate"},
        {"rank": 9, "v1": "Jamie Overton", "v1_s": 0.68, "v2": "Mitchell Starc", "v2_s": 0.68, "v3": "Mitchell Starc", "v3_s": 0.68, "v4": "Sikandar Raza", "v4_s": 0.77, "note": "New Entry in Top 9: 7.22 Econ (+1.93 vs par), 91.7% consistency"},
        {"rank": 10, "v1": "Varun Chakravarthy", "v1_s": 0.61, "v2": "Rasikh Salam", "v2_s": 0.66, "v3": "Rasikh Salam", "v3_s": 0.66, "v4": "Varun Chakravarthy", "v4_s": 0.75, "note": "Retains Top 10: 93.9% spell consistency over 706 balls"}
    ]

    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rajasthan Royals SupeRR Selector Season 2 | Final Master Dashboard</title>
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
        .v-badge {{
            display: inline-block;
            padding: 2px 6px;
            border-radius: 4px;
            font-size: 10px;
            font-weight: 700;
        }}
    </style>
</head>
<body class="min-h-screen flex flex-col">

    <!-- Top Header -->
    <header class="border-b border-slate-800 bg-slate-950/90 sticky top-0 z-50 backdrop-blur-md">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3.5 flex flex-wrap justify-between items-center gap-4">
            <div class="flex items-center space-x-3">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-pink-600 to-indigo-900 flex items-center justify-center font-extrabold text-white shadow-lg text-lg">
                    RR
                </div>
                <div>
                    <h1 class="text-lg font-bold text-white flex items-center gap-2">
                        SupeRR Selector Season 2 
                        <span class="text-xs px-2.5 py-0.5 rounded-full bg-pink-500/20 text-pink-400 border border-pink-500/30 font-semibold">Final Master Version (v1 &ndash; v4)</span>
                    </h1>
                    <p class="text-xs text-slate-400">Contextual Pressure Modeling &bull; Multi-Version Evolution &bull; Real-Time Auction Recommendations</p>
                </div>
            </div>
            
            <div class="flex items-center space-x-3 text-xs text-slate-300">
                <div class="bg-slate-900 border border-slate-800 px-3 py-1.5 rounded-lg flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-pink-500 animate-pulse"></span>
                    <span>Candidate: <b class="text-white">Mohammed Aleem Bukkapatnam</b> (M.S. in AI)</span>
                </div>
                <a href="https://github.com/Aleem1404/superr-selector-s2" target="_blank" class="bg-pink-600/20 border border-pink-500/40 text-pink-300 hover:bg-pink-600/30 px-3 py-1.5 rounded-lg font-semibold flex items-center gap-1.5 transition">
                    <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 24 24"><path fill-rule="evenodd" clip-rule="evenodd" d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.53 1.032 1.53 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"/></svg>
                    GitHub
                </a>
            </div>
        </div>
    </header>

    <!-- Main Container -->
    <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6 flex-1 w-full space-y-6">

        <!-- Unified Architecture Banner -->
        <div class="glass-card rounded-2xl p-4 border border-pink-500/30 bg-pink-950/10 flex flex-wrap items-center justify-between gap-4">
            <div class="flex items-start space-x-3">
                <div class="p-2 rounded-lg bg-pink-500/20 text-pink-400 mt-0.5">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
                </div>
                <div>
                    <h2 class="text-sm font-bold text-white">Final Comprehensive Submission &bull; Dual-View Engine Active</h2>
                    <p class="text-xs text-slate-300 max-w-2xl mt-0.5">
                        <b>Round 1 Official Top 10:</b> Evaluated on absolute clutch performance (LI &ge; 1.50) without contract prejudice. <br>
                        <b>Auction Target View:</b> Real-time toggle filtering exclusively for available, unretained players for Rajasthan Royals' auction war room.
                    </p>
                </div>
            </div>
            
            <!-- Quick Metrics Badge -->
            <div class="flex items-center gap-2">
                <div class="bg-slate-900 border border-slate-800 px-3 py-1.5 rounded-lg text-center">
                    <p class="text-[10px] text-slate-400 uppercase">Deliveries Evaluated</p>
                    <p class="text-sm font-extrabold text-pink-400">200,999</p>
                </div>
                <div class="bg-slate-900 border border-slate-800 px-3 py-1.5 rounded-lg text-center">
                    <p class="text-[10px] text-slate-400 uppercase">Venues Calibrated</p>
                    <p class="text-sm font-extrabold text-indigo-400">17 Venues</p>
                </div>
                <div class="bg-slate-900 border border-slate-800 px-3 py-1.5 rounded-lg text-center">
                    <p class="text-[10px] text-slate-400 uppercase">Models Integrated</p>
                    <p class="text-sm font-extrabold text-emerald-400">v1 &bull; v2 &bull; v3 &bull; v4</p>
                </div>
            </div>
        </div>

        <!-- Navigation Tabs -->
        <div class="flex border-b border-slate-800 space-x-2">
            <button onclick="switchTab('evolution')" id="tab-evolution" class="tab-btn px-4 py-2.5 rounded-t-xl font-bold text-xs uppercase tracking-wider transition text-slate-400 flex items-center gap-1.5">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 16V4m0 0L3 8m4-4l4 4m6 0v12m0 0l4-4m-4 4l-4-4"/></svg>
                Model Evolution (v1 vs v2 vs v3 vs v4)
            </button>
            <button onclick="switchTab('batters')" id="tab-batters" class="tab-btn active px-4 py-2.5 rounded-t-xl font-bold text-xs uppercase tracking-wider transition text-white flex items-center gap-1.5">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 8v8m-4-5v5m-4-2v2m-2 4h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z"/></svg>
                Final Batters (CBPS)
            </button>
            <button onclick="switchTab('bowlers')" id="tab-bowlers" class="tab-btn px-4 py-2.5 rounded-t-xl font-bold text-xs uppercase tracking-wider transition text-slate-400 flex items-center gap-1.5">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 10V3L4 14h7v7l9-11h-7z"/></svg>
                Final Bowlers (CBPS)
            </button>
            <button onclick="switchTab('quadrant')" id="tab-quadrant" class="tab-btn px-4 py-2.5 rounded-t-xl font-bold text-xs uppercase tracking-wider transition text-slate-400 flex items-center gap-1.5">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z"/></svg>
                Quadrant Analysis
            </button>
            <button onclick="switchTab('methodology')" id="tab-methodology" class="tab-btn px-4 py-2.5 rounded-t-xl font-bold text-xs uppercase tracking-wider transition text-slate-400 flex items-center gap-1.5">
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                Methodology & Deliverables
            </button>
        </div>

        <!-- ========================================== -->
        <!-- TAB: MODEL EVOLUTION (v1 vs v2 vs v3 vs v4) -->
        <!-- ========================================== -->
        <section id="sec-evolution" class="space-y-6 hidden">
            <!-- Evolution Header -->
            <div class="glass-card p-5 rounded-2xl border border-indigo-500/30 bg-indigo-950/20">
                <h3 class="text-base font-extrabold text-white flex items-center gap-2">
                    <span class="w-2.5 h-2.5 rounded-full bg-indigo-400"></span>
                    The 4-Stage Modeling Journey: Scientific Progression from Baseline to Unified Architecture
                </h3>
                <p class="text-xs text-slate-300 mt-1.5 max-w-4xl leading-relaxed">
                    Rather than presenting a static ranking, this study progressed through four rigorously engineered iterations. Each iteration introduced vital domain corrections &mdash; from venue baseline adjustments to opposition quality weighting and contract availability &mdash; ensuring Rajasthan Royals receives unassailable analytical rigor.
                </p>
            </div>

            <!-- Architectural Comparison Matrix -->
            <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-3">
                <h4 class="text-sm font-bold text-white flex items-center gap-2">
                    <span class="w-2 h-2 rounded-full bg-pink-500"></span>
                    Architecture & Modeling Feature Evolution Matrix
                </h4>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs text-slate-300 border-collapse">
                        <thead>
                            <tr class="border-b border-slate-700 bg-slate-900/80 text-[11px] font-bold text-slate-400 uppercase">
                                <th class="p-3">Modeling Dimension</th>
                                <th class="p-3">Model v1 (Baseline)</th>
                                <th class="p-3">Model v2 (Venue Pars)</th>
                                <th class="p-3">Model v3 (Active Roster)</th>
                                <th class="p-3 bg-pink-950/30 text-pink-400 border-l border-pink-500/30">Model v4 (Unified Contextual)</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800">
                            <tr class="hover:bg-slate-900/50">
                                <td class="p-3 font-semibold text-white">Ball-by-Ball Data Scope</td>
                                <td class="p-3">200,999 balls (867 matches)</td>
                                <td class="p-3">200,999 + 87,074 pure IPL</td>
                                <td class="p-3">200,999 + 87,074 pure IPL</td>
                                <td class="p-3 font-bold text-pink-400 bg-pink-950/20 border-l border-pink-500/30">200,999 + 87,074 pure IPL</td>
                            </tr>
                            <tr class="hover:bg-slate-900/50">
                                <td class="p-3 font-semibold text-white">Pressure Deliveries Filtered</td>
                                <td class="p-3">58,125 balls (28.92%)</td>
                                <td class="p-3">58,125 balls (28.92%)</td>
                                <td class="p-3">58,125 balls (28.92%)</td>
                                <td class="p-3 font-bold text-pink-400 bg-pink-950/20 border-l border-pink-500/30">60,375 balls (30.04% HP gate)</td>
                            </tr>
                            <tr class="hover:bg-slate-900/50">
                                <td class="p-3 font-semibold text-white">Venue Pitch Pars</td>
                                <td class="p-3 text-slate-500">Static (9.00 RPO)</td>
                                <td class="p-3 text-emerald-400 font-semibold">17 Stadium Pars</td>
                                <td class="p-3 text-emerald-400 font-semibold">17 Stadium Pars</td>
                                <td class="p-3 font-bold text-pink-400 bg-pink-950/20 border-l border-pink-500/30">17 Stadium Pars + RR Home Calibration</td>
                            </tr>
                            <tr class="hover:bg-slate-900/50">
                                <td class="p-3 font-semibold text-white">Playoff Leverage Multipliers</td>
                                <td class="p-3 text-slate-500">Flat (1.15x)</td>
                                <td class="p-3 text-indigo-400">1.20x Qualifiers / 1.30x Final</td>
                                <td class="p-3 text-indigo-400">1.20x Qualifiers / 1.30x Final</td>
                                <td class="p-3 font-bold text-pink-400 bg-pink-950/20 border-l border-pink-500/30">1.20x Qualifiers / 1.30x Final</td>
                            </tr>
                            <tr class="hover:bg-slate-900/50">
                                <td class="p-3 font-semibold text-white">Active Roster & Retentions</td>
                                <td class="p-3 text-slate-500">Raw Historical Pool</td>
                                <td class="p-3 text-slate-500">Raw Historical Pool</td>
                                <td class="p-3 text-emerald-400 font-semibold">Option 3 + 4 Verified</td>
                                <td class="p-3 font-bold text-pink-400 bg-pink-950/20 border-l border-pink-500/30">Dual-Toggle (Official + Auction Filter)</td>
                            </tr>
                            <tr class="hover:bg-slate-900/50">
                                <td class="p-3 font-semibold text-white">Opposition Bowler Quality Tiering</td>
                                <td class="p-3 text-slate-500">None</td>
                                <td class="p-3 text-slate-500">None</td>
                                <td class="p-3 text-slate-500">None</td>
                                <td class="p-3 font-bold text-emerald-400 bg-pink-950/20 border-l border-pink-500/30">53 Elite Bowlers Tagged (1.15x Multiplier)</td>
                            </tr>
                            <tr class="hover:bg-slate-900/50">
                                <td class="p-3 font-semibold text-white">Wicket Quality Discounting</td>
                                <td class="p-3 text-slate-500">None</td>
                                <td class="p-3 text-slate-500">None</td>
                                <td class="p-3 text-slate-500">None</td>
                                <td class="p-3 font-bold text-emerald-400 bg-pink-950/20 border-l border-pink-500/30">0.70x Discount on Tailenders (#7&ndash;#11)</td>
                            </tr>
                            <tr class="hover:bg-slate-900/50">
                                <td class="p-3 font-semibold text-white">Chase Asymmetry & Urgency</td>
                                <td class="p-3 text-slate-500">None</td>
                                <td class="p-3 text-slate-500">None</td>
                                <td class="p-3 text-slate-500">None</td>
                                <td class="p-3 font-bold text-emerald-400 bg-pink-950/20 border-l border-pink-500/30">Non-linear 2nd Innings Target Escalation</td>
                            </tr>
                            <tr class="hover:bg-slate-900/50">
                                <td class="p-3 font-semibold text-white">Tactical Role Cohorts</td>
                                <td class="p-3 text-slate-500">None</td>
                                <td class="p-3 text-slate-500">None</td>
                                <td class="p-3 text-slate-500">None</td>
                                <td class="p-3 font-bold text-emerald-400 bg-pink-950/20 border-l border-pink-500/30">Anchor vs Finisher Role Stratification</td>
                            </tr>
                            <tr class="hover:bg-slate-900/50">
                                <td class="p-3 font-semibold text-white">Split-Half Reliability</td>
                                <td class="p-3 text-slate-400">r = 0.89</td>
                                <td class="p-3 text-indigo-400">r = 0.91</td>
                                <td class="p-3 text-indigo-400">r = 0.92</td>
                                <td class="p-3 font-bold text-pink-400 bg-pink-950/20 border-l border-pink-500/30">r = 0.94 (Peak Statistical Power)</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Batters Evolution Comparison Table -->
            <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-3">
                <div class="flex justify-between items-center">
                    <h4 class="text-sm font-bold text-white flex items-center gap-2">
                        <span class="w-2 h-2 rounded-full bg-pink-500"></span>
                        Batting Leaderboard Evolution Across Versions (v1 &rarr; v2 &rarr; v3 &rarr; v4)
                    </h4>
                    <span class="text-xs text-slate-400">Showing Official Round 1 Rankings Across All 4 Models</span>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs text-slate-300 border-collapse">
                        <thead>
                            <tr class="border-b border-slate-700 bg-slate-900/80 text-[11px] font-bold text-slate-400 uppercase">
                                <th class="p-3 text-center">Rank</th>
                                <th class="p-3">Model v1 (Score)</th>
                                <th class="p-3">Model v2 (Score)</th>
                                <th class="p-3">Model v3 (Score)</th>
                                <th class="p-3 bg-pink-950/30 text-pink-400 border-l border-pink-500/30">Model v4 Final (Score)</th>
                                <th class="p-3">Key Analytical Shift in v4</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800" id="evolution-batters-tbody">
                            <!-- Populated by JS -->
                        </tbody>
                    </table>
                </div>
            </div>

            <!-- Bowlers Evolution Comparison Table -->
            <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-3">
                <div class="flex justify-between items-center">
                    <h4 class="text-sm font-bold text-white flex items-center gap-2">
                        <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                        Bowling Leaderboard Evolution Across Versions (v1 &rarr; v2 &rarr; v3 &rarr; v4)
                    </h4>
                    <span class="text-xs text-slate-400">Showing Official Round 1 Rankings Across All 4 Models</span>
                </div>
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs text-slate-300 border-collapse">
                        <thead>
                            <tr class="border-b border-slate-700 bg-slate-900/80 text-[11px] font-bold text-slate-400 uppercase">
                                <th class="p-3 text-center">Rank</th>
                                <th class="p-3">Model v1 (Score)</th>
                                <th class="p-3">Model v2 (Score)</th>
                                <th class="p-3">Model v3 (Score)</th>
                                <th class="p-3 bg-emerald-950/30 text-emerald-400 border-l border-emerald-500/30">Model v4 Final (Score)</th>
                                <th class="p-3">Key Analytical Shift in v4</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800" id="evolution-bowlers-tbody">
                            <!-- Populated by JS -->
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- ========================================== -->
        <!-- TAB: FINAL BATTERS (CBPS) -->
        <!-- ========================================== -->
        <section id="sec-batters" class="space-y-6">
            <!-- Controls & Table Top -->
            <div class="glass-card rounded-2xl p-4 border border-slate-800 flex flex-wrap items-center justify-between gap-4">
                <div>
                    <h3 class="text-base font-extrabold text-white flex items-center gap-2">
                        <span class="w-2 h-2 rounded-full bg-pink-500"></span>
                        Top 10 High-Pressure Batters (Contextual Clutch Score)
                    </h3>
                    <p class="text-xs text-slate-400">Pressure Gate: $LI \\ge 1.50$ &bull; Empirical Bayes Shrinkage ($K=50$) &bull; Opposition Quality Scaled</p>
                </div>
                
                <!-- Dual Interactive Toggles -->
                <div class="flex flex-wrap items-center gap-3">
                    <!-- Toggle 1: Free / Unretained Players -->
                    <div class="flex items-center gap-2 bg-slate-900 border border-slate-700 px-3 py-1.5 rounded-xl">
                        <span class="text-xs font-semibold text-slate-300">Free / Unretained Only:</span>
                        <button id="toggle-free-btn" onclick="toggleFreeOnly()" class="px-3 py-1 rounded-lg text-xs font-bold transition flex items-center gap-1.5 bg-slate-800 text-slate-400 border border-slate-700">
                            <span id="toggle-free-indicator" class="w-2 h-2 rounded-full bg-slate-500"></span>
                            <span id="toggle-free-text">OFF (All Contenders)</span>
                        </button>
                    </div>

                    <!-- Toggle 2: Home Ground Calibration -->
                    <div class="flex items-center gap-2 bg-slate-900 border border-slate-700 px-3 py-1.5 rounded-xl">
                        <span class="text-xs font-semibold text-slate-300">Venue Calibration:</span>
                        <button id="toggle-venue-btn" onclick="toggleVenueMode()" class="px-3 py-1 rounded-lg text-xs font-bold transition flex items-center gap-1.5 bg-slate-800 text-slate-400 border border-slate-700">
                            <span id="toggle-venue-indicator" class="w-2 h-2 rounded-full bg-slate-500"></span>
                            <span id="toggle-venue-text">All 17 Venues</span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Summary Highlight Cards -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4" id="batters-cards">
                <!-- Dynamically populated -->
            </div>

            <!-- Table -->
            <div class="glass-card rounded-2xl border border-slate-800 overflow-hidden">
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs text-slate-300 border-collapse">
                        <thead>
                            <tr class="border-b border-slate-800 bg-slate-900/60 text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                                <th class="p-3">Rank</th>
                                <th class="p-3">Player</th>
                                <th class="p-3">Status / IPL 2027 Team</th>
                                <th class="p-3">HP Balls</th>
                                <th class="p-3">HP Strike Rate</th>
                                <th class="p-3 text-pink-400">Opp-Adjusted SR</th>
                                <th class="p-3 text-pink-400">&Delta; Venue Par</th>
                                <th class="p-3 text-indigo-400">&Delta; Baseline</th>
                                <th class="p-3 text-emerald-400">Reliability</th>
                                <th class="p-3 text-right">CBPS (Final)</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800/60" id="batters-tbody">
                            <!-- Dynamically populated -->
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- ========================================== -->
        <!-- TAB: FINAL BOWLERS (CBPS) -->
        <!-- ========================================== -->
        <section id="sec-bowlers" class="space-y-6 hidden">
            <!-- Controls & Table Top -->
            <div class="glass-card rounded-2xl p-4 border border-slate-800 flex flex-wrap items-center justify-between gap-4">
                <div>
                    <h3 class="text-base font-extrabold text-white flex items-center gap-2">
                        <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                        Top 10 High-Pressure Bowlers (Contextual Clutch Score)
                    </h3>
                    <p class="text-xs text-slate-400">Tailender Discounting &bull; Quality Wicket Multipliers &bull; Venue Par Economy Suppression</p>
                </div>
                
                <!-- Dual Interactive Toggles (Synchronized) -->
                <div class="flex flex-wrap items-center gap-3">
                    <div class="flex items-center gap-2 bg-slate-900 border border-slate-700 px-3 py-1.5 rounded-xl">
                        <span class="text-xs font-semibold text-slate-300">Free / Unretained Only:</span>
                        <button id="toggle-free-btn-bowl" onclick="toggleFreeOnly()" class="px-3 py-1 rounded-lg text-xs font-bold transition flex items-center gap-1.5 bg-slate-800 text-slate-400 border border-slate-700">
                            <span id="toggle-free-indicator-bowl" class="w-2 h-2 rounded-full bg-slate-500"></span>
                            <span id="toggle-free-text-bowl">OFF (All Contenders)</span>
                        </button>
                    </div>

                    <div class="flex items-center gap-2 bg-slate-900 border border-slate-700 px-3 py-1.5 rounded-xl">
                        <span class="text-xs font-semibold text-slate-300">Venue Calibration:</span>
                        <button id="toggle-venue-btn-bowl" onclick="toggleVenueMode()" class="px-3 py-1 rounded-lg text-xs font-bold transition flex items-center gap-1.5 bg-slate-800 text-slate-400 border border-slate-700">
                            <span id="toggle-venue-indicator-bowl" class="w-2 h-2 rounded-full bg-slate-500"></span>
                            <span id="toggle-venue-text-bowl">All 17 Venues</span>
                        </button>
                    </div>
                </div>
            </div>

            <!-- Summary Highlight Cards -->
            <div class="grid grid-cols-1 md:grid-cols-3 gap-4" id="bowlers-cards">
                <!-- Dynamically populated -->
            </div>

            <!-- Table -->
            <div class="glass-card rounded-2xl border border-slate-800 overflow-hidden">
                <div class="overflow-x-auto">
                    <table class="w-full text-left text-xs text-slate-300 border-collapse">
                        <thead>
                            <tr class="border-b border-slate-800 bg-slate-900/60 text-[11px] font-bold text-slate-400 uppercase tracking-wider">
                                <th class="p-3">Rank</th>
                                <th class="p-3">Player</th>
                                <th class="p-3">Status / IPL 2027 Team</th>
                                <th class="p-3">HP Balls</th>
                                <th class="p-3">HP Economy</th>
                                <th class="p-3 text-emerald-400">Econ vs Venue Par</th>
                                <th class="p-3 text-indigo-400">&Delta; Baseline Econ</th>
                                <th class="p-3">Quality Wkt Rate</th>
                                <th class="p-3 text-emerald-400">Reliability</th>
                                <th class="p-3 text-right">CBPS (Final)</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y divide-slate-800/60" id="bowlers-tbody">
                            <!-- Dynamically populated -->
                        </tbody>
                    </table>
                </div>
            </div>
        </section>

        <!-- ========================================== -->
        <!-- TAB: QUADRANT ANALYSIS -->
        <!-- ========================================== -->
        <section id="sec-quadrant" class="space-y-6 hidden">
            <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                <!-- Batters Plot -->
                <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-3">
                    <div class="flex justify-between items-center">
                        <h4 class="text-sm font-bold text-white flex items-center gap-2">
                            <span class="w-2 h-2 rounded-full bg-pink-500"></span>
                            Batting Clutch Matrix (Venue Par Delta vs Baseline Elevation)
                        </h4>
                    </div>
                    <div id="plot-batters-matrix" class="w-full h-80"></div>
                </div>

                <!-- Bowlers Plot -->
                <div class="glass-card rounded-2xl p-5 border border-slate-800 space-y-3">
                    <div class="flex justify-between items-center">
                        <h4 class="text-sm font-bold text-white flex items-center gap-2">
                            <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                            Bowling Clutch Matrix (Venue Econ Suppression vs Quality Wkt Rate)
                        </h4>
                    </div>
                    <div id="plot-bowlers-matrix" class="w-full h-80"></div>
                </div>
            </div>
        </section>

        <!-- ========================================== -->
        <!-- TAB: METHODOLOGY & SCIENTIFIC VALIDATION -->
        <!-- ========================================== -->
        <section id="sec-methodology" class="space-y-6 hidden">
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div class="glass-card rounded-2xl p-6 border border-slate-800 space-y-4">
                    <h3 class="text-base font-bold text-pink-400 flex items-center gap-2">
                        <span>1. Leverage Index Formulation</span>
                    </h3>
                    <p class="text-xs text-slate-300 leading-relaxed">
                        Every delivery is assigned a dynamic Leverage Index ($LI$) defined by:
                    </p>
                    <div class="bg-slate-900/80 p-3 rounded-lg text-xs font-mono text-pink-300 border border-slate-800">
                        LI = Phase_Weight &times; Margin_Weight &times; Stage_Multiplier
                    </div>
                    <ul class="text-xs text-slate-400 space-y-1.5 list-disc list-inside">
                        <li><b>Death Phase (Overs 16-20):</b> Baseline $1.50\times$, scaling up to $2.20\times$ in 1-wicket situations.</li>
                        <li><b>Playoff Weighting:</b> $1.20\times$ for Qualifiers/Eliminators, $1.30\times$ for IPL Finals.</li>
                        <li><b>HP Threshold:</b> $LI \ge 1.50$ captures the top 30% most pressurized deliveries.</li>
                    </ul>
                </div>

                <div class="glass-card rounded-2xl p-6 border border-slate-800 space-y-4">
                    <h3 class="text-base font-bold text-emerald-400 flex items-center gap-2">
                        <span>2. Empirical Bayes Shrinkage & Contextual Multipliers</span>
                    </h3>
                    <p class="text-xs text-slate-300 leading-relaxed">
                        To neutralize small-sample skew, all metrics are shrunken toward prior means:
                    </p>
                    <div class="bg-slate-900/80 p-3 rounded-lg text-xs font-mono text-emerald-300 border border-slate-800">
                        Metric_shrunken = (N_balls / (N_balls + K)) &times; Metric_raw + (K / (N_balls + K)) &times; Prior_mean
                    </div>
                    <ul class="text-xs text-slate-400 space-y-1.5 list-disc list-inside">
                        <li><b>Sample Penalty ($K=50$ balls):</b> Eliminates one-innings wonders.</li>
                        <li><b>Opposition Tiering:</b> $1.15\times$ run scaling against 53 elite tagged bowlers.</li>
                        <li><b>Tailender Discount:</b> $0.70\times$ weight on wickets taken against batters #7&ndash;#11.</li>
                    </ul>
                </div>
            </div>

            <!-- Deliverables Download Box -->
            <div class="glass-card rounded-2xl p-6 border border-slate-800 flex flex-wrap justify-between items-center gap-4">
                <div>
                    <h4 class="text-sm font-bold text-white">Full Research Dossier & Raw Deliverables</h4>
                    <p class="text-xs text-slate-400">Access official competition reports, CSV models, and full code reproduction suite.</p>
                </div>
                <div class="flex flex-wrap gap-2 text-xs">
                    <a href="rr-submission/v4/Mohammed_Aleem_Bukkapatnam_RR_SupeRR_Selector_Report_v4.pdf" target="_blank" class="px-3.5 py-2 rounded-xl bg-pink-600 hover:bg-pink-700 text-white font-bold transition flex items-center gap-1.5">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/></svg>
                        Download PDF Report (v4)
                    </a>
                    <a href="rr-submission/COMPARATIVE_ANALYSIS_V1_VS_V2_VS_V3_VS_V4.md" target="_blank" class="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold border border-slate-700 transition">
                        Comparative Analysis Markdown
                    </a>
                    <a href="https://github.com/Aleem1404/superr-selector-s2" target="_blank" class="px-3.5 py-2 rounded-xl bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold border border-slate-700 transition flex items-center gap-1.5">
                        GitHub Source Code
                    </a>
                </div>
            </div>
        </section>

    </main>

    <!-- Footer -->
    <footer class="border-t border-slate-800 bg-slate-950/80 py-4 mt-auto">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex flex-wrap justify-between items-center text-xs text-slate-400 gap-4">
            <p>&copy; 2026 Rajasthan Royals SupeRR Selector Season 2 &bull; Analytical Case Study Submission</p>
            <p>Designed & Engineered by <b class="text-white">Mohammed Aleem Bukkapatnam</b> (M.S. in Artificial Intelligence)</p>
        </div>
    </footer>

    <!-- Interactive Logic Script -->
    <script>
        const allBatters = {json.dumps(all_bat_list)};
        const allBowlers = {json.dumps(all_bowl_list)};
        const evolutionBatters = {json.dumps(v_batters)};
        const evolutionBowlers = {json.dumps(v_bowlers)};

        let isFreeOnly = false;
        let isHomeGround = false;

        function getFilteredBatters() {{
            let pool = allBatters.slice();
            if (isFreeOnly) {{
                pool = pool.filter(b => b.is_auction_target === true);
            }}
            const scoreKey = isHomeGround ? 'cbps_home' : 'cbps_final';
            pool.sort((a, b) => b[scoreKey] - a[scoreKey]);
            return pool.slice(0, 10);
        }}

        function getFilteredBowlers() {{
            let pool = allBowlers.slice();
            if (isFreeOnly) {{
                pool = pool.filter(b => b.is_auction_target === true);
            }}
            const scoreKey = isHomeGround ? 'cbps_home' : 'cbps_final';
            pool.sort((a, b) => b[scoreKey] - a[scoreKey]);
            return pool.slice(0, 10);
        }}

        function toggleFreeOnly() {{
            isFreeOnly = !isFreeOnly;
            updateToggleButtons();
            refreshTables();
        }}

        function toggleVenueMode() {{
            isHomeGround = !isHomeGround;
            updateToggleButtons();
            refreshTables();
        }}

        function updateToggleButtons() {{
            const btnFree = document.getElementById('toggle-free-btn');
            const indFree = document.getElementById('toggle-free-indicator');
            const txtFree = document.getElementById('toggle-free-text');
            const btnFreeBowl = document.getElementById('toggle-free-btn-bowl');
            const indFreeBowl = document.getElementById('toggle-free-indicator-bowl');
            const txtFreeBowl = document.getElementById('toggle-free-text-bowl');

            if (isFreeOnly) {{
                const activeClasses = ['bg-emerald-600', 'text-white', 'border-emerald-500'];
                btnFree.classList.add(...activeClasses);
                btnFreeBowl.classList.add(...activeClasses);
                indFree.className = 'w-2 h-2 rounded-full bg-white animate-pulse';
                indFreeBowl.className = 'w-2 h-2 rounded-full bg-white animate-pulse';
                txtFree.innerText = 'ON (Auction Targets Only)';
                txtFreeBowl.innerText = 'ON (Auction Targets Only)';
            }} else {{
                btnFree.className = 'px-3 py-1 rounded-lg text-xs font-bold transition flex items-center gap-1.5 bg-slate-800 text-slate-400 border border-slate-700';
                btnFreeBowl.className = 'px-3 py-1 rounded-lg text-xs font-bold transition flex items-center gap-1.5 bg-slate-800 text-slate-400 border border-slate-700';
                indFree.className = 'w-2 h-2 rounded-full bg-slate-500';
                indFreeBowl.className = 'w-2 h-2 rounded-full bg-slate-500';
                txtFree.innerText = 'OFF (All Contenders)';
                txtFreeBowl.innerText = 'OFF (All Contenders)';
            }}

            const btnVenue = document.getElementById('toggle-venue-btn');
            const indVenue = document.getElementById('toggle-venue-indicator');
            const txtVenue = document.getElementById('toggle-venue-text');
            const btnVenueBowl = document.getElementById('toggle-venue-btn-bowl');
            const indVenueBowl = document.getElementById('toggle-venue-indicator-bowl');
            const txtVenueBowl = document.getElementById('toggle-venue-text-bowl');

            if (isHomeGround) {{
                const activeVenueClasses = ['bg-pink-600', 'text-white', 'border-pink-500'];
                btnVenue.classList.add(...activeVenueClasses);
                btnVenueBowl.classList.add(...activeVenueClasses);
                indVenue.className = 'w-2 h-2 rounded-full bg-white animate-pulse';
                indVenueBowl.className = 'w-2 h-2 rounded-full bg-white animate-pulse';
                txtVenue.innerText = 'RR Home (Jaipur & Guwahati)';
                txtVenueBowl.innerText = 'RR Home (Jaipur & Guwahati)';
            }} else {{
                btnVenue.className = 'px-3 py-1 rounded-lg text-xs font-bold transition flex items-center gap-1.5 bg-slate-800 text-slate-400 border border-slate-700';
                btnVenueBowl.className = 'px-3 py-1 rounded-lg text-xs font-bold transition flex items-center gap-1.5 bg-slate-800 text-slate-400 border border-slate-700';
                indVenue.className = 'w-2 h-2 rounded-full bg-slate-500';
                indVenueBowl.className = 'w-2 h-2 rounded-full bg-slate-500';
                txtVenue.innerText = 'All 17 Venues';
                txtVenueBowl.innerText = 'All 17 Venues';
            }}
        }}

        function refreshTables() {{
            const scoreKey = isHomeGround ? 'cbps_home' : 'cbps_final';
            renderBatters(getFilteredBatters(), scoreKey);
            renderBowlers(getFilteredBowlers(), scoreKey);
            if (!document.getElementById('sec-quadrant').classList.contains('hidden')) {{
                renderQuadrantCharts();
            }}
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

                if (rank <= 3) {{
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

                if (rank <= 3) {{
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

        function renderEvolutionTables() {{
            const batTbody = document.getElementById('evolution-batters-tbody');
            batTbody.innerHTML = '';
            evolutionBatters.forEach(row => {{
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-900/50';
                tr.innerHTML = `
                    <td class="p-3 text-center font-bold text-slate-400">#${{row.rank}}</td>
                    <td class="p-3"><span class="font-medium text-slate-300">${{row.v1}}</span> <span class="text-[11px] text-slate-500">(+${{row.v1_s.toFixed(2)}})</span></td>
                    <td class="p-3"><span class="font-medium text-slate-300">${{row.v2}}</span> <span class="text-[11px] text-slate-500">(+${{row.v2_s.toFixed(2)}})</span></td>
                    <td class="p-3"><span class="font-medium text-slate-300">${{row.v3}}</span> <span class="text-[11px] text-slate-500">(+${{row.v3_s.toFixed(2)}})</span></td>
                    <td class="p-3 bg-pink-950/20 border-l border-pink-500/30"><b class="text-pink-400">${{row.v4}}</b> <span class="text-[11px] font-bold text-pink-300">(+${{row.v4_s.toFixed(2)}})</span></td>
                    <td class="p-3 text-[11px] text-slate-300">${{row.note}}</td>
                `;
                batTbody.appendChild(tr);
            }});

            const bowlTbody = document.getElementById('evolution-bowlers-tbody');
            bowlTbody.innerHTML = '';
            evolutionBowlers.forEach(row => {{
                const tr = document.createElement('tr');
                tr.className = 'hover:bg-slate-900/50';
                tr.innerHTML = `
                    <td class="p-3 text-center font-bold text-slate-400">#${{row.rank}}</td>
                    <td class="p-3"><span class="font-medium text-slate-300">${{row.v1}}</span> <span class="text-[11px] text-slate-500">(+${{row.v1_s.toFixed(2)}})</span></td>
                    <td class="p-3"><span class="font-medium text-slate-300">${{row.v2}}</span> <span class="text-[11px] text-slate-500">(+${{row.v2_s.toFixed(2)}})</span></td>
                    <td class="p-3"><span class="font-medium text-slate-300">${{row.v3}}</span> <span class="text-[11px] text-slate-500">(+${{row.v3_s.toFixed(2)}})</span></td>
                    <td class="p-3 bg-emerald-950/20 border-l border-emerald-500/30"><b class="text-emerald-400">${{row.v4}}</b> <span class="text-[11px] font-bold text-emerald-300">(+${{row.v4_s.toFixed(2)}})</span></td>
                    <td class="p-3 text-[11px] text-slate-300">${{row.note}}</td>
                `;
                bowlTbody.appendChild(tr);
            }});
        }}

        function switchTab(tabId) {{
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active', 'text-white'));
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.add('text-slate-400'));
            
            const activeBtn = document.getElementById('tab-' + tabId);
            activeBtn.classList.add('active', 'text-white');
            activeBtn.classList.remove('text-slate-400');

            ['evolution', 'batters', 'bowlers', 'quadrant', 'methodology'].forEach(id => {{
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

        // Initial setup
        document.addEventListener('DOMContentLoaded', () => {{
            renderEvolutionTables();
            refreshTables();
        }});
    </script>
</body>
</html>
"""

    # Write to root index.html, docs/index.html, and rr-submission/v4/dashboard/index.html
    paths = [
        'index.html',
        'docs/index.html',
        'rr-submission/v4/dashboard/index.html'
    ]
    for p in paths:
        os.makedirs(os.path.dirname(p) if os.path.dirname(p) else '.', exist_ok=True)
        with open(p, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"Generated master dashboard at: {p} ({len(html_content)} bytes)")

if __name__ == '__main__':
    build_final_master_dashboard()

