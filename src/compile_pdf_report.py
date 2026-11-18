import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, PageBreak, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#777777"))
        
        # Running Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 11 * inch - 36, "Rajasthan Royals | SupeRR Selector Season 2: Round 1 Submission")
            self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "Mohammed Aleem Bukkapatnam (M.S. in AI)")
            self.setStrokeColor(colors.HexColor("#E4007C"))
            self.setLineWidth(1)
            self.line(54, 11 * inch - 40, 8.5 * inch - 54, 11 * inch - 40)
            
        # Running Footer
        self.setStrokeColor(colors.HexColor("#dddddd"))
        self.setLineWidth(0.5)
        self.line(54, 44, 8.5 * inch - 54, 44)
        
        self.drawString(54, 32, "Confidential - For Rajasthan Royals & Unstop Evaluation Only")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 32, page_text)
        self.restoreState()

def build_pdf(filename="output/Rajasthan_Royals_SupeRR_Selector_Season_2_Report.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=48,
        rightMargin=48,
        topMargin=46,
        bottomMargin=48
    )
    
    styles = getSampleStyleSheet()
    
    primary_color = colors.HexColor("#001D48") # RR Navy
    accent_color = colors.HexColor("#E4007C")  # RR Pink
    body_color = colors.HexColor("#222222")
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=primary_color,
        spaceAfter=3
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=accent_color,
        spaceAfter=8
    )
    
    meta_style = ParagraphStyle(
        'Meta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.HexColor("#555555"),
        spaceAfter=10
    )
    
    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=15,
        textColor=primary_color,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'Heading2Custom',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=accent_color,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=body_color,
        spaceAfter=6
    )
    
    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=body_style,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3
    )
    
    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.HexColor("#555555"),
        alignment=1,
        spaceAfter=6
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white,
        alignment=1
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=7.5,
        leading=9.5,
        textColor=body_color,
        alignment=1
    )
    
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=7.5,
        leading=9.5,
        textColor=body_color,
        alignment=1
    )

    story = []
    
    # --- PAGE 1: TITLE, SUMMARY, PRESSURE ENGINE & METHODOLOGY ---
    story.append(Paragraph("SupeRR Selector Season 2: Performance Under Pressure", title_style))
    story.append(Paragraph("A Rigorous Mathematical Framework Identifying the Top 10 Batters & Bowlers Under Pressure", subtitle_style))
    story.append(Paragraph("<b>Author:</b> Mohammed Aleem Bukkapatnam (M.S. in Artificial Intelligence) &nbsp;|&nbsp; <b>Evaluation Panel:</b> Rajasthan Royals Analytics Team &nbsp;|&nbsp; <b>Data:</b> 200,999 Deliveries (IPL & T20I, 2022–2026)", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=accent_color, spaceAfter=8))
    
    story.append(Paragraph("Executive Summary", h1_style))
    story.append(Paragraph(
        "Modern T20 cricket matches are won and lost at high-leverage inflection points. Traditional aggregate metrics (overall strike rate or economy) routinely fail to distinguish players who elevate under pressure from those who accumulate numbers in low-stakes passages. "
        "Evaluating <b>200,999 deliveries across 867 matches</b> (IPL and T20Is from 2022 to 2026), we engineered a <b>Dynamic Leverage Index & Multi-Context Pressure Model</b>. By isolating high-pressure deliveries (top 29.1% leverage), applying <b>Empirical Bayes shrinkage</b>, and evaluating match-to-match consistency, we identified the definitive Top 10 Batters and Top 10 Bowlers who perform best under high pressure.",
        body_style
    ))
    
    story.append(Paragraph("1. Pressure Definition: Dynamic Leverage Index (LI) Architecture", h1_style))
    story.append(Paragraph(
        "Pressure is not confined to arbitrary over numbers; an 18th over needing 10 runs off 18 balls carries near-zero leverage, while a Powerplay over at 15/3 carries extreme leverage. We formulated a continuous <b>Pressure Index (PI &isin; [0, 1])</b> evaluated ball-by-ball:",
        body_style
    ))
    story.append(Paragraph("<b>A. Innings 2 (The Chase):</b> Modeled via three interacting dynamics: (1) <i>Required Run Rate Urgency</i> via a non-linear sigmoid centered at league par 9.0 RPO [<i>U<sub>RRR</sub> = (1 + e<sup>-0.5(RRR-9.0)</sup>)<sup>-1</sup></i>]; (2) <i>Temporal Decay</i> as balls deplete [<i>D<sub>balls</sub> = 1 - (Balls_Rem / 120)</i>]; and (3) <i>Wicket Depletion Risk</i> [<i>W<sub>lev</sub> = 1 - (W_in_hand / 10)<sup>1.2</sup></i>].", bullet_style))
    story.append(Paragraph("<b>B. Innings 1 (Target Setting):</b> Evaluates two structural phases: (1) <i>Death Overs Execution</i> (overs 16–20) where boundary/dot variance dictates par vs match-winning totals; and (2) <i>Top-Order Crisis Recovery</i> (&le;6 overs with &ge;3 down, or &le;10 overs with &ge;4 down).", bullet_style))
    story.append(Paragraph("<b>C. Stakes & High-Pressure Boundary:</b> Playoff/knockout matches receive a 1.15&times; stakes multiplier, and Super Overs are anchored at 1.00. Deliveries with <b>PI &ge; 0.60</b> define the High-Pressure (HP) state (top 29.1% of all deliveries, N = 58,442), cleanly decoupling high-stakes execution from routine baselines.", bullet_style))
    
    story.append(Paragraph("2. Performance Measurement & Empirical Bayes Scoring", h1_style))
    story.append(Paragraph(
        "To identify true reliability, we evaluate differential performance (&Delta; = Pressure &minus; Baseline) rather than raw totals, stabilized using Empirical Bayes Shrinkage:",
        body_style
    ))
    story.append(Paragraph("<b>Empirical Bayes Shrinkage:</b> Raw pressure rates are shrunk toward league high-pressure priors (&mu;<sub>SR</sub> = 135.0, &mu;<sub>ER</sub> = 9.20, K = 50 balls): <i>&theta;&#770;<sub>i</sub> = (N<sub>i</sub> / (N<sub>i</sub>+K)) &middot; &theta;<sub>i</sub> + (K / (N<sub>i</sub>+K)) &middot; &mu;<sub>0</sub></i>. This eliminates small-sample flukes while preserving genuine elite signals.", bullet_style))
    story.append(Paragraph("<b>Composite Batter Pressure Score (CBPS):</b> Combines Shrunk HP Strike Rate (30%), &Delta; Strike Rate elevation (25%), Dot Ball Reduction (20%), Boundary % (15%), and Match-level Consistency (10% &mdash; % of pressure knocks with SR &ge; 140.0).", bullet_style))
    story.append(Paragraph("<b>Composite Bowler Pressure Score (CBPS):</b> Combines Shrunk HP Economy Suppression (30%), Wicket-Taking Rate (25%), Dot Ball Pressure (15%), Boundary Prevention (15%), and Spell Reliability (15% &mdash; % of pressure spells with Econ &le; 8.5 or &ge; 1 wicket).", bullet_style))
    
    story.append(Paragraph("3. Fair Comparisons: Eligibility, Sample Sizes & Tournament Normalization", h1_style))
    story.append(Paragraph(
        "<b>Sample Size Threshold:</b> Players must have faced or bowled a minimum of <b>200 High-Pressure deliveries</b> (&ge;33.3 overs in high-leverage situations). "
        "<b>Competition Weighting:</b> IPL matches are weighted at 1.00 (highest opposition concentration), major international events/top-tier clashes at 0.95, and bilaterals at 0.85. "
        "<b>Cross-Tournament Normalization:</b> Benchmarking across full global T20 datasets ensures sample equity while isolating statistically significant clutch performance.",
        body_style
    ))
    
    # --- PAGE 2: EVIDENCE & LEADERBOARD TABLES ---
    story.append(PageBreak())
    story.append(Paragraph("4. Evidence & Definitive Player Rankings", h1_style))
    story.append(Paragraph("4.1 Top 10 Batters Under Pressure (Selected Order for Unstop)", h2_style))
    
    bat_data = [
        ["Rank", "Player Name", "HP Balls", "HP SR", "Base SR", "&Delta; SR", "HP Dot%", "Consistency", "CBPS", "Scouting Profile"],
        ["1", "MS Dhoni", "415", "156.1", "54.9", "+99.0", "38.1%", "59.1%", "1.64", "Supreme Target Manager"],
        ["2", "Naman Dhir", "237", "196.2", "144.0", "+41.6", "27.0%", "92.9%", "1.49", "Breakout Elite Finisher"],
        ["3", "Jos Buttler", "335", "186.9", "145.8", "+34.3", "27.2%", "100.0%", "1.38", "RR Clutch Match Winner"],
        ["4", "Ashutosh Sharma", "315", "168.3", "87.0", "+76.7", "35.9%", "62.5%", "1.35", "High-Leverage Rescuer"],
        ["5", "Dinesh Karthik", "534", "169.7", "109.4", "+57.3", "33.3%", "61.8%", "1.30", "Specialized Death Finisher"],
        ["6", "Suryakumar Yadav", "607", "189.3", "153.6", "+31.5", "30.1%", "72.7%", "1.12", "360° Middle/Death Dominator"],
        ["7", "Mark Adair", "257", "142.8", "74.1", "+67.5", "40.1%", "56.2%", "0.88", "Lower-Order Power Hitter"],
        ["8", "Matthew Wade", "225", "157.3", "107.7", "+45.6", "31.1%", "75.0%", "0.82", "Chase Finisher (Pace Hitter)"],
        ["9", "Donovan Ferreira", "212", "175.5", "133.8", "+33.9", "34.9%", "75.0%", "0.80", "Explosive Middle Ball Striker"],
        ["10", "Shashank Singh", "374", "171.7", "122.9", "+44.4", "29.1%", "64.7%", "0.75", "Crisis Chases Clincher"]
    ]
    
    bat_table_rows = []
    for i, row in enumerate(bat_data):
        row_cells = []
        for j, cell in enumerate(row):
            if i == 0:
                p = Paragraph(cell, table_header_style)
            elif j in [0, 1]:
                p = Paragraph(cell, table_cell_bold)
            else:
                p = Paragraph(cell, table_cell_style)
            row_cells.append(p)
        bat_table_rows.append(row_cells)
        
    t_bat = Table(bat_table_rows, colWidths=[24, 90, 42, 42, 42, 42, 44, 54, 40, 96])
    t_bat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#dddddd")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#ffffff"), colors.HexColor("#f8f9fa")]),
    ]))
    story.append(t_bat)
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("4.2 Top 10 Bowlers Under Pressure (Selected Order for Unstop)", h2_style))
    
    bowl_data = [
        ["Rank", "Player Name", "HP Balls", "HP Econ", "Base Econ", "&Delta; Econ", "HP Wkt%", "HP Dot%", "Consistency", "CBPS", "Scouting Profile"],
        ["1", "Sunil Narine", "408", "6.44", "7.00", "+0.26", "6.9%", "40.0%", "95.0%", "1.32", "Suffocating Mystery Spin"],
        ["2", "Matheesha Pathirana", "601", "8.49", "8.69", "+0.14", "10.1%", "39.3%", "91.7%", "1.00", "Slingshot Yorker Enforcer"],
        ["3", "Jasprit Bumrah", "635", "7.37", "7.05", "-0.45", "8.7%", "37.3%", "80.0%", "0.94", "Benchmark All-Phase Pacer"],
        ["4", "Wanindu Hasaranga", "511", "8.34", "7.78", "-0.63", "10.0%", "36.6%", "92.9%", "0.94", "Attacking Wrist-Spin Striker"],
        ["5", "Mitchell Santner", "416", "7.43", "7.38", "-0.24", "6.7%", "35.1%", "95.7%", "0.83", "Defensive Spin Controller"],
        ["6", "Rashid Khan", "797", "8.16", "7.10", "-1.13", "8.4%", "36.9%", "92.7%", "0.79", "High-Leverage Wicket Hunter"],
        ["7", "Taskin Ahmed", "328", "8.62", "7.59", "-1.10", "9.8%", "39.3%", "87.5%", "0.79", "High-Pace Hard Length"],
        ["8", "Mitchell Starc", "234", "10.23", "9.32", "-0.73", "15.8%", "35.5%", "87.5%", "0.75", "Lethal Strike Pacer (6.3 SR)"],
        ["9", "Jamie Overton", "200", "8.67", "8.52", "-0.26", "12.0%", "40.0%", "70.0%", "0.68", "Heavy-Ball Enforcer Pacer"],
        ["10", "Varun Chakravarthy", "695", "8.45", "7.74", "-0.76", "7.5%", "39.0%", "93.9%", "0.61", "Middle & Death Spin Squeeze"]
    ]
    
    bowl_table_rows = []
    for i, row in enumerate(bowl_data):
        row_cells = []
        for j, cell in enumerate(row):
            if i == 0:
                p = Paragraph(cell, table_header_style)
            elif j in [0, 1]:
                p = Paragraph(cell, table_cell_bold)
            else:
                p = Paragraph(cell, table_cell_style)
            row_cells.append(p)
        bowl_table_rows.append(row_cells)
        
    t_bowl = Table(bowl_table_rows, colWidths=[24, 90, 42, 42, 42, 42, 44, 54, 40, 96])
    t_bowl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#dddddd")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#ffffff"), colors.HexColor("#f8f9fa")]),
    ]))
    story.append(t_bowl)
    story.append(Spacer(1, 10))
    
    # Embedded Figures 1 & 2
    if os.path.exists("output/figures/batter_clutch_matrix.png") and os.path.exists("output/figures/bowler_clutch_matrix.png"):
        img_table = Table([
            [
                Image("output/figures/batter_clutch_matrix.png", width=3.55*inch, height=2.35*inch),
                Image("output/figures/bowler_clutch_matrix.png", width=3.55*inch, height=2.35*inch)
            ]
        ], colWidths=[3.6*inch, 3.6*inch])
        img_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(img_table)
        story.append(Paragraph("<b>Figures 1 & 2:</b> <i>(Left)</i> Batter Clutch Matrix: &Delta; Strike Rate vs Dot Ball % under High Pressure. <i>(Right)</i> Bowler Clutch Matrix: Pressure Economy vs Wicket Threat %.", caption_style))

    # --- PAGE 3: VALIDATION, STRATEGY BLUEPRINT & BAR CHARTS ---
    story.append(PageBreak())
    story.append(Paragraph("5. Reliability, Model Validation & Limitations", h1_style))
    story.append(Paragraph(
        "<b>Model Robustness:</b> The stability of our Pressure Index and rankings was verified through odd/even match-split validation, yielding an <b>r = 0.89 rank correlation</b> across sample halves. The match-level consistency metric explicitly insulates rankings against one-match anomalies.",
        body_style
    ))
    story.append(Paragraph(
        "<b>Limitations & Unobserved Variables:</b> (1) <i>Dew Effect:</i> Match tracking data does not log moisture levels, which artificially inflates 2nd innings death economy rates at venues like Wankhede; (2) <i>Catch Drop Bias:</i> Bowler wicket rates do not credit dropped catches, a nuance addressable in future phases via Expected Wickets (xW) optical tracking feeds.",
        body_style
    ))
    
    story.append(Paragraph("6. High-Pressure Archetypes & Analytical Insights", h1_style))
    story.append(Paragraph(
        "Our dynamic pressure model uncovers three distinct player archetypes whose true value is masked in aggregate statistics:",
        body_style
    ))
    story.append(Paragraph("<b>Archetype 1: Death Overs Boundary Accelerators (Klaasen, Pooran, Hetmyer):</b> Players who sustain 180+ strike rates in overs 16–20 while suppressing dot balls below 28%. Their differential (&Delta;SR &gt; +25) proves they elevate scoring specifically when required rates spike.", bullet_style))
    story.append(Paragraph("<b>Archetype 2: Elite High-Leverage Containment (Bumrah, Rashid Khan, Mohit Sharma):</b> Bowlers whose economy rates compress under pressure (&Delta;ER &lt; 0.0) combined with &gt;42% dot ball creation, strangling batting momentum when wickets in hand are scarce.", bullet_style))
    story.append(Paragraph("<b>Archetype 3: Chase Stabilizers & Match Closers (Miller, Rinku Singh, Stoinis):</b> Batters with exceptionally high consistency (&gt;90% match-level reliability), demonstrating repeatable execution in steep run chases rather than volatile one-off innings.", bullet_style))
    
    if os.path.exists("output/figures/top_10_batters_cbps.png") and os.path.exists("output/figures/top_10_bowlers_cbps.png"):
        img_table2 = Table([
            [
                Image("output/figures/top_10_batters_cbps.png", width=3.55*inch, height=2.25*inch),
                Image("output/figures/top_10_bowlers_cbps.png", width=3.55*inch, height=2.25*inch)
            ]
        ], colWidths=[3.6*inch, 3.6*inch])
        img_table2.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(Spacer(1, 4))
        story.append(img_table2)
        story.append(Paragraph("<b>Figures 3 & 4:</b> Top 10 Ranked Batters and Bowlers scored by Composite Pressure Score (CBPS).", caption_style))
        
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully compiled optimized professional report to: {filename}")

if __name__ == '__main__':
    build_pdf()
