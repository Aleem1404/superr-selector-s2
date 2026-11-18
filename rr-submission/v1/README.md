# Rajasthan Royals SupeRR Selector Season 2 — Round 1 Submission
## Identifying the Most Reliable Players Under Pressure

**Candidate:** Mohammed Aleem Bukkapatnam (M.S. in Artificial Intelligence)  
**Target Evaluation Panel:** Giles Lindsay (Head of Analytics), Kumar Sangakkara (Director of Cricket), Rajasthan Royals  
**Dataset:** 200,999 Deliveries across 867 Matches (IPL & T20I, 2022–2026)  

---

### Folder Structure & Reproducible Pipeline

This folder contains the complete, stage-wise data engineering pipeline, statistical modeling, intermediate artifacts, and final deliverables for the Round 1 submission:

```
rr-submission/
├── scripts/                               # Complete Python source pipeline
│   ├── stage1_calculate_leverage.py       # Ball-level leverage & Pressure Index (PI) calculation
│   ├── stage2_aggregate_players.py        # Baseline vs High-Pressure aggregation
│   ├── stage3_bayesian_shrinkage.py       # Empirical Bayes shrinkage (K=50 balls)
│   ├── stage4_rankings_consistency.py     # Match reliability & Composite Pressure Scores (CBPS)
│   ├── build_dashboard.py                 # Standalone interactive Plotly HTML dashboard generator
│   └── compile_submission_pdf.py          # ReportLab script compiling publication-grade PDF report
│
├── stage1_ball_leverage/                  # STAGE 1 OUTPUTS
│   ├── ball_by_ball_pressure.csv          # All 200,999 deliveries tagged with Pressure Index (PI)
│   └── stage1_summary.json                # Summary: 58,447 HP balls (29.08% leverage boundary)
│
├── stage2_player_aggregates/              # STAGE 2 OUTPUTS
│   ├── raw_batting_aggregates.csv         # 888 batters: Base SR, HP SR, Delta SR, Dot %
│   └── raw_bowling_aggregates.csv         # 647 bowlers: Base Econ, HP Econ, Delta Econ, Wkt %
│
├── stage3_bayesian_filtering/             # STAGE 3 OUTPUTS
│   ├── shrunken_batters.csv               # 102 eligible batters stabilized via Bayes shrinkage
│   └── shrunken_bowlers.csv               # 115 eligible bowlers stabilized via Bayes shrinkage
│
├── stage4_consistency_scoring/            # STAGE 4 OUTPUTS
│   ├── ranked_batters_master.csv          # All eligible batters ranked by CBPS score
│   ├── ranked_bowlers_master.csv          # All eligible bowlers ranked by CBPS score
│   ├── top10_batters_final.csv            # Official Top 10 Batters (Unstop selections)
│   └── top10_bowlers_final.csv            # Official Top 10 Bowlers (Unstop selections)
│
├── stage5_deliverables/                   # FINAL DELIVERABLES
│   ├── figures/                           # High-res figures (Clutch matrices & CBPS bar charts)
│   └── Mohammed_Aleem_Bukkapatnam_RR_SupeRR_Selector_Report.pdf
│
├── dashboard/                             # INTERACTIVE WEB DASHBOARD
│   └── index.html                         # Standalone interactive web dashboard (ready for 1-click deploy)
│
├── top10_batters_final.csv                # Top 10 Batters quick-access table
├── top10_bowlers_final.csv                # Top 10 Bowlers quick-access table
└── Mohammed_Aleem_Bukkapatnam_RR_SupeRR_Selector_Report.pdf  # Main submission PDF report
```

---

### Official Final Rankings for Unstop Dropdown

#### Top 10 Batters Under High Pressure:
1. **MS Dhoni** (Score: 1.64 | HP SR: 156.1 | &Delta;SR: +99.0 | HP Balls: 415)
2. **Naman Dhir** (Score: 1.49 | HP SR: 196.2 | &Delta;SR: +41.6 | Consistency: 92.9%)
3. **Jos Buttler** (Score: 1.38 | HP SR: 186.9 | &Delta;SR: +34.3 | Consistency: 100.0%)
4. **Ashutosh Sharma** (Score: 1.35 | HP SR: 168.3 | &Delta;SR: +76.7 | HP Balls: 315)
5. **Dinesh Karthik** (Score: 1.30 | HP SR: 169.7 | &Delta;SR: +57.3 | HP Balls: 534)
6. **Suryakumar Yadav** (Score: 1.12 | HP SR: 189.3 | &Delta;SR: +31.5 | Consistency: 72.7%)
7. **Matthew Wade** (Score: 0.82 | HP SR: 157.3 | &Delta;SR: +45.6 | Consistency: 75.0%)
8. **Donovan Ferreira** (Score: 0.80 | HP SR: 175.5 | &Delta;SR: +33.9 | Consistency: 75.0%)
9. **Shashank Singh** (Score: 0.75 | HP SR: 171.7 | &Delta;SR: +44.4 | Consistency: 64.7%)
10. **Sai Sudharsan** (Score: 0.74 | HP SR: 177.2 | &Delta;SR: +29.8 | Consistency: 90.0%)

#### Top 10 Bowlers Under High Pressure:
1. **Sunil Narine** (Score: 1.32 | HP Econ: 6.44 | Dot%: 40.0% | Consistency: 95.0%)
2. **Matheesha Pathirana** (Score: 1.00 | HP Econ: 8.49 | Wkt%: 10.1% | Consistency: 91.7%)
3. **Jasprit Bumrah** (Score: 0.94 | HP Econ: 7.37 | Wkt%: 8.7% | Consistency: 80.0%)
4. **Wanindu Hasaranga** (Score: 0.94 | HP Econ: 8.34 | Wkt%: 10.0% | Consistency: 92.9%)
5. **Mitchell Santner** (Score: 0.83 | HP Econ: 7.43 | Dot%: 35.1% | Consistency: 95.7%)
6. **Rashid Khan** (Score: 0.79 | HP Econ: 8.16 | Wkt%: 8.4% | Consistency: 92.7%)
7. **Taskin Ahmed** (Score: 0.79 | HP Econ: 8.62 | Wkt%: 9.8% | Consistency: 87.5%)
8. **Mitchell Starc** (Score: 0.75 | HP Econ: 10.23 | Wkt%: 15.8% | Consistency: 87.5%)
9. **Jamie Overton** (Score: 0.68 | HP Econ: 8.67 | Dot%: 40.0% | Consistency: 70.0%)
10. **Varun Chakravarthy** (Score: 0.61 | HP Econ: 8.45 | Dot%: 39.0% | Consistency: 93.9%)

---

### How to Run the Pipeline
All scripts run out of the box using Python:
```bash
python rr-submission/scripts/stage1_calculate_leverage.py
python rr-submission/scripts/stage2_aggregate_players.py
python rr-submission/scripts/stage3_bayesian_shrinkage.py
python rr-submission/scripts/stage4_rankings_consistency.py
python rr-submission/scripts/build_dashboard.py
python rr-submission/scripts/compile_submission_pdf.py
```

