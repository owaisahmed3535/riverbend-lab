from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, KeepTogether
)
from reportlab.lib.units import mm
import csv

PDF_FILE = "task3/threat-model.pdf"
CSV_FILE = "task3/risk-ranking.csv"

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "TitleCustom",
    parent=styles["Title"],
    alignment=TA_CENTER,
    fontSize=18,
    spaceAfter=12
)

heading_style = ParagraphStyle(
    "HeadingCustom",
    parent=styles["Heading2"],
    fontSize=13,
    spaceBefore=10,
    spaceAfter=8
)

body_style = ParagraphStyle(
    "BodyCustom",
    parent=styles["BodyText"],
    fontSize=9,
    leading=13
)

small_style = ParagraphStyle(
    "SmallCustom",
    parent=styles["BodyText"],
    fontSize=7,
    leading=9
)

doc = SimpleDocTemplate(
    PDF_FILE,
    pagesize=landscape(A4),
    rightMargin=12 * mm,
    leftMargin=12 * mm,
    topMargin=12 * mm,
    bottomMargin=12 * mm
)

story = []

# Title
story.append(Paragraph(
    "Riverbend Boutique - STRIDE Threat Model",
    title_style
))

story.append(Paragraph(
    "Task 3: System architecture, STRIDE threats and risk ranking",
    body_style
))

story.append(Spacer(1, 8))

# Architecture
story.append(Paragraph("1. System Architecture", heading_style))

architecture = [
    ["CLIENT", "→", "NGINX WEB SERVER", "→", "PHP APPLICATION", "→", "MARIADB DATABASE"],
    ["Browser/User", "HTTP", "Web Server", "FastCGI", "Application", "SQL", "riverbend_shop"],
]

arch_table = Table(
    architecture,
    colWidths=[35*mm, 12*mm, 42*mm, 15*mm, 42*mm, 12*mm, 42*mm]
)

arch_table.setStyle(TableStyle([
    ("GRID", (0,0), (-1,-1), 0.8, colors.black),
    ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
    ("ALIGN", (0,0), (-1,-1), "CENTER"),
    ("VALIGN", (0,0), (-1,-1), "MIDDLE"),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 8),
    ("TOPPADDING", (0,0), (-1,-1), 7),
    ("BOTTOMPADDING", (0,0), (-1,-1), 7),
]))

story.append(arch_table)
story.append(Spacer(1, 8))

story.append(Paragraph(
    "External Services are connected to the PHP Application for external requests and responses. "
    "The lab/application boundary contains the web server, PHP application and MariaDB database.",
    body_style
))

story.append(PageBreak())

# STRIDE explanation
story.append(Paragraph("2. STRIDE Threat Categories", heading_style))

stride_text = (
    "<b>S</b> = Spoofing &nbsp;&nbsp; "
    "<b>T</b> = Tampering &nbsp;&nbsp; "
    "<b>R</b> = Repudiation &nbsp;&nbsp; "
    "<b>I</b> = Information Disclosure &nbsp;&nbsp; "
    "<b>D</b> = Denial of Service &nbsp;&nbsp; "
    "<b>E</b> = Elevation of Privilege"
)

story.append(Paragraph(stride_text, body_style))
story.append(Spacer(1, 8))

story.append(Paragraph(
    "Risk Score = Likelihood × Impact. Both Likelihood and Impact use a 1–5 scale.",
    body_style
))

story.append(Spacer(1, 10))

# Read CSV
rows = []

with open(CSV_FILE, newline="", encoding="utf-8") as file:
    reader = csv.DictReader(file)

    for row in reader:
        rows.append([
            Paragraph(row["Component"], small_style),
            Paragraph(row["Threat"], small_style),
            row["Likelihood"],
            row["Impact"],
            row["Score"]
        ])

# Table header
table_data = [
    [
        Paragraph("<b>Component</b>", small_style),
        Paragraph("<b>Threat</b>", small_style),
        Paragraph("<b>Likelihood</b>", small_style),
        Paragraph("<b>Impact</b>", small_style),
        Paragraph("<b>Score</b>", small_style)
    ]
]

table_data.extend(rows)

risk_table = Table(
    table_data,
    repeatRows=1,
    colWidths=[42*mm, 145*mm, 25*mm, 20*mm, 20*mm]
)

risk_table.setStyle(TableStyle([
    ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
    ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
    ("VALIGN", (0,0), (-1,-1), "TOP"),
    ("ALIGN", (2,1), (-1,-1), "CENTER"),
    ("FONTNAME", (0,0), (-1,0), "Helvetica-Bold"),
    ("FONTSIZE", (0,0), (-1,-1), 7),
    ("TOPPADDING", (0,0), (-1,-1), 4),
    ("BOTTOMPADDING", (0,0), (-1,-1), 4),
]))

story.append(risk_table)

story.append(PageBreak())

# Observed findings
story.append(Paragraph("3. Observed Security Findings", heading_style))

findings = [
    "SQL injection-like request observed in the NGINX access log.",
    "/admin path probing was observed.",
    "/wp-login.php probing was observed.",
    "/etc/passwd probing was observed."
]

for finding in findings:
    story.append(Paragraph("• " + finding, body_style))
    story.append(Spacer(1, 4))

story.append(Spacer(1, 8))

story.append(Paragraph("4. Risk Methodology", heading_style))

story.append(Paragraph(
    "Likelihood and Impact are rated from 1 to 5. The risk score is calculated as "
    "Likelihood × Impact. The risk-ranking CSV is sorted from the highest score to "
    "the lowest score.",
    body_style
))

story.append(Spacer(1, 8))

story.append(Paragraph("5. Scope and Limitations", heading_style))

story.append(Paragraph(
    "This threat model is based on the Riverbend Boutique lab architecture and the "
    "observed log-analysis findings. It represents a simplified lab environment and "
    "does not claim to cover every possible production threat.",
    body_style
))

doc.build(story)

print("PDF created successfully:", PDF_FILE)
