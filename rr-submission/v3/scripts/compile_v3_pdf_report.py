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
            self.drawString(54, 11 * inch - 36, "Rajasthan Royals | SupeRR Selector Season 2: Round 1 Submission (Model v3)")
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

def build_pdf_v3(filename="rr-submission/v3/Mohammed_Aleem_Bukkapatnam_RR_SupeRR_Selector_Report_v3.pdf"):
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
        fontSize=10,
        leading=13,
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
        fontSize=7.0,
        leading=8.8,
        textColor=colors.white,
        alignment=1
    )
    
    table_cell_style = ParagraphStyle(
        'TableCell',
        fontName='Helvetica',
        fontSize=7.0,
        leading=8.8,
        textColor=body_color,
        alignment=1
    )
    
    table_cell_bold = ParagraphStyle(
        'TableCellBold',
        fontName='Helvetica-Bold',
        fontSize=7.0,
        leading=8.8,
        textColor=body_color,
        alignment=1
    )

    story = []
    
    # --- PAGE 1: TITLE, EXECUTIVE SUMMARY & DUAL-PILLAR METHODOLOGY ---
    story.append(Paragraph("SupeRR Selector Season 2: Performance Under Pressure", title_style))
    story.append(Paragraph("Model v3: Active Roster Verified, Venue Par Calibrated & Multi-Stage Leverage Framework", subtitle_style))
    story.append(Paragraph("<b>Candidate:</b> Mohammed Aleem Bukkapatnam (M.S. in Artificial Intelligence) &nbsp;|&nbsp; <b>Evaluation Panel:</b> Rajasthan Royals Analytics Team &nbsp;|&nbsp; <b>Data:</b> 200,999 Balls + 365 IPL Logs", meta_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=accent_color, spaceAfter=7))
    
    story.append(Paragraph("Executive Summary & Core Directives (Model v3)", h1_style))
    story.append(Paragraph(
        "Cricket pressure is multidimensional: a batter chasing 14 an over at Jaipur ($Par_{venue}=9.36$) faces vastly different physical constraints than at Chinnaswamy ($Par_{venue}=10.15$). Model v3 synthesizes three analytical imperatives: "
        "(1) <b>Contextual Leverage Modeling</b> across 200,999 deliveries with 17 venue-specific par baselines ($Par_{venue}$) and playoff multipliers ($1.20\times$ Qualifiers, $1.30\times$ Final); "
        "(2) <b>Sample Reliability & Empirical Bayes Shrinkage</b> ($K=50$ deliveries) across match-level consistency benchmarks; and "
        "(3) <b>Active Roster Verification (Criteria 1)</b>. "
        "Per strict Round 1 evaluation rules, our mandate is exclusively to measure pure pressure performance without auction/retention filtering; however, to ensure practical utility for scouts, confirmed retired veterans are eliminated via <b>ESPNcricinfo profile status + official public retirement statements</b> (including MS Dhoni transitioning to CSK mentor, Dinesh Karthik to RCB mentor, and Matthew Wade to Australia coach) while preserving all active players (e.g., Jos Buttler, Suryakumar Yadav, Jasprit Bumrah, Sunil Narine, Dhruv Jurel, Tim David).",
        body_style
    ))
    
    story.append(Paragraph("1. Pressure Definition: Dynamic Leverage & Stadium Pitch Pars", h1_style))
    story.append(Paragraph(
        "Static RRR thresholds fail to reflect changing game leverage. We formulate ball-by-ball <b>Pressure Index ($PI_t \in [0, 1]$)</b> calibrated for pitch conditions and match stages:",
        body_style
    ))
    story.append(Paragraph("<b>A. Innings 2 (The Chase):</b> Modeled via three non-linear dynamics: (1) <i>Required Run Rate Urgency</i> relative to venue par [<i>U<sub>RRR</sub> = (1 + e<sup>-0.5(RRR - Par_venue)</sup>)<sup>-1</sup></i>]; (2) <i>Temporal Decay</i> [<i>D<sub>balls</sub> = 1 - (Balls_Rem / 120)</i>]; and (3) <i>Wicket Risk</i> [<i>W<sub>lev</sub> = 1 - (W_in_hand / 10)<sup>1.2</sup></i>].", bullet_style))
    story.append(Paragraph("<b>B. Innings 1 (Target Setting):</b> Evaluates: (1) <i>Death Overs Execution</i> (overs 16–20) where dot vs boundary variance swings par by &plusmn;22 runs; and (2) <i>Top-Order Crisis Recovery</i> (&le;6 overs with &ge;3 wickets down, or &le;10 overs with &ge;4 down).", bullet_style))
    story.append(Paragraph("<b>C. Playoff Stakes & High-Pressure Gate:</b> Stage multipliers reflect tournament pressure (Group = 1.00&times;, Qualifiers/Eliminators = 1.20&times;, Final = 1.30&times;). Deliveries with <b>PI &ge; 0.60</b> are flagged as High-Pressure (HP) (28.92% of total sample, N = 58,125).", bullet_style))
    
    story.append(Paragraph("2. Performance Measurement, Bayes Shrinkage & Active Roster Verification", h1_style))
    story.append(Paragraph(
        "Raw strike rates and economies under pressure can be heavily distorted by small samples. We deploy a multi-stage statistical pipeline:",
        body_style
    ))
    story.append(Paragraph("<b>Empirical Bayes Shrinkage:</b> Observed pressure metrics are shrunk toward empirical tournament priors (&mu;<sub>SR</sub> = 135.0, &mu;<sub>ER</sub> = 9.20, K = 50 balls): <i>&theta;&#770;<sub>i</sub> = (N<sub>i</sub> / (N<sub>i</sub>+K)) &middot; &theta;<sub>i</sub> + (K / (N<sub>i</sub>+K)) &middot; &mu;<sub>0</sub></i>.", bullet_style))
    story.append(Paragraph("<b>Composite Batter Pressure Score (CBPS v3):</b> Blends Shrunk HP Strike Rate (25%), Venue Par Elevation &Delta;SR<sub>venue</sub> (25%), Baseline Elevation &Delta;SR<sub>base</sub> (20%), Dot Ball Minimization (15%), and Match Consistency (15% &mdash; % of pressure innings with SR &ge; 140.0).", bullet_style))
    story.append(Paragraph("<b>Composite Bowler Pressure Score (CBPS v3):</b> Blends Shrunk HP Economy (25%), Venue Run Suppression &Delta;Econ<sub>venue</sub> (25%), Wicket Strike Rate (20%), Dot Ball Pressure (15%), and Spell Consistency (15% &mdash; % of spells with Econ &le; 8.5 or &ge;1 wicket).", bullet_style))
    story.append(Paragraph("<b>Criteria 1 - Active Roster Verification Protocol:</b> Players are evaluated against ESPNcricinfo official profiles and BCCI/board announcements. Confirmed retired personnel (<b>MS Dhoni</b>, retired and appointed CSK mentor; <b>Dinesh Karthik</b>, retired 1 June 2024, now RCB mentor; <b>Matthew Wade</b>, retired Oct 2024, now Australian coach) are removed. Active contracted superstars (<b>Jos Buttler</b>, <b>Dhruv Jurel</b>, <b>Jasprit Bumrah</b>, <b>Tim David</b>) are strictly retained.", bullet_style))
    
    story.append(Paragraph("3. Sample Size Threshold & Fair Evaluation Equity", h1_style))
    story.append(Paragraph(
        "To guarantee statistical power, candidates must have faced or delivered a minimum of <b>200 High-Pressure deliveries</b> (&ge;33.3 overs in crunch situations). Furthermore, a sample confidence multiplier <i>C<sub>i</sub> = min(1.0, &radic;(N<sub>i</sub> / 250))</i> prevents low-sample variance from overshadowing battle-hardened performers.",
        body_style
    ))
    
    # --- PAGE 2: TABLES & CLUTCH MATRICES ---
    story.append(PageBreak())
    story.append(Paragraph("4. Evidence & Definitive Player Rankings (Model v3)", h1_style))
    story.append(Paragraph("<b>Table 1: Top 10 Active Batters Under High Pressure (Official Unstop Selections - Model v3)</b>", ParagraphStyle('Sub', parent=body_style, fontName='Helvetica-Bold', textColor=accent_color)))
    
    bat_data = [
        ["Rank", "Player", "HP Balls", "HP SR", "&Delta;SR Venue", "&Delta;SR Base", "HP Dot%", "Consistency", "Score", "Active Status & Tactical Archetype"],
        ["1", "Naman Dhir", "235", "194.9", "+46.6", "+49.8", "27.2%", "92.9%", "1.48", "Active (MI) &bull; Explosive Boundary Striker"],
        ["2", "Ashutosh Sharma", "307", "171.0", "+20.3", "+87.1", "34.9%", "62.5%", "1.38", "Active (DC) &bull; Crisis Recovery Enforcer"],
        ["3", "Jos Buttler", "319", "185.0", "+34.5", "+38.6", "27.0%", "100.0%", "1.36", "Active &bull; 100% Chase Closer / Match Winner"],
        ["4", "Suryakumar Yadav", "609", "188.8", "+43.1", "+35.1", "30.2%", "77.4%", "1.26", "Active (MI Retained) &bull; 360-Degree Field Sculptor"],
        ["5", "Shreyas Iyer", "420", "177.6", "+29.6", "+38.4", "26.2%", "80.0%", "1.00", "Active &bull; Championship Playoff Match Winner"],
        ["6", "Glenn Phillips", "255", "179.2", "+30.9", "+44.4", "29.0%", "78.6%", "0.90", "Active &bull; Dynamic Versatile Lower-Order Finisher"],
        ["7", "Dhruv Jurel", "325", "171.1", "+21.1", "+40.6", "28.3%", "83.3%", "0.89", "Active (RR Retained) &bull; Elite Clutch Keeper-Batter"],
        ["8", "Marcus Stoinis", "536", "170.7", "+21.3", "+39.8", "31.5%", "64.3%", "0.82", "Active &bull; Power-Hitter & Pace Counter-Attacker"],
        ["9", "Tristan Stubbs", "580", "170.5", "+20.2", "+52.0", "27.6%", "66.7%", "0.81", "Active (DC Retained) &bull; 360 Spin & Pace Destroyer"],
        ["10", "Tim David", "716", "178.5", "+30.0", "+22.5", "34.9%", "81.6%", "0.76", "Active &bull; Death-Overs Heavy Power Finisher"]
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
        
    t_bat = Table(bat_table_rows, colWidths=[22, 86, 36, 36, 42, 42, 38, 48, 32, 138])
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
    
    story.append(Paragraph("<b>Table 2: Top 10 Active Bowlers Under High Pressure (Official Unstop Selections - Model v3)</b>", ParagraphStyle('Sub', parent=body_style, fontName='Helvetica-Bold', textColor=accent_color)))
    
    bowl_data = [
        ["Rank", "Player", "HP Balls", "HP Econ", "&Delta;Econ Venue", "&Delta;Econ Base", "Wkt%", "Consistency", "Score", "Active Status & Tactical Archetype"],
        ["1", "Sunil Narine", "393", "6.20", "+2.90", "+0.88", "6.9%", "95.2%", "1.61", "Active (KKR Retained) &bull; Mystery Spin Constrictor"],
        ["2", "Matheesha Pathirana", "611", "8.53", "+1.40", "+0.10", "10.2%", "91.9%", "1.08", "Active (CSK Retained) &bull; Slingshot Yorker Enforcer"],
        ["3", "Jasprit Bumrah", "646", "7.41", "+1.66", "-0.39", "8.5%", "78.0%", "0.97", "Active (MI Retained) &bull; Gold Standard Death Pacer"],
        ["4", "Mitchell Santner", "418", "7.46", "+1.86", "-0.09", "6.5%", "95.7%", "0.89", "Active &bull; Defensive Middle-Overs Controller"],
        ["5", "Rashid Khan", "800", "8.13", "+0.89", "-1.02", "8.6%", "92.9%", "0.81", "Active (GT Retained) &bull; High-Leverage Strike Spinner"],
        ["6", "Varun Chakravarthy", "674", "8.26", "+0.95", "-0.42", "7.7%", "93.9%", "0.79", "Active (KKR Retained) &bull; Middle & Death Squeeze"],
        ["7", "Taskin Ahmed", "328", "8.62", "+0.71", "-1.03", "9.8%", "87.5%", "0.75", "Active &bull; High-Pace Hard-Length Enforcer"],
        ["8", "Jamie Overton", "202", "8.61", "+0.59", "-0.06", "12.4%", "70.0%", "0.69", "Active &bull; Heavy-Ball Hit-the-Deck Pacer"],
        ["9", "Mitchell Starc", "224", "10.15", "-0.49", "-0.78", "16.1%", "87.5%", "0.68", "Active &bull; Ultimate Wicket Weapon (Wkt/6.2 balls)"],
        ["10", "Rasikh Salam", "250", "9.12", "+0.72", "+0.85", "11.6%", "85.7%", "0.66", "Active &bull; Emerging Pressure Death Bowler"]
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
        
    t_bowl = Table(bowl_table_rows, colWidths=[22, 86, 36, 36, 42, 42, 38, 48, 32, 138])
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
    fig1 = "rr-submission/v3/stage5_deliverables/figures/batter_clutch_matrix.png"
    fig2 = "rr-submission/v3/stage5_deliverables/figures/bowler_clutch_matrix.png"
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
        story.append(Paragraph("<b>Figures 1 & 2:</b> <i>(Left)</i> Active Batter Clutch Matrix: Venue Outperformance vs Baseline Delta. <i>(Right)</i> Active Bowler Clutch Matrix: Venue Economy Suppression vs Wicket Threat %.", caption_style))

    # --- PAGE 3: MODEL EVOLUTION, SCOUTING TAKEAWAYS & VERIFICATION ---
    story.append(PageBreak())
    story.append(Paragraph("5. Progression & Comparative Analysis (v1 &rarr; v2 &rarr; v3)", h1_style))
    story.append(Paragraph(
        "<b>Model Evolution:</b> "
        "(1) <i>Model v1 (Baseline):</i> Established the Dynamic Leverage Index (LI &ge; 1.50) across 200,999 deliveries, isolating high-pressure game states from low-stakes stat padding. "
        "(2) <i>Model v2 (Venue-Calibrated):</i> Integrated 17 stadium scoring baselines ($Par_{venue}$) from 87,074 balls across 5 IPL seasons, correcting stadium skew (Chinnaswamy vs Jaipur). "
        "(3) <i>Model v3 (Active Roster Calibrated):</i> Enforced Criteria 1 by cross-referencing ESPNcricinfo profile status and official public retirement statements, eliminating inactive coaching personnel (MS Dhoni transitioning to CSK mentor, Dinesh Karthik to RCB mentor, Matthew Wade to Australia coach). This cleanly elevated <b>Dhruv Jurel</b> (RR's own clutch keeper-batter, CBPS +0.89 to #7), <b>Shreyas Iyer</b> (+1.00), <b>Marcus Stoinis</b> (+0.82), <b>Tristan Stubbs</b> (+0.81), and <b>Tim David</b> (+0.76) into the verified Top 10.",
        body_style
    ))
    
    story.append(Paragraph("6. Key Tactical Scouting Takeaways for Rajasthan Royals", h1_style))
    story.append(Paragraph(
        "Our venue-calibrated, active roster model provides three direct strategic insights for Rajasthan Royals' match execution at Sawai Mansingh Stadium (Jaipur) and Barsapara Stadium (Guwahati):",
        body_style
    ))
    story.append(Paragraph("<b>1. Retained Asset Validation &ndash; Dhruv Jurel (#7 Batter, CBPS +0.89):</b> With a 171.1 HP Strike Rate (+21.1 above venue par), 28.3% dot balls, and 83.3% match-level consistency, Jurel ranks as India's premier active young clutch finisher. His retention represents mathematically verified championship equity.", bullet_style))
    story.append(Paragraph("<b>2. Unrivaled Spin Stranglehold &ndash; Sunil Narine (#1 Bowler, CBPS +1.61):</b> Conceding 2.90 runs below venue par under pressure with a 6.20 economy rate and 95.2% spell reliability, Narine remains the world benchmark for high-leverage defensive choke.", bullet_style))
    story.append(Paragraph("<b>3. The Dual Threat Paradox &ndash; Starc (#9) vs Bumrah (#3):</b> While Bumrah provides total run containment (7.41 HP Econ, +1.66 vs venue par), Mitchell Starc provides unmatched raw wicket threat (16.1% wkt rate &mdash; 1 wicket every 6.2 pressure balls). Pairing a containment anchor with a pure strike weapon maximizes championship win probability.", bullet_style))
    
    fig3 = "rr-submission/v3/stage5_deliverables/figures/top_10_batters_cbps.png"
    fig4 = "rr-submission/v3/stage5_deliverables/figures/top_10_bowlers_cbps.png"
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
        story.append(Paragraph("<b>Figures 3 & 4:</b> Top 10 Active Batters and Bowlers scored by Composite Pressure Score (CBPS v3).", caption_style))
        
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully compiled v3 report to: {filename}")

if __name__ == '__main__':
    build_pdf_v3()
    build_pdf_v3("rr-submission/v3/stage5_deliverables/Mohammed_Aleem_Bukkapatnam_RR_SupeRR_Selector_Report_v3.pdf")

