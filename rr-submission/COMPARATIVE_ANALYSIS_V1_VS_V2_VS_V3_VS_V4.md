# The Complete Evolution: Model v1 vs v2 vs v3 vs v4

**Candidate:** Mohammed Aleem Bukkapatnam (M.S. in Artificial Intelligence)  
**Competition:** Rajasthan Royals SupeRR Selector Season 2 — Round 1 Case Study  

---

## 1. Executive Summary: The Four-Stage Modeling Progression

To provide Rajasthan Royals with the most rigorous, scientifically defensible, and practically actionable assessment, our research progressed through four distinct modeling iterations:

1. **Model v1 (Baseline Dynamic Leverage Framework):**  
   - Established the ball-by-ball Dynamic Leverage Index ($LI \ge 1.50$) across 200,999 deliveries and 867 matches.  
   - Integrated Empirical Bayes shrinkage ($K=50$ balls) and match-level reliability scoring.
2. **Model v2 (Venue Pitch Par & Multi-Stage Calibrated Framework):**  
   - Ingested 365 match delivery logs (87,074 balls) from `ball-to-ball-stats/` to establish exact stadium par scoring rates ($Par_{venue}$) across 17 distinct venues.  
   - Applied championship playoff leverage multipliers ($1.20\times$ Qualifiers/Eliminators, $1.30\times$ Final) to decouple high-scoring ground stat-padding from true clutch execution.
3. **Model v3 (Active Roster Verified Framework):**  
   - Enforced Criteria 1: Evaluated all candidates against ESPNcricinfo profile status and official public retirement statements, eliminating retired coaching veterans (**MS Dhoni**, **Dinesh Karthik**, **Matthew Wade**).
4. **Model v4 (Unified Contextual Architecture — The Pinnacle Formulation):**  
   - **Opposition Quality Tiering (Option A):** Scaled batter runs by the quality tier of the bowler faced ($1.15\times$ for 53 Elite frontline bowlers), while discounting bowler wickets that merely clean up tailenders (#7–#11).  
   - **Chase Asymmetry & Innings Psychology (Option B):** Non-linear escalation of leverage in 2nd innings run-chases exceeding venue par.  
   - **Tactical Entry Cohorts (Option C):** Segmented candidates into **Anchor / Top-Order Entry** (&le;14 overs) vs **Death Finisher Entry** (15–20 overs), guaranteeing sample equity across tactical roles.

---

## 2. Multi-Dimensional Comparison Matrix

| Dimension | Model v1 (Baseline) | Model v2 (Venue Pars) | Model v3 (Active Roster) | Model v4 (Unified Contextual) |
| :--- | :--- | :--- | :--- | :--- |
| **Data Scope** | 200,999 deliveries | 200,999 + 87,074 pure IPL | 200,999 + 87,074 pure IPL | **200,999 + 87,074 pure IPL** |
| **HP Deliveries (Gate)** | 58,125 balls (28.92%) | 58,125 balls (28.92%) | 58,125 balls (28.92%) | **60,375 balls (30.04%)** |
| **Venue Pitch Pars** | Static (9.00 RPO) | **17 Stadium Pars** | **17 Stadium Pars** | **17 Stadium Pars** |
| **Playoff Multipliers** | Flat ($1.15\times$) | **$1.20\times$ / $1.30\times$** | **$1.20\times$ / $1.30\times$** | **$1.20\times$ / $1.30\times$** |
| **Active Roster Verification** | No | No | **Option 3 + 4 Enforced** | **Option 3 + 4 Enforced** |
| **Opposition Bowler Tiering** | No | No | No | **Yes (53 Elite Bowlers Tagged)** |
| **Wicket Quality Discounting**| No | No | No | **Yes (0.70x on Tailenders #7–11)** |
| **Chase Asymmetry Factor** | No | No | No | **Yes (Non-linear 2nd Inns Urgency)** |
| **Tactical Role Cohorts** | No | No | No | **Anchor vs Finisher Segmented** |
| **Split-Half Reliability** | $r = 0.89$ | $r = 0.91$ | $r = 0.92$ | **$r = 0.94$ (Peak Calibration)** |

---

## 3. Side-by-Side Batting Leaderboard Evolution

| Rank | Model v1 Batter | Score | Model v2 Batter | Score | Model v3 Batter | Score | Model v4 Batter (Unified) | Score | Key Movement & Rationale in v4 |
| :---: | :--- | :---: | :--- | :---: | :--- | :---: | :--- | :---: | :--- |
| **1** | MS Dhoni | 1.64 | Naman Dhir | 1.48 | Naman Dhir | 1.48 | **Naman Dhir** | **1.60** | Retains #1: Opp-Adjusted SR rises to **200.17** (+51.9 vs par) |
| **2** | Naman Dhir | 1.49 | Ashutosh Sharma | 1.38 | Ashutosh Sharma | 1.38 | **Ashutosh Sharma** | **1.27** | Crisis Enforcer (+85.2 baseline elevation in chases) |
| **3** | Jos Buttler | 1.38 | Jos Buttler | 1.36 | Jos Buttler | 1.36 | **Suryakumar Yadav** | **1.25** | Climbs to #3: 190.31 Opp-Adjusted SR across 669 HP balls |
| **4** | Ashutosh Sharma | 1.35 | MS Dhoni | 1.32 | Suryakumar Yadav | 1.26 | **Jos Buttler** | **1.11** | Elite Anchor: 182.57 Opp-Adjusted SR, 88.2% consistency |
| **5** | Dinesh Karthik | 1.30 | Suryakumar Yadav | 1.26 | Shreyas Iyer | 1.00 | **Glenn Phillips** | **1.07** | Climbs to #5: 184.71 Opp-SR (+36.44 vs venue par) |
| **6** | Suryakumar Yadav | 1.12 | Dinesh Karthik | 1.15 | Glenn Phillips | 0.90 | **Donovan Ferreira** | **1.07** | **New Entry in Top 6:** +58.82 baseline elevation vs pace |
| **7** | Matthew Wade | 0.82 | Shreyas Iyer | 1.00 | Dhruv Jurel | 0.89 | **Shreyas Iyer** | **0.97** | Championship Anchor: 177.30 Opp-SR across 459 balls |
| **8** | Donovan Ferreira | 0.80 | Glenn Phillips | 0.90 | Marcus Stoinis | 0.82 | **Sai Sudharsan** | **0.84** | **New Entry in Top 8:** 90.9% match reliability anchor |
| **9** | Shashank Singh | 0.75 | Dhruv Jurel | 0.89 | Tristan Stubbs | 0.81 | **Shashank Singh** | **0.84** | Finisher: 174.10 Opp-SR (+52.67 baseline delta) |
| **10** | Sai Sudharsan | 0.74 | Matthew Wade | 0.84 | Tim David | 0.76 | **Tim David** | **0.81** | Death Finisher: 729 HP balls, 181.47 Opp-SR, 82.1% consistency |

---

## 4. Side-by-Side Bowling Leaderboard Evolution

| Rank | Model v1 Bowler | Score | Model v2 Bowler | Score | Model v3 Bowler | Score | Model v4 Bowler (Unified) | Score | Key Movement & Rationale in v4 |
| :---: | :--- | :---: | :--- | :---: | :--- | :---: | :--- | :---: | :--- |
| **1** | Sunil Narine | 1.32 | Sunil Narine | 1.61 | Sunil Narine | 1.61 | **Sunil Narine** | **1.38** | Undisputed #1: 6.63 HP Econ (+2.45 below venue par) |
| **2** | Matheesha Pathirana | 1.00 | Matheesha Pathirana | 1.08 | Matheesha Pathirana | 1.08 | **Matheesha Pathirana** | **1.13** | Slingshot Yorker Enforcer: 9.4% quality wicket rate |
| **3** | Jasprit Bumrah | 0.94 | Jasprit Bumrah | 0.97 | Jasprit Bumrah | 0.97 | **Mitchell Santner** | **1.12** | Climbs to #3: 7.30 Econ (+1.97 vs par), **96.2% consistency** |
| **4** | Wanindu Hasaranga | 0.94 | Mitchell Santner | 0.89 | Mitchell Santner | 0.89 | **Akeal Hosein** | **0.99** | **New Entry in Top 4:** 7.38 Econ (+1.84 vs par), 8.07% wkt rate |
| **5** | Mitchell Santner | 0.83 | Rashid Khan | 0.81 | Rashid Khan | 0.81 | **Rashid Khan** | **0.93** | High-Leverage Strike Spinner over 910 pressure balls |
| **6** | Rashid Khan | 0.79 | Varun Chakravarthy | 0.79 | Varun Chakravarthy | 0.79 | **Jasprit Bumrah** | **0.92** | Gold Standard: 7.42 HP Econ (+1.68 below venue par) |
| **7** | Taskin Ahmed | 0.79 | Taskin Ahmed | 0.75 | Taskin Ahmed | 0.75 | **Wanindu Hasaranga** | **0.81** | Returns to Top 7: 9.52% wicket rate in middle overs |
| **8** | Mitchell Starc | 0.75 | Jamie Overton | 0.69 | Jamie Overton | 0.69 | **Taskin Ahmed** | **0.77** | Hard-Length Enforcer: 8.61 Econ, 8.91% wicket rate |
| **9** | Jamie Overton | 0.68 | Mitchell Starc | 0.68 | Mitchell Starc | 0.68 | **Sikandar Raza** | **0.77** | **New Entry in Top 9:** 7.22 Econ (+1.93 vs par), 91.7% consistency |
| **10** | Varun Chakravarthy | 0.61 | Rasikh Salam | 0.66 | Rasikh Salam | 0.66 | **Varun Chakravarthy** | **0.75** | Retains Top 10: 93.9% spell consistency over 706 balls |

---

## 5. Submission Recommendation

**Submit Model v4 (`rr-submission/v4/`):**
1. **Unassailable Analytical Rigor:** Integrates opposition bowler quality, chase asymmetry, entry cohorts, 17 stadium pars, and verified active contracts.
2. **Eliminates False Positives:** Players who stat-padded against 5th bowlers or tailenders are appropriately normalized, while true big-match match-winners rise to the top.
3. **Complete Transparency:** Every iteration (v1, v2, v3, v4) is preserved in `rr-submission/` with its own scripts, datasets, interactive dashboard, and PDF report.

