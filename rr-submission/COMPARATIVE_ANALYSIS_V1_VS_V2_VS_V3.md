# Comparative Architecture & Progression: Model v1 vs Model v2 vs Model v3

**Candidate:** Mohammed Aleem Bukkapatnam (M.S. in Artificial Intelligence)  
**Competition:** Rajasthan Royals SupeRR Selector Season 2 — Round 1 Case Study  

---

## 1. Executive Summary: The Three-Tier Evolution

To provide Rajasthan Royals with the most rigorous, scientifically defensible, and practically actionable assessment, our research progressed through three distinct modeling iterations:

1. **Model v1 (Baseline Dynamic Leverage Framework):**  
   - Established the ball-by-ball Dynamic Leverage Index ($LI \ge 1.50$) across 200,999 deliveries and 867 matches.  
   - Integrated Empirical Bayes shrinkage ($K=50$ balls) and match-level reliability scoring.
2. **Model v2 (Venue Pitch Par & Multi-Stage Calibrated Framework):**  
   - Ingested 365 match delivery logs (87,074 balls) from `ball-to-ball-stats/` to establish exact stadium par scoring rates ($Par_{venue}$) across 17 distinct venues.  
   - Applied championship playoff leverage multipliers ($1.20\times$ Qualifiers/Eliminators, $1.30\times$ Final) to decouple high-scoring ground stat-padding from true clutch execution.
3. **Model v3 (Active Roster Verified & Tournament Calibrated Framework):**  
   - **Enforces Criteria 1 (Active Roster Verification)**: Evaluates all candidates against **Option 3 (ESPNcricinfo official profile status)** and **Option 4 (Official public retirement announcements)**.  
   - Eliminates retired coaching personnel (**MS Dhoni**, transitioned to CSK Team Mentor; **Dinesh Karthik**, retired 1 June 2024, RCB coach; **Matthew Wade**, retired Oct 2024, Australia coach).  
   - Strictly preserves all active contracted and retained superstars (**Jos Buttler**, **Suryakumar Yadav**, **Jasprit Bumrah**, **Sunil Narine**, **Dhruv Jurel**, **Tim David**).  
   - Elevates Rajasthan Royals' retained clutch keeper-batter **Dhruv Jurel** to **#7**, **Marcus Stoinis** to **#8**, **Tristan Stubbs** to **#9**, and Australia/IPL power finisher **Tim David** to **#10**.

---

## 2. Multi-Dimensional Comparison Matrix

| Architectural Dimension | Model v1 (Baseline) | Model v2 (Venue-Calibrated) | Model v3 (Active Roster Calibrated) |
| :--- | :--- | :--- | :--- |
| **Total Deliveries Analyzed** | 200,999 balls (IPL + T20Is) | 200,999 balls + 87,074 pure IPL balls | 200,999 balls + 87,074 pure IPL balls |
| **Pressure Urgency Benchmark** | Static T20 League Baseline (9.00 RPO) | **Dynamic 17 Stadium Pars ($Par_{venue}$)** | **Dynamic 17 Stadium Pars ($Par_{venue}$)** |
| **Stage Leverage Weighting** | Flat knockout boost ($1.15\times$) | **Tiered:** Group ($1.00\times$), Qualifiers ($1.20\times$), Final ($1.30\times$) | **Tiered:** Group ($1.00\times$), Qualifiers ($1.20\times$), Final ($1.30\times$) |
| **Dual-Engine Differentials** | $\Delta = \text{Pressure} - \text{Baseline}$ | $\Delta_{venue} = \text{HP} - Par_{venue}$ & $\Delta_{base} = \text{HP} - \text{Base}$ | $\Delta_{venue} = \text{HP} - Par_{venue}$ & $\Delta_{base} = \text{HP} - \text{Base}$ |
| **Statistical Regularization** | Empirical Bayes ($K=50$ deliveries) | Empirical Bayes ($K=50$ deliveries) | Empirical Bayes ($K=50$ deliveries) |
| **Match-Level Reliability** | Min 8 HP balls per innings ($\text{SR} \ge 140$) | Min 8 HP balls per innings ($\text{SR} \ge 140$) | Min 8 HP balls per innings ($\text{SR} \ge 140$) |
| **Player Status Verification** | Unfiltered | Unfiltered | **Option 3 + 4 Cricinfo & Official Verification** |
| **Retired Personnel Included?** | Yes (Dhoni, Karthik, Wade) | Yes (Dhoni, Karthik, Wade) | **NO (100% Active Professional Roster)** |
| **Retained Players Included?** | Yes (Preserved) | Yes (Preserved) | **Yes (Preserved: Buttler, Surya, Bumrah, Narine, etc.)** |
| **Split-Half Reliability** | $r = 0.89$ | $r = 0.91$ | **$r = 0.92$** |

---

## 3. Side-by-Side Batting Leaderboard Evolution

| Rank | Model v1 Batter | Score | Model v2 Batter | Score | Model v3 Batter (Active Roster) | Score | Key Movement & Roster Status in v3 |
| :---: | :--- | :---: | :--- | :---: | :--- | :---: | :--- |
| **1** | MS Dhoni | 1.64 | Naman Dhir | 1.48 | **Naman Dhir** | **1.48** | Active (MI) • 194.89 HP SR (+46.6 vs venue par) |
| **2** | Naman Dhir | 1.49 | Ashutosh Sharma | 1.38 | **Ashutosh Sharma** | **1.38** | Active (DC) • +87.14 baseline elevation in crisis |
| **3** | Jos Buttler | 1.38 | Jos Buttler | 1.36 | **Jos Buttler** | **1.36** | Active • 100% match consistency in chases |
| **4** | Ashutosh Sharma | 1.35 | MS Dhoni | 1.32 | **Suryakumar Yadav** | **1.26** | Active (MI Retained) • 360-degree field sculptor |
| **5** | Dinesh Karthik | 1.30 | Suryakumar Yadav | 1.26 | **Shreyas Iyer** | **1.00** | Active • Championship playoff match winner |
| **6** | Suryakumar Yadav | 1.12 | Dinesh Karthik | 1.15 | **Glenn Phillips** | **0.90** | Active • Versatile lower-order striker |
| **7** | Matthew Wade | 0.82 | Shreyas Iyer | 1.00 | **Dhruv Jurel** | **0.89** | **Active (RR Retained)** • Moves to #7 with Dhoni & DK retired |
| **8** | Donovan Ferreira | 0.80 | Glenn Phillips | 0.90 | **Marcus Stoinis** | **0.82** | Active • Heavy power-hitter & counter-attacker |
| **9** | Shashank Singh | 0.75 | Dhruv Jurel | 0.89 | **Tristan Stubbs** | **0.81** | Active (DC Retained) • All-ground spin/pace striker |
| **10** | Sai Sudharsan | 0.74 | Matthew Wade | 0.84 | **Tim David** | **0.76** | **New Entry in Top 10** • 716 HP balls, 81.6% consistency |

> **Key Takeaway for Batters:**  
> In Model v3, removing retired coaching veterans (MS Dhoni, Dinesh Karthik, Matthew Wade) elevates **Dhruv Jurel** (Rajasthan Royals' own retained asset) into the official **Top 7**, while bringing **Marcus Stoinis**, **Tristan Stubbs**, and **Tim David** into the Top 10.

---

## 4. Side-by-Side Bowling Leaderboard Evolution

| Rank | Model v1 Bowler | Score | Model v2 Bowler | Score | Model v3 Bowler (Active Roster) | Score | Key Movement & Roster Status in v3 |
| :---: | :--- | :---: | :--- | :---: | :--- | :---: | :--- |
| **1** | Sunil Narine | 1.32 | Sunil Narine | 1.61 | **Sunil Narine** | **1.61** | Active (KKR Retained) • +2.90 venue suppression |
| **2** | Matheesha Pathirana | 1.00 | Matheesha Pathirana | 1.08 | **Matheesha Pathirana** | **1.08** | Active (CSK Retained) • 10.15% death wicket rate |
| **3** | Jasprit Bumrah | 0.94 | Jasprit Bumrah | 0.97 | **Jasprit Bumrah** | **0.97** | Active (MI Retained) • 7.41 HP Econ (+1.66 vs par) |
| **4** | Wanindu Hasaranga | 0.94 | Mitchell Santner | 0.89 | **Mitchell Santner** | **0.89** | Active • 95.7% consistency, 7.46 HP Econ |
| **5** | Mitchell Santner | 0.83 | Rashid Khan | 0.81 | **Rashid Khan** | **0.81** | Active (GT Retained) • 92.9% consistency over 800 balls |
| **6** | Rashid Khan | 0.79 | Varun Chakravarthy | 0.79 | **Varun Chakravarthy** | **0.79** | Active (KKR Retained) • 93.9% spell reliability |
| **7** | Taskin Ahmed | 0.79 | Taskin Ahmed | 0.75 | **Taskin Ahmed** | **0.75** | Active • 9.76% wicket rate in hard-length spells |
| **8** | Mitchell Starc | 0.75 | Jamie Overton | 0.69 | **Jamie Overton** | **0.69** | Active • Heavy hit-the-deck strike pace (12.38% wkt) |
| **9** | Jamie Overton | 0.68 | Mitchell Starc | 0.68 | **Mitchell Starc** | **0.68** | Active • 16.07% wicket rate (1 wkt every 6.2 balls) |
| **10** | Varun Chakravarthy | 0.61 | Rasikh Salam | 0.66 | **Rasikh Salam** | **0.66** | Active • Emerging death pacer (+0.72 vs venue par) |

> **Key Takeaway for Bowlers:**  
> All 10 bowlers in Model v2 were already 100% active professional cricketers. Their rankings remain rock-solid in Model v3, led by Sunil Narine's peerless run-strangle (+1.61) and Matheesha Pathirana's yorker mastery (+1.08).

---

## 5. Final Recommendation for Unstop Submission

**Submit Model v3 (`rr-submission/v3/`):**
1. **Unstop Dropdown Alignment:** Every single player in Model v3 is an **active, available professional cricketer** without any retired coaching personnel.
2. **Contextual Rigor:** Grounded in 17 stadium scoring pars and championship playoff multipliers.
3. **Royals Alignment:** Quantitatively validates Rajasthan Royals' retention of **Dhruv Jurel** as an empirical Top 8 clutch asset globally.
4. **Complete Preservation:** All three iterations are meticulously archived in `rr-submission/v1/`, `rr-submission/v2/`, and `rr-submission/v3/`.

