# SupeRR Selector Season 2: Identifying the Most Reliable Players Under Pressure
## A Rigorous Data-Driven Framework for Round 1 Evaluation

**Author:** Mohammed Aleem Bukkapatnam (M.S. in Artificial Intelligence)  
**Target Panel:** Giles Lindsay (Head of Analytics), Kumar Sangakkara (Director of Cricket), Rajasthan Royals  
**Date:** November 2026  

---

## Executive Summary

When games are on the line, average statistics fail to capture value. A batter with an overall strike rate of 145 may collapse to 110 when the required run rate climbs above 11. Conversely, true clutch performers elevate their execution, suppress dot balls, and absorb pressure.

To identify cricket's most reliable players under pressure, we built a **Dynamic Leverage & Multi-Context Pressure Model** evaluating all **200,999 deliveries across 867 matches (IPL and T20 Internationals from 2022 to 2026)**. By decoupling baseline performance from high-leverage execution and applying Empirical Bayes shrinkage with match-level reliability scoring, we uncovered the definitive Top 10 Batters and Top 10 Bowlers who consistently deliver when it matters most.

---

## 1. Pressure Definition: Dynamic Leverage Index ($LI$) & Match State Architecture

Pressure in T20 cricket is not static, nor is it simply confined to arbitrary overs. A delivery in over 18 of a blowout (requiring 12 runs off 18 balls with 8 wickets in hand) carries virtually zero pressure. In contrast, an over bowled in a Powerplay where a team has slumped to $18/3$, or a chase needing 38 off 18 balls, carries immense structural leverage.

We define the **Pressure Index ($PI_t \in [0, 1]$)** for every delivery $t$ across two distinct game architectures:

### 1.1 Second Innings (The Chase): Chasing Leverage & Urgency Function
In a chase, every ball alters the probability of victory. Pressure is parameterized across three interdependent dynamics:
1. **Required Run Rate Urgency ($U_{RRR}$):** Non-linear sigmoid scaling centered at modern T20 league par ($9.0\text{ RPO}$):
   $$U_{RRR} = \frac{1}{1 + e^{-0.5(RRR_t - 9.0)}}$$
2. **Temporal Decay / Balls Remaining Factor ($D_{balls}$):** As balls deplete, error margins shrink:
   $$D_{balls} = 1 - \frac{\text{Balls Remaining}}{120}$$
3. **Wicket Depletion Risk ($W_{lev}$):** Non-linear penalty as batting depth erodes:
   $$W_{lev} = 1 - \left(\frac{W_{in\_hand}}{10}\right)^{1.2}$$

The Chase Pressure Index is formulated as:
$$PI_{chase} = \text{clip}\left(0.40 \cdot U_{RRR} + 0.35 \cdot D_{balls} \cdot \left(\frac{RRR_t}{8.5}\right) + 0.25 \cdot W_{lev}, 0, 1\right)$$

### 1.2 First Innings (Setting the Target): Death Leverage & Crisis Recovery
1. **Death Overs Execution ($overid \ge 16$, balls 91–120):** Every dot ball or boundary causes severe shifts between sub-par ($<170$) and match-winning ($200+$) totals:
   $$PI_{death} = 0.55 + 0.08 \times (overid - 16) + 0.15 \times \left(\frac{W_{lost}}{10}\right)$$
2. **Top-Order Collapse / Crisis Situations:**
   - $\le 6$ overs and $\ge 3$ wickets lost: $PI = 0.70$
   - $\le 10$ overs and $\ge 4$ wickets lost: $PI = 0.65$
   - Ordinary 1st innings play: $PI = 0.30$

### 1.3 Tournament Stakes & High-Pressure Threshold
- **Knockout / Playoff Multiplier:** Knockout matches (Finals, Qualifiers, Eliminators, Semi-Finals) receive a $1.15\times$ multiplier.
- **Super Overs:** $PI = 1.00$ (Absolute pressure).
- **The High-Pressure Boundary:** Deliveries with $PI_t \ge 0.60$ constitute the **High-Pressure (HP)** regime ($29.1\%$ of all deliveries, $N = 58,442$), cleanly separating routine passages from high-leverage battles.

---

## 2. Performance Measurement & Scoring Framework

To reward players who genuinely elevate their execution—and not simply players who feast in low-leverage situations—we evaluate differential metrics ($\Delta = \text{Pressure} - \text{Baseline}$) alongside absolute pressure output.

### 2.1 Empirical Bayes Shrinkage for Sample Normalization
To prevent small-sample distortions (e.g. a tail-ender hitting 2 sixes in 5 balls), all raw pressure rates are shrunken toward the league high-pressure prior ($\mu_0$):
$$\widehat{\theta}_i = \left(\frac{N_i}{N_i + K}\right) \cdot \theta_i^{\text{raw}} + \left(\frac{K}{N_i + K}\right) \cdot \mu_0$$
- Batters: $\mu_{SR} = 135.0, \mu_{Dot} = 36.0\%, K = 50\text{ balls}$.
- Bowlers: $\mu_{ER} = 9.20, \mu_{Wkt} = 7.0\%, K = 50\text{ balls}$.

### 2.2 Composite Batter Pressure Score (CBPS)
A multi-criteria rating combining:
1. **Shrunk Pressure Strike Rate ($z_{SR}$ - $30\%$):** Ability to score rapidly in crunch time.
2. **Delta Strike Rate ($z_{\Delta SR}$ - $25\%$):** $\Delta SR = SR_{hp} - SR_{base}$ (Scoring elevation).
3. **Dot Ball Resistance ($z_{\Delta Dot}$ - $20\%$):** $\Delta Dot\% = Dot_{base} - Dot_{hp}$ (Suppressing empty deliveries).
4. **Pressure Boundary Conversion ($z_{Bnd}$ - $15\%$):** Boundary striking capability.
5. **Match Consistency Rate ($z_{Cons}$ - $10\%$):** $\%$ of high-pressure innings ($N \ge 8\text{ balls}$) with $SR \ge 140.0$.
$$\text{CBPS} = \text{Raw CBPS} \times \min\left(1.0, \sqrt{\frac{N_{hp}}{250}}\right)$$

### 2.3 Composite Bowler Pressure Score (CBPS)
A multi-criteria rating combining:
1. **Shrunk Pressure Economy Suppression ($z_{ER}$ - $30\%$):** Conceding fewer runs under pressure.
2. **Pressure Wicket-Taking Threat ($z_{Wkt}$ - $25\%$):** Striking under pressure.
3. **Dot Ball Generation ($z_{Dot}$ - $15\%$):** Building scoreboard pressure.
4. **Boundary Prevention ($z_{Bnd}$ - $15\%$):** Denying 4s and 6s in crunch overs.
5. **Match Spell Reliability ($z_{Cons}$ - $15\%$):** $\%$ of high-pressure spells where bowler conceded $\le 8.5\text{ ER}$ or took $\ge 1\text{ wicket}$.
$$\text{CBPS} = \text{Raw CBPS} \times \min\left(1.0, \sqrt{\frac{N_{hp}}{250}}\right)$$

---

## 3. Fair Comparisons: Eligibility, Sample Sizes, and Context

1. **Volume Qualifications:**
   - Minimum threshold: $\ge 200\text{ High-Pressure balls}$ faced/bowled (equivalent to $33.3$ full overs of high-pressure cricket).
2. **Competition Weighting:**
   - Deliveries in the IPL are weighted at $1.00$ (highest opposition concentration).
   - Major T20Is (ICC Tournaments, Asia Cup, top-tier clashes) weighted at $0.95$.
   - Bilateral series vs associates weighted at $0.85$.
3. **Auction Viability for Rajasthan Royals:**
   - By BCCI regulations, Pakistani players cannot enter the IPL auction. To make this submission directly operational for Rajasthan Royals' IPL 2027 auction table, rankings are filtered for IPL auction eligibility while international baseline comparisons are transparently retained.

---

## 4. Evidence for the Top 10 Picks

### 4.1 Top 10 Batters Under Pressure (Selected Order)

| Rank | Player Name | HP Balls | HP SR | Base SR | $\Delta$ Strike Rate | HP Dot % | Match Consistency | CBPS Score | Tactical Scouting Archetype |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **1** | **Mahendra Singh Dhoni** | 415 | 156.1 | 54.9 | **+99.0** | 38.1% | 59.1% | **1.64** | Supreme Clutch Finisher / Target Manager |
| **2** | **Naman Dhir** | 237 | **196.2** | 144.0 | **+41.6** | **27.0%** | **92.9%** | **1.49** | Elite Emerging Finisher / Spin & Pace Hitter |
| **3** | **Jos Buttler** | 335 | 186.9 | 145.8 | **+34.3** | **27.2%** | **100.0%** | **1.38** | Anchor-to-Explosion Match Winner |
| **4** | **Ashutosh Sharma** | 315 | 168.3 | 87.0 | **+76.7** | 35.9% | 62.5% | **1.35** | High-Leverage Rescuer / Boundary Hunter |
| **5** | **Dinesh Karthik** | 534 | 169.7 | 109.4 | **+57.3** | 33.3% | 61.8% | **1.30** | Specialized Death Overs Executioner |
| **6** | **Suryakumar Yadav** | 607 | 189.3 | 153.6 | **+31.5** | 30.1% | 72.7% | **1.12** | 360° Field Manipulator / Middle-Overs Clutch |
| **7** | **Mark Adair** | 257 | 142.8 | 74.1 | **+67.5** | 40.1% | 56.2% | **0.88** | Lower-Order Power Hitter (Death Overs) |
| **8** | **Matthew Wade** | 225 | 157.3 | 107.7 | **+45.6** | 31.1% | 75.0% | **0.82** | Pressure Chase Finisher (Pace Hitter) |
| **9** | **Donovan Ferreira** | 212 | 175.5 | 133.8 | **+33.9** | 34.9% | 75.0% | **0.80** | Explosive Middle-Order Ball Striker |
| **10** | **Shashank Singh** | 374 | 171.7 | 122.9 | **+44.4** | 29.1% | 64.7% | **0.75** | Crisis Recovery Specialist / Chase Clincher |

#### Key Analytical Findings - Batting:
* **The Breakout Sensation (Naman Dhir - Rank 2):** In 237 high-pressure balls, Naman Dhir posted a staggering **196.2 SR** with a minuscule **27.0% dot ball rate** and **92.9% match-level consistency**. He is a prime target for RR's middle-order finishing rebuild.
* **The Royally Proven Anchor-Finisher (Jos Buttler - Rank 3):** Delivered a perfect **100.0% clutch consistency rate** in high-pressure situations, striking at **186.9** with only 27.2% dots.
* **Crisis Chasers (Ashutosh Sharma & Shashank Singh):** Boast massive positive $\Delta SR$ values ($+76.7$ and $+44.4$), demonstrating rare ability to accelerate when teammates struggle.

---

### 4.2 Top 10 Bowlers Under Pressure (Selected Order)

| Rank | Player Name | HP Balls | HP Econ | Base Econ | $\Delta$ Economy | HP Wkt % | HP Dot % | Match Consistency | CBPS Score | Tactical Scouting Archetype |
|:---:|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---|
| **1** | **Sunil Narine** | 408 | **6.44** | 7.00 | **+0.26** | 6.9% | **40.0%** | **95.0%** | **1.32** | Suffocating Mystery Spin / Middle & Death |
| **2** | **Matheesha Pathirana** | 601 | 8.49 | 8.69 | **+0.14** | **10.1%** | 39.3% | 91.7% | **1.00** | Slingshot Yorker King / Death Overs Enforcer |
| **3** | **Jasprit Bumrah** | 635 | **7.37** | 7.05 | -0.45 | 8.7% | 37.3% | 80.0% | **0.94** | Benchmark All-Phase Executioner |
| **4** | **Wanindu Hasaranga** | 511 | 8.34 | 7.78 | -0.63 | **10.0%** | 36.6% | 92.9% | **0.94** | Attacking Wrist-Spin Wicket Hunter |
| **5** | **Mitchell Santner** | 416 | **7.43** | 7.38 | -0.24 | 6.7% | 35.1% | **95.7%** | **0.83** | Defensive Left-Arm Match Controller |
| **6** | **Rashid Khan** | 797 | 8.16 | 7.10 | -1.13 | 8.4% | 36.9% | 92.7% | **0.79** | High-Leverage Partnership Breaker |
| **7** | **Taskin Ahmed** | 328 | 8.62 | 7.59 | -1.10 | 9.8% | 39.3% | 87.5% | **0.79** | High-Pace Hard-Length Enforcer |
| **8** | **Mitchell Starc** | 234 | 10.23 | 9.32 | -0.73 | **15.8%** | 35.5% | 87.5% | **0.75** | Elite Strike Weapon (Wicket every 6.3 balls) |
| **9** | **Jamie Overton** | 200 | 8.67 | 8.52 | -0.26 | **12.0%** | **40.0%** | 70.0% | **0.68** | Enforcer Pace & Heavy Ball Bowler |
| **10** | **Varun Chakravarthy** | 695 | 8.45 | 7.74 | -0.76 | 7.5% | 39.0% | 93.9% | **0.61** | Middle & Death Spin Constrictor |

#### Key Analytical Findings - Bowling:
* **The Gold Standard (Sunil Narine - Rank 1):** Concedes only **6.44 RPO** across 408 pressure deliveries with **40.0% dot balls** and a **95.0% consistency rate**.
* **The Strike Weapons (Pathirana & Starc):** Pathirana took **61 high-pressure wickets** (10.1% rate), while Starc strikes at a breathtaking **15.8% rate** (1 wicket every 6.3 deliveries in high leverage).
* **Death Economy Masters (Bumrah & Santner):** Bumrah's **7.37 economy** over 635 pressure balls remains unmatched for pace bowling across the tournament sample.

---

## 5. Reliability, Model Validation & Limitations

### 5.1 Robustness & Cross-Validation
* **Phase Invariance:** The model was tested across both 1st innings death and 2nd innings chases. Rankings remained highly robust ($r = 0.89$ rank correlation when splitting odd/even match IDs).
* **Inter-Match Stability:** The consistency parameter explicitly rewards performers whose value is distributed across multiple campaigns rather than bloated by a single outlier match.

### 5.2 Methodological Limitations
1. **Impact of Toss & Dew:** Certain venues (e.g., Wankhede, Eden Gardens) experience significant dew in the 2nd innings, inflating chasing strike rates and bowling economy rates. While venue factors were monitored, ball-level dew tracking is unrecorded in public feeds.
2. **Fielding & Catch Drop Bias:** Bowler economy and wicket metrics do not credit dropped catches. Expected Wickets ($xW$) could be incorporated in future iterations with tracking camera data.
3. **Role Specialization:** Pure death bowlers (e.g. Starc, Pathirana) naturally carry higher economies than middle-overs spin restrictors (Narine, Santner), which our multi-component weighting balances through the strike rate and boundary suppression terms.

---

## Conclusion & Summary

In accordance with Round 1 objectives, this study has:
1. **Mathematically Defined Pressure** using a dynamic, ball-by-ball leverage framework ($PI_t$) accounting for chase urgency, temporal decay, wicket risk, and tournament stakes.
2. **Evaluated Performance Under Pressure** through differential metrics ($\Delta$SR, $\Delta$ER, dot suppression, and match-level consistency) stabilized via Empirical Bayes shrinkage.
3. **Delivered the Definitive Top 10 Batters and Top 10 Bowlers**, separating genuine high-leverage performers from players whose statistics depend on low-pressure accumulation.

*All supporting data, scripts, and visualizations are available in the project repository.*

