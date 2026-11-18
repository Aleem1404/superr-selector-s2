# Rajasthan Royals | SupeRR Selector Season 2: Round 1 Submission (Model v3)

**Candidate:** Mohammed Aleem Bukkapatnam (M.S. in Artificial Intelligence)  
**Evaluation Panel:** Rajasthan Royals Analytics Team  
**Deliverable Version:** v3 (Active Roster Verified, Venue Par Calibrated & Multi-Stage Leverage Framework)  
**Deliverable Files:**
- **Report PDF:** [`Mohammed_Aleem_Bukkapatnam_RR_SupeRR_Selector_Report_v3.pdf`](file:///f:/Challenges/Rajasthan%20Royals/rr-submission/v3/Mohammed_Aleem_Bukkapatnam_RR_SupeRR_Selector_Report_v3.pdf)
- **Interactive Web App Dashboard:** [`dashboard/index.html`](file:///f:/Challenges/Rajasthan%20Royals/rr-submission/v3/dashboard/index.html)

---

## 1. Executive Summary & Model v3 Evolution
Model v3 represents the definitive, competition-calibrated pressure evaluation framework for Round 1 of the SupeRR Selector contest.

While Model v1 established the Dynamic Leverage Index (LI $\ge 1.50$) across 200,999 balls, and Model v2 calibrated individual performances against 17 stadium-specific scoring par rates ($Par_{venue}$) from 87,074 balls across 5 IPL seasons, **Model v3 implements Criteria 1: Active Roster Verification**.

### Criteria 1: Active Roster Verification (Cricinfo Status + Public Announcements)
Per the prompt's evaluation guidelines, Round 1 measures pure pressure performance without artificial retention constraints. However, evaluating retired or coaching personnel provides no practical utility for team intelligence. 

Using **Option 3 (ESPNcricinfo official profile status)** and **Option 4 (Official public retirement announcements)**:
- **Excluded Inactive/Coaching Personnel:**
  - **MS Dhoni:** Officially retired from representative play and transitioned to CSK Team Mentor.
  - **Dinesh Karthik:** Officially retired from representative cricket on 1 June 2024; appointed RCB Batting Coach & Mentor.
  - **Matthew Wade:** Officially retired from international and elite professional cricket in October 2024; joined the Australian coaching staff.
- **Verified Active Personnel (Strictly Retained):**
  - **Jos Buttler, Suryakumar Yadav, Jasprit Bumrah, Sunil Narine, Rashid Khan, Shreyas Iyer:** All verified active, contracted tournament superstars.
  - **Dhruv Jurel:** Retained by Rajasthan Royals (RR) for ₹14 Crore; mathematically emerges as India's premier young clutch batter (#7).
  - **Tristan Stubbs:** Retained by Delhi Capitals (DC) for ₹10 Crore; ranks at #9.
  - **Tim David:** Australia and IPL power finisher; enters the Top 10 Batters at #10.

---

## 2. Definitive Player Rankings (Model v3)

### Official Top 10 Batters Under Pressure (Dropdown Selections)
| Rank | Player Name | HP Balls | HP Strike Rate | $\Delta$SR Venue Par | $\Delta$SR Baseline | HP Dot% | Consistency Rate | CBPS (v3) | Tactical Archetype |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | **Naman Dhir** | 235 | 194.89 | +46.63 | +49.78 | 27.2% | 92.9% | **+1.48** | Active (MI) • Boundary Striker / High-Impact Finisher |
| **2** | **Ashutosh Sharma** | 307 | 171.01 | +20.26 | +87.14 | 34.9% | 62.5% | **+1.38** | Active (DC) • Crisis Recovery Enforcer |
| **3** | **Jos Buttler** | 319 | 184.95 | +34.51 | +38.62 | 27.0% | 100.0% | **+1.36** | Active • 100% Chase Closer & Match Winner |
| **4** | **Suryakumar Yadav** | 609 | 188.83 | +43.12 | +35.10 | 30.2% | 77.4% | **+1.26** | Active (MI Retained) • 360-Degree Field Manipulator |
| **5** | **Shreyas Iyer** | 420 | 177.62 | +29.57 | +38.35 | 26.2% | 80.0% | **+1.00** | Active • Championship Playoff Match Winner |
| **6** | **Glenn Phillips** | 255 | 179.22 | +30.87 | +44.35 | 29.0% | 78.6% | **+0.90** | Active • Versatile Lower-Order Finisher |
| **7** | **Dhruv Jurel** | 325 | 171.08 | +21.05 | +40.62 | 28.3% | 83.3% | **+0.89** | **Active (RR Retained)** • Elite Clutch Keeper-Batter |
| **8** | **Marcus Stoinis** | 536 | 170.71 | +21.31 | +39.82 | 31.5% | 64.3% | **+0.82** | Active • Heavy Power-Hitter & Counter-Attacker |
| **9** | **Tristan Stubbs** | 580 | 170.52 | +20.24 | +52.00 | 27.6% | 66.7% | **+0.81** | Active (DC Retained) • All-Ground Spin & Pace Destroyer |
| **10** | **Tim David** | 716 | 178.49 | +30.01 | +22.51 | 34.9% | 81.6% | **+0.76** | Active • Death-Overs Heavy Power Finisher |

---

### Official Top 10 Bowlers Under Pressure (Dropdown Selections)
| Rank | Player Name | HP Balls | HP Economy | $\Delta$Econ Venue Par | $\Delta$Econ Baseline | HP Wkt Rate | Consistency Rate | CBPS (v3) | Tactical Archetype |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | **Sunil Narine** | 393 | 6.20 | +2.90 | +0.88 | 6.87% | 95.2% | **+1.61** | Active (KKR Retained) • Suffocating Mystery Spin Constrictor |
| **2** | **Matheesha Pathirana** | 611 | 8.53 | +1.40 | +0.10 | 10.15% | 91.9% | **+1.08** | Active (CSK Retained) • Slingshot Yorker Enforcer |
| **3** | **Jasprit Bumrah** | 646 | 7.41 | +1.66 | -0.39 | 8.51% | 78.0% | **+0.97** | Active (MI Retained) • Gold Standard Death Pacer |
| **4** | **Mitchell Santner** | 418 | 7.46 | +1.86 | -0.09 | 6.46% | 95.7% | **+0.89** | Active • Defensive Middle-Overs Controller |
| **5** | **Rashid Khan** | 800 | 8.13 | +0.89 | -1.02 | 8.62% | 92.9% | **+0.81** | Active (GT Retained) • High-Leverage Strike Spinner |
| **6** | **Varun Chakravarthy** | 674 | 8.26 | +0.95 | -0.42 | 7.72% | 93.9% | **+0.79** | Active (KKR Retained) • Middle & Death Spin Squeeze |
| **7** | **Taskin Ahmed** | 328 | 8.62 | +0.71 | -1.03 | 9.76% | 87.5% | **+0.75** | Active • High-Pace Hard-Length Enforcer |
| **8** | **Jamie Overton** | 202 | 8.61 | +0.59 | -0.06 | 12.38% | 70.0% | **+0.69** | Active • Heavy-Ball Hit-the-Deck Pacer |
| **9** | **Mitchell Starc** | 224 | 10.15 | -0.49 | -0.78 | 16.07% | 87.5% | **+0.68** | Active • Ultimate Wicket Weapon (Wkt / 6.2 balls) |
| **10** | **Rasikh Salam** | 250 | 9.12 | +0.72 | +0.85 | 11.60% | 85.7% | **+0.66** | Active • Emerging Pressure Death Bowler |

---

## 3. Directory Structure
```
rr-submission/v3/
├── dashboard/
│   └── index.html                                          # Interactive Plotly Web App
├── Mohammed_Aleem_Bukkapatnam_RR_SupeRR_Selector_Report_v3.pdf  # Final PDF Report
├── scripts/
│   ├── build_v3_dashboard.py
│   ├── compile_v3_pdf_report.py
│   ├── generate_v3_figures.py
│   └── stage4_v3_rankings_active_roster.py
├── stage1_ball_leverage/
│   ├── ball_by_ball_pressure_v3.csv
│   └── stage1_summary_v3.json
├── stage2_player_aggregates/
│   ├── raw_batting_aggregates_v3.csv
│   └── raw_bowling_aggregates_v3.csv
├── stage3_bayesian_filtering/
│   ├── shrunken_batters_v3.csv
│   └── shrunken_bowlers_v3.csv
├── stage4_consistency_scoring/
│   ├── active_batters_v3_master.csv
│   ├── active_bowlers_v3_master.csv
│   ├── ranked_batters_v3_master.csv
│   ├── ranked_bowlers_v3_master.csv
│   ├── top10_batters_v3_final.csv
│   └── top10_bowlers_v3_final.csv
├── stage5_deliverables/
│   ├── figures/
│   │   ├── batter_clutch_matrix.png
│   │   ├── bowler_clutch_matrix.png
│   │   ├── top_10_batters_cbps.png
│   │   └── top_10_bowlers_cbps.png
│   ├── Mohammed_Aleem_Bukkapatnam_RR_SupeRR_Selector_Report_v3.pdf
│   ├── top10_batters_v3.csv
│   └── top10_bowlers_v3.csv
├── top10_batters_final.csv
├── top10_bowlers_final.csv
└── v3_pipeline_summary.json
```

