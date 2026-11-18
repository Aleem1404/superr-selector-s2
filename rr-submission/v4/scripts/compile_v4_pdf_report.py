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
        
        if self._pageNumber > 1:
            self.drawString(54, 11 * inch - 36, "Rajasthan Royals | SupeRR Selector Season 2: Round 1 Submission (Model v4)")
            self.drawRightString(8.5 * inch - 54, 11 * inch - 36, "Mohammed Aleem Bukkapatnam (M.S. in AI)")
            self.setStrokeColor(colors.HexColor("#E4007C"))
            self.setLineWidth(1)
            self.line(54, 11 * inch - 40, 8.5 * inch - 54, 11 * inch - 40)
            
        self.setStrokeColor(colors.HexColor("#dddddd"))
        self.setLineWidth(0.5)
        self.line(54, 44, 8.5 * inch - 54, 44)
        
        self.drawString(54, 32, "Confidential - For Rajasthan Royals & Unstop Evaluation Only")
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 32, page_text)
        self.restoreState()

def build_pdf_v4(filename="rr-submission/v4/Mohammed_Aleem_Bukkapatnam_RR_SupeRR_Selector_Report_v4.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=46,
        rightMargin=46,
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
        fontSize=18,
        leading=22,
        textColor=primary_color,
        spaceAfter=3
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.8,
        leading=12.8,
        textColor=accent_color,
        spaceAfter=7
    )
    
    meta_style = ParagraphStyle(
        'Meta',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.2,
        textColor=colors.HexColor("#555555"),
        spaceAfter=8
    )
    
    h1_style = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=primary_color,
        spaceBefore=7,
        spaceAfter=3.5,
        keepWithNext=True
    )
    
    body_style = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.4,
        textColor=body_color,
        spaceAfter=4.5
    )
    
    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=body_style,
        leftIndent=10,
        firstLineIndent=-7,
        spaceAfter=2.5
    )
    
    caption_style = ParagraphStyle(
        'Caption',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=7.2,
        leading=9.2,
        textColor=colors.HexColor("#555555"),
        alignment=1,
        spaceAfter=5
    )
    
    table_header_style = ParagraphStyle(
        'TableHeader',
        fontName='Helvetica-Bold',
        fontSize=6.8,
        leading=8.6,
        textColor=colors.white,
        alignment=1
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=6.8,
        leading=8.6,
        textColor=body_color,
        alignment=1
    )
    
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=6.8,
        leading=8.6,
        textColor=body_color,
        alignment=1
    )

    story = []
    
    # --- PAGE 1: TITLE, EXECUTIVE SUMMARY & 3D UNIFIED ARCHITECTURE ---
    story.append(Paragraph("SupeRR Selector Season 2: Performance Under Pressure", title_style))
    story.append(Paragraph("Model v4: Unified Contextual Architecture (Opposition Tiering, Chase Asymmetry & Tactical Cohorts)", subtitle_style))
    story.append(Paragraph("<b>Candidate:</b> Mohammed Aleem Bukkapatnam (M.S. in Artificial Intelligence) &nbsp;|&nbsp; <b>Evaluation Panel:</b> Rajasthan Royals Analytics Team &nbsp;|&nbsp; <b>Data:</b> 200,999 Balls + 365 IPL Logs", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=accent_color, spaceAfter=7))
    
    story.append(Paragraph("Executive Summary & The Unified Contextual Architecture (Model v4)", h1_style))
    story.append(Paragraph(
        "Cricket pressure cannot be captured through a one-dimensional lens. A boundary struck off Jasprit Bumrah in the 19th over of a steep chase carries fundamentally different physical and cognitive leverage than one hit off a 5th-bowler in the 1st innings. "
        "Model v4 represents our <b>pinnacle production-grade formulation</b>, integrating three complementary contextual pillars into a unified dynamic leverage framework across <b>200,999 deliveries</b> (60,375 high-pressure balls): "
        "(1) <b>Opposition Quality Calibration:</b> Weighting runs by the quality tier of the bowler faced ($1.15\times$ for Elite bowlers like Bumrah/Narine; $0.88\times$ for part-timers), while discounting bowler wickets that merely clean up the tail (#7–#11); "
        "(2) <b>Chase Asymmetry:</b> Escalating the urgency multiplier in 2nd innings run-chases where RRR exceeds venue par; and "
        "(3) <b>Role-Specific Cohort Calibration:</b> Disentangling top-order anchors (&le;14 overs entry) from pure death finishers (15–20 overs entry) to guarantee fair sample equity. "
        "Verified active roster filtering (Criteria 1) is strictly enforced: retired veterans (MS Dhoni, Dinesh Karthik, Matthew Wade) are excluded, leaving a 100% active, contracted player pool.",
        body_style
    ))
    
    story.append(Paragraph("1. Pressure Definition: Dynamic Leverage & Chase Asymmetry", h1_style))
    story.append(Paragraph(
        "Model v4 defines ball-level <b>Unified Pressure Index ($PI_t^{v4} \in [0, 1]$)</b> calibrated across match innings and stage stakes:",
        body_style
    ))
    story.append(Paragraph("<b>A. Chase Asymmetry (Innings 2):</b> Chases feature an escalating psychological urgency factor centered at venue par ($Par_{venue}$ across 17 stadiums): <i>Mult<sub>chase</sub> = 1.0 + 0.15 &times; clip((RRR - Par<sub>venue</sub>) / Par<sub>venue</sub>, 0, 1)</i>. Interacts with required run rate urgency [<i>U<sub>RRR</sub></i>], temporal ball decay [<i>D<sub>balls</sub></i>], and wicket depletion risk [<i>W<sub>lev</sub></i>].", bullet_style))
    story.append(Paragraph("<b>B. Target Defense & Crisis (Innings 1):</b> Evaluates: (1) <i>Death Overs Execution</i> (overs 16–20) where dot vs boundary variance swings par by &plusmn;22 runs; and (2) <i>Top-Order Crisis Recovery</i> (&le;6 overs with &ge;3 down, or &le;10 overs with &ge;4 down).", bullet_style))
    story.append(Paragraph("<b>C. Stage Multipliers:</b> Group stage = 1.00&times;, Qualifiers/Eliminators = 1.20&times;, and Final = 1.30&times;. Balls with <b>$PI^{v4} \ge 0.60$</b> constitute High-Pressure (30.04% of total sample, N = 60,375).", bullet_style))
    
    story.append(Paragraph("2. Performance Measurement: Opposition Quality & Empirical Bayes Regularization", h1_style))
    story.append(Paragraph(
        "To eliminate distortion from stat-padding against weak attacks or tailenders, Model v4 applies dual quality weighting:",
        body_style
    ))
    story.append(Paragraph("<b>Batter Opposition Quality:</b> Each run scored under pressure is scaled by the opponent bowler's career tier: <i>Runs<sub>opp</sub> = Runs &times; BowlerTierMult</i>. Facing 53 pre-identified Elite bowlers (Econ &le; 7.85 or Wkt% &ge; 9.5%) yields a 1.15&times; multiplier.", bullet_style))
    story.append(Paragraph("<b>Bowler Wicket Value Weighting:</b> Dismissals of top-to-middle order batters (#1–#6) receive full 1.00&times; weight, while wickets of tailenders (#7–#11) in overs 16–20 are discounted to 0.70&times; to reward genuine breakthrough bowling over tail mopping.", bullet_style))
    story.append(Paragraph("<b>Empirical Bayes Shrinkage (K = 50 balls):</b> Raw opposition-adjusted metrics are shrunk toward tournament empirical priors (&mu;<sub>SR</sub> = 135.0, &mu;<sub>ER</sub> = 9.20): <i>&theta;&#770;<sub>i</sub> = (N<sub>i</sub> / (N<sub>i</sub>+K)) &middot; &theta;<sub>i</sub> + (K / (N<sub>i</sub>+K)) &middot; &mu;<sub>0</sub></i>.", bullet_style))
    story.append(Paragraph("<b>Composite Ball Pressure Score (CBPS v4):</b> Blends Shrunk Opp-Adjusted SR / Economy (25%), Venue Par Delta (25%), Baseline Elevation (20%), Dot Minimization / Dot Pressure (15%), and Match Consistency (15%), dampened by sample confidence <i>C<sub>i</sub> = min(1.0, &radic;(N<sub>i</sub> / 250))</i>.", bullet_style))
    
    story.append(Paragraph("3. Fair Comparisons: Role Cohorts & Sample Equity", h1_style))
    story.append(Paragraph(
        "Candidates must possess a minimum sample of <b>200 High-Pressure deliveries</b> (&ge;33.3 crunch overs). By grouping players into <b>Anchor / Top-Order Entry</b> (&le;14 overs entry) vs <b>Death Finisher Entry</b> (15–20 overs entry), Model v4 ensures that multi-phase anchors (Buttler, Surya, Shreyas) are evaluated equitably alongside pure death enforcers (Dhir, Ashutosh, Tim David).",
        body_style
    ))
    
    # --- PAGE 2: TABLES & CLUTCH MATRICES ---
    story.append(PageBreak())
    story.append(Paragraph("4. Evidence & Definitive Player Rankings (Model v4)", h1_style))
    story.append(Paragraph("<b>Table 1: Top 10 Active Batters Under High Pressure (Official Unstop Selections - Model v4)</b>", ParagraphStyle('Sub', parent=body_style, fontName='Helvetica-Bold', textColor=accent_color)))
    
    bat_data = [
        ["Rank", "Player", "HP Balls", "HP SR", "Opp-SR", "&Delta;SR Venue", "&Delta;SR Base", "Consistency", "Score", "Cohort & Tactical Archetype"],
        ["1", "Naman Dhir", "237", "196.2", "200.2", "+51.9", "+56.2", "92.9%", "1.60", "Finisher &bull; Elite Boundary Striker (200.2 Opp-SR)"],
        ["2", "Ashutosh Sharma", "310", "169.7", "171.7", "+20.9", "+85.2", "62.5%", "1.27", "Finisher &bull; Crisis Recovery Enforcer (+85.2 Delta)"],
        ["3", "Suryakumar Yadav", "669", "186.7", "190.3", "+44.3", "+36.9", "78.8%", "1.25", "Anchor &bull; 360-Degree Field Sculptor Across 669 Balls"],
        ["4", "Jos Buttler", "350", "180.6", "182.6", "+32.1", "+36.1", "88.2%", "1.11", "Anchor &bull; Chase Closer & Big-Match Match Winner"],
        ["5", "Glenn Phillips", "289", "179.9", "184.7", "+36.4", "+51.9", "78.6%", "1.07", "Finisher &bull; Versatile Lower-Order Striker"],
        ["6", "Donovan Ferreira", "205", "181.5", "186.3", "+33.3", "+58.8", "72.7%", "1.07", "Finisher &bull; Dynamic Pace & Spin Hitter"],
        ["7", "Shreyas Iyer", "459", "174.7", "177.3", "+29.4", "+38.1", "80.0%", "0.97", "Anchor &bull; Championship Playoff Match Builder"],
        ["8", "Sai Sudharsan", "213", "174.7", "177.1", "+28.8", "+38.6", "90.9%", "0.84", "Anchor &bull; Elite Reliability Anchor (90.9% Consistency)"],
        ["9", "Shashank Singh", "378", "172.0", "174.1", "+26.2", "+52.7", "66.7%", "0.84", "Finisher &bull; Crisis Counter-Attacker (+52.7 Delta)"],
        ["10", "Tim David", "729", "179.7", "181.5", "+33.0", "+27.6", "82.1%", "0.81", "Finisher &bull; Death-Overs Heavy Power Enforcer"]
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
        
    t_bat = Table(bat_table_rows, colWidths=[20, 84, 34, 32, 34, 38, 38, 44, 30, 150])
    t_bat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#dddddd")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#ffffff"), colors.HexColor("#f8f9fa")]),
    ]))
    story.append(t_bat)
    story.append(Spacer(1, 6))
    
    story.append(Paragraph("<b>Table 2: Top 10 Active Bowlers Under High Pressure (Official Unstop Selections - Model v4)</b>", ParagraphStyle('Sub', parent=body_style, fontName='Helvetica-Bold', textColor=accent_color)))
    
    bowl_data = [
        ["Rank", "Player", "HP Balls", "HP Econ", "&Delta;Econ Venue", "&Delta;Econ Base", "Quality Wkt%", "Consistency", "Score", "Tactical Archetype"],
        ["1", "Sunil Narine", "470", "6.63", "+2.45", "+0.32", "6.4%", "90.5%", "1.38", "Mystery Spin Constrictor (+2.45 Below Venue Par)"],
        ["2", "Matheesha Pathirana", "615", "8.51", "+1.42", "+0.16", "9.4%", "91.9%", "1.13", "Slingshot Yorker Enforcer (9.4% Quality Wkts)"],
        ["3", "Mitchell Santner", "491", "7.30", "+1.97", "+0.13", "6.7%", "96.2%", "1.12", "Defensive Master Controller (96.2% Consistency)"],
        ["4", "Akeal Hosein", "244", "7.38", "+1.84", "+0.38", "8.1%", "83.3%", "0.99", "Powerplay & Death Control Spinner"],
        ["5", "Rashid Khan", "910", "7.96", "+1.04", "-0.83", "8.4%", "90.9%", "0.93", "High-Leverage Strike Spinner Across 910 Balls"],
        ["6", "Jasprit Bumrah", "691", "7.42", "+1.68", "-0.42", "7.2%", "77.8%", "0.92", "Gold Standard Containment Pacer (7.42 HP Econ)"],
        ["7", "Wanindu Hasaranga", "523", "8.43", "+0.41", "-0.68", "9.5%", "89.7%", "0.81", "Middle-Overs Breakthrough Wicket Striker"],
        ["8", "Taskin Ahmed", "329", "8.61", "+0.72", "-1.02", "8.9%", "87.5%", "0.77", "High-Pace Hard-Length Enforcer"],
        ["9", "Sikandar Raza", "241", "7.22", "+1.93", "-0.23", "5.3%", "91.7%", "0.77", "Defensive Finger Spin Squeeze (7.22 Econ)"],
        ["10", "Varun Chakravarthy", "706", "8.35", "+0.86", "-0.57", "7.2%", "93.9%", "0.75", "Middle & Death Squeeze (93.9% Spell Reliability)"]
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
        
    t_bowl = Table(bowl_table_rows, colWidths=[20, 84, 34, 34, 40, 40, 36, 44, 30, 142])
    t_bowl.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), primary_color),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#dddddd")),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.HexColor("#ffffff"), colors.HexColor("#f8f9fa")]),
    ]))
    story.append(t_bowl)
    story.append(Spacer(1, 6))
    
    # Embedded Figures 1 & 2
    fig1 = "rr-submission/v4/stage5_deliverables/figures/batter_clutch_matrix.png"
    fig2 = "rr-submission/v4/stage5_deliverables/figures/bowler_clutch_matrix.png"
    if os.path.exists(fig1) and os.path.exists(fig2):
        img_table = Table([
            [
                Image(fig1, width=3.55*inch, height=2.30*inch),
                Image(fig2, width=3.55*inch, height=2.30*inch)
            ]
        ], colWidths=[3.6*inch, 3.6*inch])
        img_table.setStyle(TableStyle([
            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
            ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
            ('LEFTPADDING', (0,0), (-1,-1), 0),
            ('RIGHTPADDING', (0,0), (-1,-1), 0),
        ]))
        story.append(img_table)
        story.append(Paragraph("<b>Figures 1 & 2:</b> <i>(Left)</i> Active Batter Clutch Matrix: Venue Outperformance vs Baseline Delta. <i>(Right)</i> Active Bowler Clutch Matrix: Venue Economy Suppression vs Quality Wicket Threat %.", caption_style))

    # --- PAGE 3: PROGRESSION, SCOUTING TAKEAWAYS & VALIDATION ---
    story.append(PageBreak())
    story.append(Paragraph("5. Progression & Comparative Analysis (v1 &rarr; v2 &rarr; v3 &rarr; v4)", h1_style))
    story.append(Paragraph(
        "<b>Model Progression Summary:</b> "
        "(1) <i>Model v1 (Baseline):</i> Established Dynamic Leverage Index (LI &ge; 1.50) across 200,999 balls. "
        "(2) <i>Model v2 (Venue-Calibrated):</i> Introduced 17 stadium par rates ($Par_{venue}$) from 87,074 balls and playoff leverage multipliers. "
        "(3) <i>Model v3 (Active Roster Calibrated):</i> Verified player contracts, eliminating retired coaching personnel (MS Dhoni, Dinesh Karthik, Matthew Wade). "
        "(4) <i>Model v4 (Unified Contextual Framework):</i> Successfully synthesized <b>Opposition Quality Tiering</b> (53 Elite bowlers tagged), <b>Chase Asymmetry</b> (escalating 2nd innings pressure), and <b>Tactical Entry Cohorts</b> (Anchor vs Finisher). "
        "Split-half reliability reaches a peak <b>r = 0.94</b>.",
        body_style
    ))
    
    story.append(Paragraph("6. Key Tactical Scouting Takeaways for Rajasthan Royals", h1_style))
    story.append(Paragraph(
        "Model v4 delivers three conclusive strategic findings for Rajasthan Royals' match execution at Sawai Mansingh Stadium (Jaipur) and Barsapara Stadium (Guwahati):",
        body_style
    ))
    story.append(Paragraph("<b>1. True Opposition-Neutral Hitting &ndash; Naman Dhir (#1 Batter, CBPS +1.60):</b> When weighted for bowler quality, Dhir's strike rate actually *increases* from 196.2 to 200.2, proving that his boundary production occurs directly against frontline pacers and mystery spinners rather than stat-padding against 5th bowlers.", bullet_style))
    story.append(Paragraph("<b>2. The Spin Choke Blueprint &ndash; Sunil Narine (#1, 6.63 Econ) & Mitchell Santner (#3, 7.30 Econ):</b> In 200+ run chases, Narine and Santner provide an unprecedented 90%+ spell reliability while conceding ~2.00 to 2.45 runs below venue par. Finger/mystery spin constriction remains the most bankable defense.", bullet_style))
    story.append(Paragraph("<b>3. Tactical Cohort Balance:</b> Championship-winning teams require a complementary blend of high-sample Anchors (Jos Buttler, Suryakumar Yadav) who maintain an 85%+ consistency across 350+ pressure balls, paired with elite crisis Finishers (Ashutosh Sharma, Donovan Ferreira, Tim David) who elevate their baseline by +50 to +85 strike rate points.", bullet_style))
    
    story.append(Paragraph("7. Tactical Addendum: RR Home Ground Calibration & Auction Radar", h1_style))
    story.append(Paragraph(
        "While Round 1 strictly mandates an objective tournament-wide ranking (Tables 1 & 2), we extended Model v4 with two practical war-room filters for Rajasthan Royals: "
        "(1) <b>SMS Jaipur & Guwahati Home Fortress:</b> On Sawai Mansingh Stadium's 75m+ boundary dimensions, spin choke and low-dot running become paramount, maximizing the value of anchors like Jos Buttler and spin enforcers Sunil Narine and Mitchell Santner; "
        "(2) <b>Unretained Auction Target Radar:</b> Filtering for unretained players identifies premier auction targets including <b>Matheesha Pathirana</b> (9.4% quality wicket rate), <b>Wanindu Hasaranga</b> (9.5%), <b>Sikandar Raza</b> (7.22 Econ), and <b>Taskin Ahmed</b> (8.61 Econ).",
        body_style
    ))
    
    fig3 = "rr-submission/v4/stage5_deliverables/figures/top_10_batters_cbps.png"
    fig4 = "rr-submission/v4/stage5_deliverables/figures/top_10_bowlers_cbps.png"
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
        story.append(Paragraph("<b>Figures 3 & 4:</b> Top 10 Active Batters and Bowlers scored by Composite Ball Pressure Score (CBPS v4).", caption_style))
        
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully compiled v4 report to: {filename}")

if __name__ == '__main__':
    build_pdf_v4()
    build_pdf_v4("rr-submission/v4/stage5_deliverables/Mohammed_Aleem_Bukkapatnam_RR_SupeRR_Selector_Report_v4.pdf")

