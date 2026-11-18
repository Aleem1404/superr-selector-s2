import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, HRFlowable, PageBreak
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
            self.drawString(54, 11 * inch - 36, "Rajasthan Royals | SupeRR Selector Season 2: Round 1 Submission (Model v2)")
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

def build_pdf_v2(filename="rr-submission/v2/Mohammed_Aleem_Bukkapatnam_RR_SupeRR_Selector_Report_v2.pdf"):
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
        fontSize=19,
        leading=23,
        textColor=primary_color,
        spaceAfter=3
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10.5,
        leading=13.5,
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
        fontSize=11.5,
        leading=14.5,
        textColor=primary_color,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.8,
        textColor=body_color,
        spaceAfter=5
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
        fontSize=7.2,
        leading=9.0,
        textColor=colors.white,
        alignment=1
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.0,
        textColor=body_color,
        alignment=1
    )
    
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.0,
        textColor=body_color,
        alignment=1
    )

    story = []
    
    # --- PAGE 1: TITLE, SUMMARY, PRESSURE ENGINE & METHODOLOGY ---
    story.append(Paragraph("SupeRR Selector Season 2: Performance Under Pressure", title_style))
    story.append(Paragraph("Model v2: Venue Pitch Par Calibrated & Multi-Stage Leverage Framework", subtitle_style))
    story.append(Paragraph("<b>Candidate:</b> Mohammed Aleem Bukkapatnam (M.S. in Artificial Intelligence) &nbsp;|&nbsp; <b>Evaluation Panel:</b> Rajasthan Royals Analytics Team &nbsp;|&nbsp; <b>Data:</b> 200,999 Balls + 365 IPL Match Metadata", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=accent_color, spaceAfter=8))
    
    story.append(Paragraph("Executive Summary (v2 Framework)", h1_style))
    story.append(Paragraph(
        "Modern T20 cricket matches are won and lost at high-leverage inflection points. In Model v2, we advanced beyond static league averages by integrating <b>venue-specific scoring pars ($Par_{venue}$)</b> and <b>playoff-specific leverage stages</b> derived from 5 complete seasons of delivery logs. "
        "Evaluating <b>200,999 deliveries across 867 matches</b> (with 87,687 pure IPL balls mapped to exact stadium pitch rates), we decoupled routine stat-padding from true high-leverage execution. Stabilized through Empirical Bayes shrinkage ($K=50$ balls) and match-level reliability scoring, Model v2 delivers the definitive Top 10 Batters and Top 10 Bowlers under pressure.",
        body_style
    ))
    
    story.append(Paragraph("1. Pressure Definition (v2): Dynamic Leverage & Stadium Pitch Par", h1_style))
    story.append(Paragraph(
        "Scoring 14 off 6 balls at Sawai Mansingh Stadium, Jaipur ($Par_{venue} = 9.36$) carries vastly higher leverage than at Chinnaswamy or Kolkata ($Par_{venue} \ge 9.36$). Conversely, an 8.5 economy at Kolkata is elite, while at Chennai ($Par = 8.27$) it is sub-par. We formulate ball-level <b>Pressure Index ($PI_t \in [0, 1]$)</b> calibrated for pitch conditions:",
        body_style
    ))
    story.append(Paragraph("<b>A. Innings 2 (The Chase):</b> Modeled via three interacting dynamics: (1) <i>Required Run Rate Urgency</i> centered at dynamic stadium par [<i>U<sub>RRR</sub> = (1 + e<sup>-0.5(RRR - Par_venue)</sup>)<sup>-1</sup></i>]; (2) <i>Temporal Decay</i> [<i>D<sub>balls</sub> = 1 - (Balls_Rem / 120)</i>]; and (3) <i>Wicket Depletion Risk</i> [<i>W<sub>lev</sub> = 1 - (W_in_hand / 10)<sup>1.2</sup></i>].", bullet_style))
    story.append(Paragraph("<b>B. Innings 1 (Target Setting):</b> Evaluates two structural phases: (1) <i>Death Overs Execution</i> (overs 16–20) where boundary/dot variance dictates par vs match-winning totals; and (2) <i>Top-Order Crisis Recovery</i> (&le;6 overs with &ge;3 down, or &le;10 overs with &ge;4 down).", bullet_style))
    story.append(Paragraph("<b>C. Stage & Championship Leverage Multipliers:</b> Group stage matches = 1.00&times;, Qualifiers/Eliminators = 1.20&times;, IPL Final = 1.30&times;, and Super Overs = 1.00. Deliveries with <b>PI &ge; 0.60</b> define the High-Pressure (HP) state (top 28.92% of all deliveries, N = 58,125).", bullet_style))
    
    story.append(Paragraph("2. Performance Measurement & Empirical Bayes Scoring", h1_style))
    story.append(Paragraph(
        "To identify true reliability, we evaluate differential performance against both baseline and venue par, stabilized using Empirical Bayes Shrinkage:",
        body_style
    ))
    story.append(Paragraph("<b>Empirical Bayes Shrinkage:</b> Raw pressure rates are shrunk toward tournament high-pressure priors (&mu;<sub>SR</sub> = 135.0, &mu;<sub>ER</sub> = 9.20, K = 50 balls): <i>&theta;&#770;<sub>i</sub> = (N<sub>i</sub> / (N<sub>i</sub>+K)) &middot; &theta;<sub>i</sub> + (K / (N<sub>i</sub>+K)) &middot; &mu;<sub>0</sub></i>.", bullet_style))
    story.append(Paragraph("<b>Composite Batter Pressure Score (CBPS v2):</b> Combines Shrunk HP Strike Rate (25%), Venue-Adjusted Elevation &Delta;SR<sub>venue</sub> (25%), Baseline Elevation &Delta;SR<sub>base</sub> (20%), Dot Ball Reduction (15%), and Match-level Consistency (15% &mdash; % of pressure knocks with SR &ge; 140.0).", bullet_style))
    story.append(Paragraph("<b>Composite Bowler Pressure Score (CBPS v2):</b> Combines Shrunk HP Economy (25%), Venue Run Suppression &Delta;Econ<sub>venue</sub> (25%), Wicket-Taking Threat (20%), Dot Ball Pressure (15%), and Spell Reliability (15% &mdash; % of pressure spells with Econ &le; 8.5 or &ge; 1 wicket).", bullet_style))
    
    story.append(Paragraph("3. Fair Comparisons: Eligibility, Sample Sizes & Tournament Normalization", h1_style))
    story.append(Paragraph(
        "<b>Sample Size Threshold:</b> Players must have faced or bowled a minimum of <b>200 High-Pressure deliveries</b> (&ge;33.3 overs in high-leverage situations). "
        "<b>Competition Weighting:</b> IPL matches are weighted at 1.15&times; (highest opposition concentration) relative to bilateral internationals, eliminating distortion from lower-tier international opponents.",
        body_style
    ))
    
    # --- PAGE 2: EVIDENCE & LEADERBOARD TABLES ---
    story.append(PageBreak())
    story.append(Paragraph("4. Evidence & Definitive Player Rankings (v2)", h1_style))
    story.append(Paragraph("<b>Table 1: Top 10 Batters Under High Pressure (Official Unstop Selections - Model v2)</b>", ParagraphStyle('Sub', parent=body_style, fontName='Helvetica-Bold', textColor=accent_color)))
    
    bat_data = [
        ["Rank", "Player", "HP Balls", "HP SR", "&Delta;SR Venue", "&Delta;SR Base", "HP Dot%", "Consistency", "Score", "Tactical Archetype"],
        ["1", "Naman Dhir", "235", "194.9", "+46.6", "+49.8", "27.2%", "92.9%", "1.48", "High-Impact Boundary Hunter / Finisher"],
        ["2", "Ashutosh Sharma", "307", "171.0", "+20.3", "+87.1", "34.9%", "62.5%", "1.38", "Crisis Rescue Specialist"],
        ["3", "Jos Buttler", "319", "185.0", "+34.5", "+38.6", "27.0%", "100.0%", "1.36", "100% Chase Closer / Match Winner"],
        ["4", "MS Dhoni", "412", "156.8", "+13.1", "+101.5", "38.1%", "59.1%", "1.32", "Clutch Anchor & Target Finisher"],
        ["5", "Suryakumar Yadav", "609", "188.8", "+43.1", "+35.1", "30.2%", "77.4%", "1.26", "360-Degree Field Manipulator"],
        ["6", "Dinesh Karthik", "533", "170.0", "+21.8", "+61.3", "33.2%", "61.8%", "1.15", "Elite Death Overs Finisher"],
        ["7", "Shreyas Iyer", "420", "177.6", "+29.6", "+38.4", "26.2%", "80.0%", "1.00", "Playoff Captain & Match Anchor"],
        ["8", "Glenn Phillips", "255", "179.2", "+30.9", "+44.4", "29.0%", "78.6%", "0.90", "Dynamic Lower-Order Striker"],
        ["9", "Dhruv Jurel", "325", "171.1", "+21.1", "+40.6", "28.3%", "83.3%", "0.89", "Rajasthan Royals Clutch Finisher"],
        ["10", "Matthew Wade", "223", "158.7", "+11.3", "+52.0", "30.5%", "75.0%", "0.84", "Pressure Ramp / Pace Destroyer"]
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
        
    t_bat = Table(bat_table_rows, colWidths=[24, 88, 38, 38, 44, 44, 40, 52, 36, 112])
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
    
    story.append(Paragraph("<b>Table 2: Top 10 Bowlers Under High Pressure (Official Unstop Selections - Model v2)</b>", ParagraphStyle('Sub', parent=body_style, fontName='Helvetica-Bold', textColor=accent_color)))
    
    bowl_data = [
        ["Rank", "Player", "HP Balls", "HP Econ", "&Delta;Econ Venue", "&Delta;Econ Base", "Wkt%", "Consistency", "Score", "Tactical Archetype"],
        ["1", "Sunil Narine", "393", "6.20", "+2.90", "+0.88", "6.9%", "95.2%", "1.61", "Suffocating Mystery Spin Constrictor"],
        ["2", "Matheesha Pathirana", "611", "8.53", "+1.40", "+0.10", "10.2%", "91.9%", "1.08", "Slingshot Yorker Enforcer"],
        ["3", "Jasprit Bumrah", "646", "7.41", "+1.66", "-0.39", "8.5%", "78.0%", "0.97", "Benchmark All-Phase Executioner"],
        ["4", "Mitchell Santner", "418", "7.46", "+1.86", "-0.09", "6.5%", "95.7%", "0.89", "Defensive Match Controller"],
        ["5", "Rashid Khan", "800", "8.13", "+0.89", "-1.02", "8.6%", "92.9%", "0.81", "High-Leverage Partnership Breaker"],
        ["6", "Varun Chakravarthy", "674", "8.26", "+0.95", "-0.42", "7.7%", "93.9%", "0.79", "Middle & Death Spin Squeeze"],
        ["7", "Taskin Ahmed", "328", "8.62", "+0.71", "-1.03", "9.8%", "87.5%", "0.75", "High-Pace Hard-Length Enforcer"],
        ["8", "Jamie Overton", "202", "8.61", "+0.59", "-0.06", "12.4%", "70.0%", "0.69", "Heavy-Ball Hit-the-Deck Pacer"],
        ["9", "Mitchell Starc", "224", "10.15", "-0.49", "-0.78", "16.1%", "87.5%", "0.68", "Elite Strike Weapon (Wkt/6.2 balls)"],
        ["10", "Rasikh Salam", "250", "9.12", "+0.72", "+0.85", "11.6%", "85.7%", "0.66", "Emerging Death Bowling Striker"]
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
        
    t_bowl = Table(bowl_table_rows, colWidths=[24, 86, 36, 38, 44, 44, 36, 52, 34, 122])
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
    fig1 = "rr-submission/v2/stage5_deliverables/figures/batter_clutch_matrix.png"
    fig2 = "rr-submission/v2/stage5_deliverables/figures/bowler_clutch_matrix.png"
    if os.path.exists(fig1) and os.path.exists(fig2):
        img_table = Table([
            [
                Image(fig1, width=3.55*inch, height=2.35*inch),
                Image(fig2, width=3.55*inch, height=2.35*inch)
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

    # --- PAGE 3: VALIDATION, INSIGHTS & COMPARATIVE ANALYSIS ---
    story.append(PageBreak())
    story.append(Paragraph("5. Reliability, Model Validation & Comparative Insights (v1 vs v2)", h1_style))
    story.append(Paragraph(
        "<b>Model Robustness & Calibration:</b> By introducing stadium pitch par rates, Model v2 improves split-half stability to <b>r = 0.91</b>. The venue delta explicitly credits players whose pressure numbers were delivered on high-scoring tracks (e.g. Chinnaswamy, Wankhede) versus spin tracks (Chepauk).",
        body_style
    ))
    story.append(Paragraph(
        "<b>Limitations & Unobserved Variables:</b> (1) <i>Dew Effect:</i> Match tracking data does not log moisture levels, which artificially inflates 2nd innings death economy rates at venues like Wankhede; (2) <i>Catch Drop Bias:</i> Bowler wicket rates do not credit dropped catches, a nuance addressable in future phases via Expected Wickets (xW) optical tracking feeds.",
        body_style
    ))
    
    story.append(Paragraph("6. Key Scouting Takeaways for Rajasthan Royals", h1_style))
    story.append(Paragraph(
        "Our venue-calibrated model surfaces three critical performance archetypes directly relevant to Rajasthan Royals' home ground dynamics at Sawai Mansingh Stadium (Jaipur) and Barsapara Stadium (Guwahati):",
        body_style
    ))
    story.append(Paragraph("<b>1. Elite Spin Suffocation (Sunil Narine & Varun Chakravarthy):</b> Narine concedes 2.90 runs below venue par under pressure with 40% dot balls. Conceding sub-6.5 RPO in overs 14–20 provides unprecedented tactical squeeze.", bullet_style))
    story.append(Paragraph("<b>2. Pure Yorkers & Slingshot Execution (Matheesha Pathirana & Jasprit Bumrah):</b> Pathirana strikes at 10.2% while Bumrah limits high-leverage scoring to 7.41 RPO. Pairing lead pacers with high-consistency death specialists produces the highest championship win-shares.", bullet_style))
    story.append(Paragraph("<b>3. Low-Dot Clutch Anchors (Jos Buttler, Naman Dhir & Dhruv Jurel):</b> Buttler's 100% consistency across pressure chases and Dhir's 194.9 strike rate prove that boundary frequency combined with sub-28% dot ball rates is the primary differentiator in 200+ run chases.", bullet_style))
    
    fig3 = "rr-submission/v2/stage5_deliverables/figures/top_10_batters_cbps.png"
    fig4 = "rr-submission/v2/stage5_deliverables/figures/top_10_bowlers_cbps.png"
    if os.path.exists(fig3) and os.path.exists(fig4):
        img_table2 = Table([
            [
                Image(fig3, width=3.55*inch, height=2.25*inch),
                Image(fig4, width=3.55*inch, height=2.25*inch)
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
        story.append(Paragraph("<b>Figures 3 & 4:</b> Top 10 Ranked Batters and Bowlers scored by Composite Pressure Score (CBPS v2).", caption_style))
        
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully compiled v2 report to: {filename}")

if __name__ == '__main__':
    build_pdf_v2()
    build_pdf_v2("rr-submission/v2/stage5_deliverables/Mohammed_Aleem_Bukkapatnam_RR_SupeRR_Selector_Report_v2.pdf")

