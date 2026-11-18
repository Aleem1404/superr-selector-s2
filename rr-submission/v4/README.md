# Rajasthan Royals | SupeRR Selector Season 2: Round 1 Submission (Model v4)

**Candidate:** Mohammed Aleem Bukkapatnam (M.S. in Artificial Intelligence)  
**Evaluation Panel:** Rajasthan Royals Analytics Team  
**Deliverable Version:** **v4 (Unified Contextual Architecture: Opposition Tiering, Chase Asymmetry & Tactical Cohorts)**  
**Deliverable Files:**
- **Report PDF:** [`Mohammed_Aleem_Bukkapatnam_RR_SupeRR_Selector_Report_v4.pdf`](file:///f:/Challenges/Rajasthan%20Royals/rr-submission/v4/Mohammed_Aleem_Bukkapatnam_RR_SupeRR_Selector_Report_v4.pdf)
- **Interactive Web App Dashboard:** [`dashboard/index.html`](file:///f:/Challenges/Rajasthan%20Royals/rr-submission/v4/dashboard/index.html)

---

## 1. Executive Summary & Model v4 Unified Architecture

Model v4 represents our **pinnacle, production-grade formulation** designed to simulate an elite franchise scouting room. It unifies three complementary contextual pillars across 200,999 deliveries (60,375 high-pressure deliveries):

1. **Opposition Quality Tiering (Option A):**  
   - Batters receive a 1.15&times; quality multiplier when facing 53 pre-identified **Elite bowlers** (e.g. Jasprit Bumrah, Sunil Narine, Matheesha Pathirana, Rashid Khan).  
   - Bowlers' wickets are evaluated by tactical depth: dismissing top-to-middle order batters (#1–#6) receives full 1.00&times; weight, while tailender wickets (#7–#11) in the death overs are discounted to 0.70&times; to eliminate stat-padding.
2. **Chase Asymmetry & Innings Psychology (Option B):**  
   - Deliveries in 2nd innings run-chases where the Required Run Rate exceeds venue pitch par escalate non-linearly: $Mult_{chase} = 1.0 + 0.15 \times \min(1.0, \max(0.0, (RRR - Par_{venue})/Par_{venue}))$.
3. **Role & Entry Point Cohorts (Option C):**  
   - Classifies batters by match entry point: **Anchor / Top-Order Entry** (&le;14 overs) vs **Death Finisher Entry** (15–20 overs), guaranteeing sample equity across tactical roles.
4. **Interactive Dual Toggles (Dashboard & Scouting War-Room):**  
   - **Toggle 1: Roster Scope:** Switch dynamically between **All Active Contenders (Round 1 Official)** and **Available in Auction Only (RR Targets)**.  
   - **Toggle 2: Venue Scope:** Switch between **All 17 IPL Stadiums** and **Rajasthan Royals Home Fortress (Jaipur SMS & Guwahati)**.
5. **Active Roster Verification (Option 3 & Option 4):**  
   - Eliminates retired coaching personnel (**MS Dhoni**, CSK Mentor; **Dinesh Karthik**, RCB Mentor; **Matthew Wade**, Australia Coach) while strictly retaining 100% active contracted players.

---

## 2. Definitive Player Rankings (Model v4)

### Official Top 10 Active Batters Under Pressure (Dropdown Selections)
| Rank | Player Name | HP Balls | HP Strike Rate | Opp-Adjusted SR | $\Delta$SR Venue Par | $\Delta$SR Baseline | Consistency Rate | CBPS (v4) | Tactical Cohort & Archetype |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | **Naman Dhir** | 237 | 196.20 | **200.17** | +51.86 | +56.18 | 92.9% | **+1.60** | Finisher • Elite Boundary Striker (200.2 Opp-SR) |
| **2** | **Ashutosh Sharma** | 310 | 169.68 | **171.68** | +20.91 | +85.24 | 62.5% | **+1.27** | Finisher • Crisis Recovery Enforcer (+85.2 Delta) |
| **3** | **Suryakumar Yadav** | 669 | 186.70 | **190.31** | +44.32 | +36.89 | 78.8% | **+1.25** | Anchor • 360° Field Sculptor Across 669 Balls |
| **4** | **Jos Buttler** | 350 | 180.57 | **182.57** | +32.14 | +36.11 | 88.2% | **+1.11** | Anchor • Elite Chase Closer & Match Winner |
| **5** | **Glenn Phillips** | 289 | 179.93 | **184.71** | +36.44 | +51.90 | 78.6% | **+1.07** | Finisher • Dynamic Lower-Order Finisher |
| **6** | **Donovan Ferreira** | 205 | 181.46 | **186.34** | +33.32 | +58.82 | 72.7% | **+1.07** | Finisher • Heavy Pace & Spin Hitter |
| **7** | **Shreyas Iyer** | 459 | 174.73 | **177.30** | +29.37 | +38.14 | 80.0% | **+0.97** | Anchor • Championship Playoff Match Builder |
| **8** | **Sai Sudharsan** | 213 | 174.65 | **177.09** | +28.78 | +38.56 | 90.9% | **+0.84** | Anchor • Top-Order Reliability Anchor (90.9%) |
| **9** | **Shashank Singh** | 378 | 171.96 | **174.10** | +26.19 | +52.67 | 66.7% | **+0.84** | Finisher • Crisis Counter-Attacker (+52.7 Delta) |
| **10** | **Tim David** | 729 | 179.70 | **181.47** | +33.03 | +27.57 | 82.1% | **+0.81** | Finisher • Death-Overs Heavy Power Enforcer |

---

### Official Top 10 Active Bowlers Under Pressure (Dropdown Selections)
| Rank | Player Name | HP Balls | HP Economy | $\Delta$Econ Venue Par | $\Delta$Econ Baseline | Quality Wkt% | Consistency Rate | CBPS (v4) | Tactical Archetype |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | **Sunil Narine** | 470 | 6.63 | +2.45 | +0.32 | 6.40% | 90.5% | **+1.38** | Mystery Spin Constrictor (+2.45 Below Venue Par) |
| **2** | **Matheesha Pathirana** | 615 | 8.51 | +1.42 | +0.16 | 9.40% | 91.9% | **+1.13** | Slingshot Yorker Enforcer (9.4% Quality Wkts) |
| **3** | **Mitchell Santner** | 491 | 7.30 | +1.97 | +0.13 | 6.74% | 96.2% | **+1.12** | Defensive Match Controller (96.2% Consistency) |
| **4** | **Akeal Hosein** | 244 | 7.38 | +1.84 | +0.38 | 8.07% | 83.3% | **+0.99** | Powerplay & Death Precision Spinner |
| **5** | **Rashid Khan** | 910 | 7.96 | +1.04 | -0.83 | 8.35% | 90.9% | **+0.93** | High-Leverage Strike Spinner Across 910 Balls |
| **6** | **Jasprit Bumrah** | 691 | 7.42 | +1.68 | -0.42 | 7.24% | 77.8% | **+0.92** | Gold Standard Containment Pacer (7.42 HP Econ) |
| **7** | **Wanindu Hasaranga** | 523 | 8.43 | +0.41 | -0.68 | 9.52% | 89.7% | **+0.81** | Middle-Overs Breakthrough Wicket Striker |
| **8** | **Taskin Ahmed** | 329 | 8.61 | +0.72 | -1.02 | 8.91% | 87.5% | **+0.77** | High-Pace Hard-Length Enforcer |
| **9** | **Sikandar Raza** | 241 | 7.22 | +1.93 | -0.23 | 5.27% | 91.7% | **+0.77** | Finger Spin Run Squeeze (7.22 HP Econ) |
| **10** | **Varun Chakravarthy** | 706 | 8.35 | +0.86 | -0.57 | 7.18% | 93.9% | **+0.75** | Middle & Death Squeeze (93.9% Spell Reliability) |

---

## 3. Directory Architecture
```
rr-submission/v4/
├── dashboard/
│   └── index.html                                          # Interactive Plotly Web App
├── Mohammed_Aleem_Bukkapatnam_RR_SupeRR_Selector_Report_v4.pdf  # Final PDF Report
├── scripts/
│   ├── build_v4_dashboard.py
│   ├── compile_v4_pdf_report.py
│   ├── generate_v4_figures.py
│   ├── stage1_v4_unified_leverage.py
│   ├── stage2_v4_aggregate_players.py
│   ├── stage3_v4_bayesian_shrinkage.py
│   └── stage4_v4_rankings_active_roster.py
├── stage1_ball_leverage/
│   ├── ball_by_ball_pressure_v4.csv
│   └── stage1_summary_v4.json
├── stage2_player_aggregates/
│   ├── raw_batting_aggregates_v4.csv
│   └── raw_bowling_aggregates_v4.csv
├── stage3_bayesian_filtering/
│   ├── shrunken_batters_v4.csv
│   └── shrunken_bowlers_v4.csv
├── stage4_consistency_scoring/
│   ├── active_batters_v4_master.csv
│   ├── active_bowlers_v4_master.csv
│   ├── ranked_batters_v4_master.csv
│   ├── ranked_bowlers_v4_master.csv
│   ├── top10_batters_v4_final.csv
│   └── top10_bowlers_v4_final.csv
├── stage5_deliverables/
│   ├── figures/
│   │   ├── batter_clutch_matrix.png
│   │   ├── bowler_clutch_matrix.png
│   │   ├── top_10_batters_cbps.png
│   │   └── top_10_bowlers_cbps.png
│   ├── Mohammed_Aleem_Bukkapatnam_RR_SupeRR_Selector_Report_v4.pdf
│   ├── top10_batters_v4.csv
│   └── top10_bowlers_v4.csv
├── top10_batters_final.csv
├── top10_bowlers_final.csv
└── v4_pipeline_summary.json
```

