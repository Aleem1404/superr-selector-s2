# Rajasthan Royals SupeRR Selector Season 2 — Model v2
## Venue-Adjusted Pitch Par & Playoff-Calibrated Pressure Engine

**Candidate:** Mohammed Aleem Bukkapatnam (M.S. in Artificial Intelligence)  
**Evaluation Panel:** Giles Lindsay (Head of Analytics), Kumar Sangakkara (Director of Cricket), Rajasthan Royals  
**Data Sources:** 200,999 Deliveries (IPL & T20I) + 365 Match Stadium Logs from `ball-to-ball-stats/`  

---

### Key Innovations in Model v2

1. **Venue-Adjusted Pitch Par ($Par_{venue}$):**
   * Incorporates exact historical scoring rates for 17 stadiums (Jaipur: 9.36, Guwahati: 8.72, Chennai: 8.27, Bengaluru: 9.36, Ahmedabad: 8.98).
   * Calculates $\Delta \text{SR}_{venue} = \text{HP\_SR} - \text{Expected\_SR}_{venue}$ and $\Delta \text{Econ}_{venue} = Par_{venue} - \text{HP\_Econ}$.
2. **Playoff Stage Weighting:**
   * Qualifier & Eliminator matches receive a $1.20\times$ multiplier; IPL Finals receive $1.30\times$.
3. **Dual-Horizon Quality Weighting:**
   * IPL deliveries are weighted at $1.15\times$ relative to bilateral internationals, eliminating distortion from lower-tier international opponents.

---

### Final Top 10 Dropdown Selections (Model v2)

#### Top 10 Batters (v2):
1. **Naman Dhir** (Score: 1.48 | HP SR: 194.9 | Venue &Delta;SR: +46.6 | Consistency: 92.9%)
2. **Ashutosh Sharma** (Score: 1.38 | HP SR: 171.0 | Base &Delta;SR: +87.1 | Dot%: 34.9%)
3. **Jos Buttler** (Score: 1.36 | HP SR: 185.0 | Venue &Delta;SR: +34.5 | Consistency: 100.0%)
4. **MS Dhoni** (Score: 1.32 | HP SR: 156.8 | Base &Delta;SR: +101.5 | HP Balls: 412)
5. **Suryakumar Yadav** (Score: 1.26 | HP SR: 188.8 | Venue &Delta;SR: +43.1 | Consistency: 77.4%)
6. **Dinesh Karthik** (Score: 1.15 | HP SR: 170.0 | Base &Delta;SR: +61.3 | HP Balls: 533)
7. **Shreyas Iyer** (Score: 1.00 | HP SR: 177.6 | Venue &Delta;SR: +29.6 | Consistency: 80.0%)
8. **Glenn Phillips** (Score: 0.90 | HP SR: 179.2 | Venue &Delta;SR: +30.9 | Consistency: 78.6%)
9. **Dhruv Jurel** (Score: 0.89 | HP SR: 171.1 | Venue &Delta;SR: +21.1 | Consistency: 83.3%)
10. **Matthew Wade** (Score: 0.84 | HP SR: 158.7 | Consistency: 75.0%)

#### Top 10 Bowlers (v2):
1. **Sunil Narine** (Score: 1.61 | HP Econ: 6.20 | Venue Run Suppression: +2.90 RPO | Consistency: 95.2%)
2. **Matheesha Pathirana** (Score: 1.08 | HP Econ: 8.53 | Venue Suppression: +1.40 | Wkt%: 10.2%)
3. **Jasprit Bumrah** (Score: 0.97 | HP Econ: 7.41 | Venue Suppression: +1.66 | Wkt%: 8.5%)
4. **Mitchell Santner** (Score: 0.89 | HP Econ: 7.46 | Venue Suppression: +1.86 | Consistency: 95.7%)
5. **Rashid Khan** (Score: 0.81 | HP Econ: 8.13 | Venue Suppression: +0.89 | Wkt%: 8.6%)
6. **Varun Chakravarthy** (Score: 0.79 | HP Econ: 8.26 | Venue Suppression: +0.95 | Consistency: 93.9%)
7. **Taskin Ahmed** (Score: 0.75 | HP Econ: 8.62 | Venue Suppression: +0.71 | Wkt%: 9.8%)
8. **Jamie Overton** (Score: 0.69 | HP Econ: 8.61 | Venue Suppression: +0.59 | Wkt%: 12.4%)
9. **Mitchell Starc** (Score: 0.68 | HP Econ: 10.15 | Wkt Rate: 16.1% — 1 wkt every 6.2 balls)
10. **Rasikh Salam** (Score: 0.66 | HP Econ: 9.12 | Venue Suppression: +0.72 | Wkt%: 11.6%)

---

### Deliverables Inside `rr-submission/v2/`
* [Mohammed_Aleem_Bukkapatnam_RR_SupeRR_Selector_Report_v2.pdf](file:///f:/Challenges/Rajasthan%20Royals/rr-submission/v2/Mohammed_Aleem_Bukkapatnam_RR_SupeRR_Selector_Report_v2.pdf)
* [dashboard/index.html](file:///f:/Challenges/Rajasthan%20Royals/rr-submission/v2/dashboard/index.html)
* [top10_batters_final.csv](file:///f:/Challenges/Rajasthan%20Royals/rr-submission/v2/top10_batters_final.csv)
* [top10_bowlers_final.csv](file:///f:/Challenges/Rajasthan%20Royals/rr-submission/v2/top10_bowlers_final.csv)

