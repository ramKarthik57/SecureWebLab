"""
generate_perfect_academic_report.py
===================================
Produces an academic project report for SecureJobLab (Course: 20CYS403).

Key Requirements Implemented:
1. Student Name: "Ram Karthik G" (no "Persona", no subtitle).
2. Removed 2nd image (diagram_dual_engine.png) as requested.
3. Proper Table of Contents using native Word Tab Stops with Dot Leaders (numbers flush-right).
4. Continuous content flow without artificial mid-chapter gaps or excessive blank spaces.
5. Strictly 5 Core CWE Vulnerabilities (CWE-89, CWE-79, CWE-78, CWE-22, CWE-1021).
6. High-impact Clickjacking UI Redressing demonstration with Opacity slider evidence.
7. Professional academic typography, color palette, borders, callouts, and side-by-side comparative tables.
"""

import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = r"C:\Users\Ram\Desktop\SecureWebLab"
DOCX_OUT = os.path.join(BASE_DIR, "SecureJobLab_Web_Application_Security_Report.docx")
PDF_OUT = os.path.join(BASE_DIR, "SecureJobLab_Web_Application_Security_Report.pdf")

# Images
IMG_ARCH = os.path.join(BASE_DIR, "diagram_architecture.png")
IMG_DB = os.path.join(BASE_DIR, "diagram_db_schema.png")
IMG_LOGIN = os.path.join(BASE_DIR, "screenshot_login_verified.png")
IMG_INDEX = os.path.join(BASE_DIR, "screenshot_index_verified.png")
IMG_APPS = os.path.join(BASE_DIR, "screenshot_applications_verified.png")

LAB_5VULN_DIR = os.path.join(BASE_DIR, "lab_5vuln_screenshots")
IMG_M1_V = os.path.join(LAB_5VULN_DIR, "mod1_vulnerable.png")
IMG_M1_S = os.path.join(LAB_5VULN_DIR, "mod1_secure.png")
IMG_M2_V = os.path.join(LAB_5VULN_DIR, "mod2_vulnerable.png")
IMG_M2_S = os.path.join(LAB_5VULN_DIR, "mod2_secure.png")
IMG_M3_V = os.path.join(LAB_5VULN_DIR, "mod3_vulnerable.png")
IMG_M3_S = os.path.join(LAB_5VULN_DIR, "mod3_secure.png")
IMG_M4_V = os.path.join(LAB_5VULN_DIR, "mod4_vulnerable.png")
IMG_M4_S = os.path.join(LAB_5VULN_DIR, "mod4_secure.png")
IMG_M5_100 = os.path.join(LAB_5VULN_DIR, "clickjack_harmful_100pct.png")
IMG_M5_30 = os.path.join(LAB_5VULN_DIR, "clickjack_harmful_30pct.png")
IMG_M5_TRIG = os.path.join(LAB_5VULN_DIR, "clickjack_harmful_triggered.png")
IMG_M5_S = os.path.join(LAB_5VULN_DIR, "mod5_secure.png")

# Colors
COLOR_NAVY = RGBColor(27, 54, 93)       # #1B365D - H1
COLOR_STEEL = RGBColor(43, 76, 126)     # #2B4C7E - H2
COLOR_SLATE = RGBColor(44, 62, 80)      # #2C3E50 - H3
COLOR_BODY = RGBColor(33, 37, 41)       # #212529 - Text
COLOR_MUTED = RGBColor(108, 117, 125)   # #6C757D - Footers, Captions
COLOR_RED = RGBColor(220, 38, 38)       # #DC2626 - Vuln
COLOR_GREEN = RGBColor(16, 185, 129)    # #10B981 - Secure
COLOR_BLUE = RGBColor(37, 99, 235)      # #2563EB - Highlights

HEX_NAVY = "1B365D"
HEX_STEEL = "2B4C7E"
HEX_LIGHT_GRAY = "F8FAFC"
HEX_BORDER = "CBD5E1"
HEX_CODE_BG = "F8F9FA"
HEX_VULN_BG = "FEF2F2"
HEX_SEC_BG = "F0FDF4"
HEX_VULN_BORDER = "FCA5A5"
HEX_SEC_BORDER = "86EFAC"

# --- XML Helpers ---
def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    for child in list(tcPr):
        if child.tag.endswith('shd'):
            tcPr.remove(child)
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=45, bottom=45, left=60, right=60):
    tcPr = cell._tc.get_or_add_tcPr()
    for child in list(tcPr):
        if child.tag.endswith('tcMar'):
            tcPr.remove(child)
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}>'
                      f'<w:top w:w="{top}" w:type="dxa"/>'
                      f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
                      f'<w:left w:w="{left}" w:type="dxa"/>'
                      f'<w:right w:w="{right}" w:type="dxa"/>'
                      f'</w:tcMar>')
    tcPr.append(tcMar)

def set_cell_borders(cell, top=None, bottom=None, left=None, right=None):
    tcPr = cell._tc.get_or_add_tcPr()
    for child in list(tcPr):
        if child.tag.endswith('tcBorders'):
            tcPr.remove(child)
    borders_elm = OxmlElement('w:tcBorders')
    for side_name, side_opts in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        if side_opts:
            val = side_opts.get('val', 'single')
            sz = side_opts.get('sz', '4')
            color = side_opts.get('color', 'auto')
            el = parse_xml(f'<w:{side_name} {nsdecls("w")} w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>')
            borders_elm.append(el)
        else:
            el = parse_xml(f'<w:{side_name} {nsdecls("w")} w:val="none"/>')
            borders_elm.append(el)
    tcPr.append(borders_elm)

def add_page_number_to_run(run):
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    run._r.append(fldSimple)

# --- Typography Helpers ---
def add_h1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(11)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(14.5)
    r.font.bold = True
    r.font.color.rgb = COLOR_NAVY
    return p

def add_h2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(7)
    p.paragraph_format.space_after = Pt(2.5)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(11.5)
    r.font.bold = True
    r.font.color.rgb = COLOR_STEEL
    return p

def add_h3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(5)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(10)
    r.font.bold = True
    r.font.color.rgb = COLOR_SLATE
    return p

def add_p(doc, text, bold_prefix=None, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2.5)
    p.paragraph_format.line_spacing = 1.12
    if bold_prefix:
        rb = p.add_run(bold_prefix)
        rb.font.name = "Calibri"
        rb.font.size = Pt(9.5)
        rb.font.bold = True
        rb.font.color.rgb = COLOR_SLATE
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(9.5)
    r.font.italic = italic
    r.font.color.rgb = COLOR_BODY
    return p

def add_bullet(doc, text, prefix="• "):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.2)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(1.5)
    p.paragraph_format.line_spacing = 1.12
    rb = p.add_run(prefix)
    rb.font.name = "Calibri"
    rb.font.size = Pt(9)
    rb.font.bold = True
    rb.font.color.rgb = COLOR_STEEL
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(9)
    r.font.color.rgb = COLOR_BODY
    return p

def add_callout(doc, text, title="KEY TAKEAWAY", color_type="blue"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)

    c = tbl.cell(0, 0)
    set_cell_margins(c, top=35, bottom=35, left=50, right=50)

    if color_type == "green":
        bg_hex, border_hex, title_col = "F0FDF4", "10B981", COLOR_GREEN
    elif color_type == "red":
        bg_hex, border_hex, title_col = "FEF2F2", "DC2626", COLOR_RED
    else:
        bg_hex, border_hex, title_col = "F8FAFC", "2563EB", COLOR_STEEL

    set_cell_background(c, bg_hex)
    set_cell_borders(c,
        left={'val': 'single', 'sz': '18', 'color': border_hex},
        top={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
        right={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
        bottom={'val': 'single', 'sz': '4', 'color': HEX_BORDER}
    )

    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.12

    rt = p.add_run(f"[{title}] ")
    rt.font.name = "Calibri"
    rt.font.size = Pt(8.5)
    rt.font.bold = True
    rt.font.color.rgb = title_col

    rb = p.add_run(text)
    rb.font.name = "Calibri"
    rb.font.size = Pt(8.5)
    rb.font.color.rgb = COLOR_BODY

    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(1.5)
    p_after.paragraph_format.space_after = Pt(0)

def add_code_block(doc, code_str, title=None):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)

    c = tbl.cell(0, 0)
    set_cell_margins(c, top=30, bottom=30, left=45, right=45)
    set_cell_background(c, HEX_CODE_BG)
    set_cell_borders(c,
        left={'val': 'single', 'sz': '10', 'color': HEX_STEEL},
        top={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
        right={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
        bottom={'val': 'single', 'sz': '4', 'color': HEX_BORDER}
    )

    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.02

    if title:
        rt = p.add_run(f"// {title}\n")
        rt.font.name = "Consolas"
        rt.font.size = Pt(7.5)
        rt.font.bold = True
        rt.font.color.rgb = COLOR_STEEL

    rc = p.add_run(code_str)
    rc.font.name = "Consolas"
    rc.font.size = Pt(7)
    rc.font.color.rgb = COLOR_BODY

    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(1.5)
    p_after.paragraph_format.space_after = Pt(0)

def add_dual_code_comparison(doc, vuln_code, sec_code, vuln_title, sec_title):
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(3.2)
    tbl.columns[1].width = Inches(3.2)

    c0, c1 = tbl.cell(0, 0), tbl.cell(0, 1)
    set_cell_margins(c0, top=25, bottom=25, left=40, right=40)
    set_cell_margins(c1, top=25, bottom=25, left=40, right=40)

    set_cell_background(c0, HEX_VULN_BG)
    set_cell_borders(c0,
        left={'val': 'single', 'sz': '14', 'color': 'DC2626'},
        top={'val': 'single', 'sz': '4', 'color': HEX_VULN_BORDER},
        right={'val': 'single', 'sz': '4', 'color': HEX_VULN_BORDER},
        bottom={'val': 'single', 'sz': '4', 'color': HEX_VULN_BORDER}
    )

    set_cell_background(c1, HEX_SEC_BG)
    set_cell_borders(c1,
        left={'val': 'single', 'sz': '14', 'color': '16A34A'},
        top={'val': 'single', 'sz': '4', 'color': HEX_SEC_BORDER},
        right={'val': 'single', 'sz': '4', 'color': HEX_SEC_BORDER},
        bottom={'val': 'single', 'sz': '4', 'color': HEX_SEC_BORDER}
    )

    p0 = c0.paragraphs[0]
    p0.paragraph_format.space_before = Pt(0)
    p0.paragraph_format.space_after = Pt(0)
    p0.paragraph_format.line_spacing = 1.02
    r0_t = p0.add_run(f"🔴 {vuln_title}\n")
    r0_t.font.name = "Calibri"
    r0_t.font.size = Pt(8)
    r0_t.font.bold = True
    r0_t.font.color.rgb = COLOR_RED
    r0_c = p0.add_run(vuln_code)
    r0_c.font.name = "Consolas"
    r0_c.font.size = Pt(6.8)
    r0_c.font.color.rgb = COLOR_BODY

    p1 = c1.paragraphs[0]
    p1.paragraph_format.space_before = Pt(0)
    p1.paragraph_format.space_after = Pt(0)
    p1.paragraph_format.line_spacing = 1.02
    r1_t = p1.add_run(f"🟢 {sec_title}\n")
    r1_t.font.name = "Calibri"
    r1_t.font.size = Pt(8)
    r1_t.font.bold = True
    r1_t.font.color.rgb = COLOR_GREEN
    r1_c = p1.add_run(sec_code)
    r1_c.font.name = "Consolas"
    r1_c.font.size = Pt(6.8)
    r1_c.font.color.rgb = COLOR_BODY

    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(1.5)
    p_after.paragraph_format.space_after = Pt(0)

def add_dual_image_comparison(doc, img_vuln, img_sec, cap_vuln, cap_sec):
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(3.2)
    tbl.columns[1].width = Inches(3.2)

    c0, c1 = tbl.cell(0, 0), tbl.cell(0, 1)
    set_cell_margins(c0, top=6, bottom=6, left=6, right=6)
    set_cell_margins(c1, top=6, bottom=6, left=6, right=6)

    if os.path.exists(img_vuln):
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p0.paragraph_format.space_before = Pt(0)
        p0.paragraph_format.space_after = Pt(1)
        p0.add_run().add_picture(img_vuln, width=Inches(3.05))
        p0_cap = c0.add_paragraph()
        p0_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p0_cap.paragraph_format.space_before = Pt(1)
        p0_cap.paragraph_format.space_after = Pt(0)
        r = p0_cap.add_run(f"🔴 {cap_vuln}")
        r.font.name = "Calibri"
        r.font.size = Pt(7.5)
        r.font.bold = True
        r.font.color.rgb = COLOR_RED

    if os.path.exists(img_sec):
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p1.paragraph_format.space_before = Pt(0)
        p1.paragraph_format.space_after = Pt(1)
        p1.add_run().add_picture(img_sec, width=Inches(3.05))
        p1_cap = c1.add_paragraph()
        p1_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p1_cap.paragraph_format.space_before = Pt(1)
        p1_cap.paragraph_format.space_after = Pt(0)
        r = p1_cap.add_run(f"🟢 {cap_sec}")
        r.font.name = "Calibri"
        r.font.size = Pt(7.5)
        r.font.bold = True
        r.font.color.rgb = COLOR_GREEN

    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(2)
    p_after.paragraph_format.space_after = Pt(0)

def add_image_box(doc, img_path, caption, width=Inches(4.6)):
    if not os.path.exists(img_path):
        return

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(img_path, width=width)

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(1)
    p_cap.paragraph_format.space_after = Pt(2)
    rc = p_cap.add_run(f"Figure: {caption}")
    rc.font.name = "Calibri"
    rc.font.size = Pt(8)
    rc.font.italic = True
    rc.font.color.rgb = COLOR_MUTED

# ==============================================================================
# MAIN REPORT BUILDER
# ==============================================================================
def build_report(toc_mapping=None):
    doc = docx.Document()

    # Page Margins: 1 inch all around
    for sec in doc.sections:
        sec.top_margin = Inches(1.0)
        sec.bottom_margin = Inches(1.0)
        sec.left_margin = Inches(1.0)
        sec.right_margin = Inches(1.0)
        sec.page_width = Inches(8.5)
        sec.page_height = Inches(11.0)
        sec.different_first_page_header_footer = True

        # Header
        hdr = sec.header
        p_hdr = hdr.paragraphs[0]
        p_hdr.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_hdr.paragraph_format.space_after = Pt(0)
        r_hdr = p_hdr.add_run("Course: 20CYS403 | Web Application Security Laboratory Report | SecureJobLab")
        r_hdr.font.name = "Calibri"
        r_hdr.font.size = Pt(8)
        r_hdr.font.color.rgb = COLOR_MUTED

        # Footer
        ftr = sec.footer
        p_ftr = ftr.paragraphs[0]
        p_ftr.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_ftr.paragraph_format.space_after = Pt(0)
        p_ftr.paragraph_format.tab_stops.add_tab_stop(Inches(6.5), WD_TAB_ALIGNMENT.RIGHT)

        rf1 = p_ftr.add_run("SecureJobLab Platform — Exactly 5 CWE Security Modules")
        rf1.font.name = "Calibri"
        rf1.font.size = Pt(8.5)
        rf1.font.color.rgb = COLOR_MUTED

        rf_tab = p_ftr.add_run("\tPage ")
        rf_tab.font.name = "Calibri"
        rf_tab.font.size = Pt(8.5)
        rf_tab.font.color.rgb = COLOR_MUTED
        add_page_number_to_run(p_ftr.runs[-1])

    # Default TOC mapping
    if not toc_mapping:
        toc_mapping = {
            "Chapter 1: Introduction, Problem Statement & Objectives": "6",
            "    1.1 Context & Background": "6",
            "    1.2 Problem Statement & Motivation": "6",
            "    1.3 Project Objectives & Methodology": "6",
            "    1.4 Strict 5-Vulnerability Project Scope": "6",
            "Chapter 2: System Architecture & Dual-Engine Design": "7",
            "    2.1 Four-Tier Architecture Model": "7",
            "    2.2 The Dual-Engine Security Execution Model": "7",
            "Chapter 3: Technology Stack & Database Architecture": "8",
            "    3.1 Technology Stack Specification": "8",
            "    3.2 Relational Database Schema Design": "9",
            "Chapter 4: Application Functional Modules": "10",
            "    4.1 Authentication & Role-Based Access Control": "10",
            "    4.2 Instant Job Board & Filtering Engine": "10",
            "    4.3 Candidate Application Pipeline & Local Storage": "11",
            "    4.4 Network Latency & Diagnostic Utilities": "11",
            "Chapter 5: Vulnerability 1 — SQL Injection (SQLi) [CWE-89]": "12",
            "    5.1 Vulnerability Overview & Threat Dynamics": "12",
            "    5.2 Vulnerable Implementation & Insecure Code": "12",
            "    5.3 Secure Mitigation & Parameterized Statements": "13",
            "Chapter 6: Vulnerability 2 — Cross-Site Scripting (XSS) [CWE-79]": "14",
            "    6.1 Vulnerability Overview & Threat Dynamics": "14",
            "    6.2 Vulnerable Implementation & Live Script Execution": "14",
            "    6.3 Secure Mitigation & Contextual Output Encoding": "15",
            "Chapter 7: Vulnerability 3 — OS Command Injection [CWE-78]": "16",
            "    7.1 Vulnerability Overview & Threat Dynamics": "16",
            "    7.2 Vulnerable Implementation & Shell Chaining": "16",
            "    7.3 Secure Mitigation & Strict Whitelisting": "17",
            "Chapter 8: Vulnerability 4 — Directory / Path Traversal [CWE-22]": "18",
            "    8.1 Vulnerability Overview & Threat Dynamics": "18",
            "    8.2 Vulnerable Implementation & Path Climbing": "18",
            "    8.3 Secure Mitigation & Canonical Boundary Defense": "19",
            "Chapter 9: Vulnerability 5 — Clickjacking (UI Redressing) [CWE-1021]": "20",
            "    9.1 Vulnerability Overview & High-Impact Scenario": "20",
            "    9.2 Interactive UI Redressing Sandbox with Opacity": "20",
            "    9.3 Secure Mitigation & HTTP Framing Protection Headers": "21",
            "Chapter 10: Comparative Defense Matrix & Telemetry Analysis": "22",
            "    10.1 Master 5-Vulnerability Security Comparison Matrix": "22",
            "    10.2 Real-time Security Telemetry Engine": "22",
            "Chapter 11: Testing & Verification Methodology": "23",
            "    11.1 Test Plan & Execution Strategy": "23",
            "    11.2 Comprehensive Verification Results Table": "23",
            "Chapter 12: Viva Voce Reference & Security Analysis": "24",
            "Chapter 13: Limitations & Future Enhancements": "25",
            "Chapter 14: Conclusion": "25",
            "References & Authoritative Standards": "26",
        }

    # ==============================================================================
    # PAGE 1: COVER PAGE
    # ==============================================================================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_inst.paragraph_format.space_before = Pt(30)
    p_inst.paragraph_format.space_after = Pt(2)
    r_inst1 = p_inst.add_run("DEPARTMENT OF CYBERSECURITY & COMPUTER ENGINEERING\n")
    r_inst1.font.name = "Calibri"
    r_inst1.font.size = Pt(13)
    r_inst1.font.bold = True
    r_inst1.font.color.rgb = COLOR_NAVY

    r_inst2 = p_inst.add_run("20CYS403: WEB APPLICATION SECURITY LABORATORY\n")
    r_inst2.font.name = "Calibri"
    r_inst2.font.size = Pt(11)
    r_inst2.font.bold = True
    r_inst2.font.color.rgb = COLOR_STEEL

    r_inst3 = p_inst.add_run("ACADEMIC PROJECT REPORT")
    r_inst3.font.name = "Calibri"
    r_inst3.font.size = Pt(10)
    r_inst3.font.bold = True
    r_inst3.font.color.rgb = COLOR_SLATE

    p_div = doc.add_paragraph()
    p_div.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_div.paragraph_format.space_before = Pt(8)
    p_div.paragraph_format.space_after = Pt(24)
    r_div = p_div.add_run("—" * 42)
    r_div.font.color.rgb = COLOR_STEEL

    tbl_title = doc.add_table(rows=1, cols=1)
    tbl_title.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_title.autofit = False
    tbl_title.columns[0].width = Inches(6.5)

    c_t = tbl_title.cell(0, 0)
    set_cell_background(c_t, "F0F7FF")
    set_cell_margins(c_t, top=140, bottom=140, left=140, right=140)
    set_cell_borders(c_t,
        left={'val': 'single', 'sz': '28', 'color': HEX_NAVY},
        top={'val': 'single', 'sz': '6', 'color': HEX_STEEL},
        right={'val': 'single', 'sz': '6', 'color': HEX_STEEL},
        bottom={'val': 'single', 'sz': '6', 'color': HEX_STEEL}
    )

    pt = c_t.paragraphs[0]
    pt.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rt1 = pt.add_run("SecureJobLab: Job Recruitment Vulnerability Demonstration & Defense Platform\n")
    rt1.font.name = "Calibri"
    rt1.font.size = Pt(18)
    rt1.font.bold = True
    rt1.font.color.rgb = COLOR_NAVY

    rt2 = pt.add_run("A Dual-Engine Laboratory for Web Application Vulnerability Analysis & Defensive Engineering\nCovering Exactly Five Core CWE Modules")
    rt2.font.name = "Calibri"
    rt2.font.size = Pt(10.5)
    rt2.font.italic = True
    rt2.font.color.rgb = COLOR_SLATE

    p_sp = doc.add_paragraph()
    p_sp.paragraph_format.space_before = Pt(36)

    # Metadata Table (Just Student Name: Ram Karthik G)
    tbl_meta = doc.add_table(rows=4, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_meta.autofit = False
    tbl_meta.columns[0].width = Inches(2.6)
    tbl_meta.columns[1].width = Inches(3.9)

    meta_data = [
        ("Student Name:", "Ram Karthik G"),
        ("Course Name & Code:", "Web Application Security (20CYS403)"),
        ("Evaluation Scope:", "5 Core CWE Modules (SQLi, XSS, Cmd Inj, Traversal, Clickjacking)"),
        ("Platform Architecture:", "Apache 2.4, PHP 8.x, MySQL 10.4 (MariaDB), AJAX, Bootstrap 5"),
    ]

    for idx, (label, val) in enumerate(meta_data):
        cell_l = tbl_meta.cell(idx, 0)
        cell_r = tbl_meta.cell(idx, 1)
        set_cell_margins(cell_l, top=35, bottom=35, left=50, right=50)
        set_cell_margins(cell_r, top=35, bottom=35, left=50, right=50)
        pl = cell_l.paragraphs[0]
        pr = cell_r.paragraphs[0]
        rl = pl.add_run(label)
        rl.font.name = "Calibri"
        rl.font.size = Pt(10)
        rl.font.bold = True
        rl.font.color.rgb = COLOR_SLATE
        rr = pr.add_run(val)
        rr.font.name = "Calibri"
        rr.font.size = Pt(10)
        rr.font.color.rgb = COLOR_BODY

    p_sp2 = doc.add_paragraph()
    p_sp2.paragraph_format.space_before = Pt(45)

    p_foot = doc.add_paragraph()
    p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
    rf = p_foot.add_run("Academic Year 2026 | Comprehensive Laboratory & Viva Demonstration Package")
    rf.font.name = "Calibri"
    rf.font.size = Pt(9.5)
    rf.font.color.rgb = COLOR_MUTED

    doc.add_page_break()

    # ==============================================================================
    # PAGE 2: CERTIFICATE OF ORIGINALITY
    # ==============================================================================
    add_h1(doc, "Certificate of Originality & Project Declaration")
    add_callout(doc, "This project is prepared strictly for the academic course 20CYS403 (Web Application Security). All vulnerable and secure implementations are isolated on local infrastructure (localhost) using simulated candidate records and controlled lab files.", "ACADEMIC DECLARATION", "blue")

    add_p(doc, "This is to certify that the project report entitled \"SecureJobLab: Job Recruitment Vulnerability Demonstration & Defense Platform\" submitted by Ram Karthik G in partial fulfillment of the academic requirements for the course 20CYS403 Web Application Security represents authentic, original work conducted under laboratory supervision.")
    add_p(doc, "The laboratory implementation rigorously implements, analyzes, and demonstrates exactly five web application security vulnerabilities classified under the Common Weakness Enumeration (CWE) framework:")
    add_bullet(doc, "SQL Injection (SQLi) — CWE-89: Direct query concatenation versus Parameterized Prepared Statements.", "1. ")
    add_bullet(doc, "Cross-Site Scripting (XSS) — CWE-79: Reflected execution versus Contextual HTML Entity Encoding.", "2. ")
    add_bullet(doc, "OS Command Injection — CWE-78: Unsanitized shell concatenation versus Strict Regex Whitelisting and Argument Escaping.", "3. ")
    add_bullet(doc, "Directory / Path Traversal — CWE-22: Arbitrary file inclusion versus Basename Whitelisting and Canonical Boundary Isolation.", "4. ")
    add_bullet(doc, "Clickjacking (UI Redressing) — CWE-1021: Framed destructive actions versus HTTP Framing Defense Headers (X-Frame-Options and CSP).", "5. ")

    add_p(doc, "I hereby declare that this report has been authored with technical diligence, that no external or unapproved vulnerability modules have been included, and that all code snippets, telemetry data, and screenshots accurately reflect the live execution behavior of the SecureJobLab system.")

    p_sig = doc.add_paragraph()
    p_sig.paragraph_format.space_before = Pt(35)
    r_sig1 = p_sig.add_run("Student Signature: ___________________________          Date: October 6, 2026\n\n")
    r_sig1.font.bold = True
    r_sig1.font.color.rgb = COLOR_SLATE
    r_sig2 = p_sig.add_run("Student Name: Ram Karthik G\nCourse Code: 20CYS403 — Web Application Security\nFaculty Evaluation Sign-off: ___________________________")
    r_sig2.font.color.rgb = COLOR_BODY

    doc.add_page_break()

    # ==============================================================================
    # PAGE 3: ACKNOWLEDGEMENTS & ABSTRACT
    # ==============================================================================
    add_h1(doc, "Acknowledgements")
    add_p(doc, "I express my profound gratitude to the faculty and course coordinators of 20CYS403 (Web Application Security) for providing the pedagogical guidance, threat modeling frameworks, and foundational principles that enabled the design and realization of the SecureJobLab platform.")
    add_p(doc, "Special thanks are extended to the open-source cybersecurity community, the Open Web Application Security Project (OWASP), and the MITRE Corporation for maintaining the Common Weakness Enumeration (CWE) repository, which served as the structural benchmark for the vulnerability implementations and defensive architectures evaluated in this report.")

    add_h1(doc, "Executive Summary / Abstract")
    add_p(doc, "Modern web application development frequently balances rapid user experience requirements with rigorous application security controls. Insecure data handling across web endpoints frequently results in severe vulnerabilities that compromise data confidentiality, system integrity, and host availability. To investigate these security dynamics in a realistic business environment, SecureJobLab was engineered as a dual-engine recruitment portal modeled after modern SaaS human-resource platforms.")
    add_p(doc, "Unlike purely conceptual training applications, SecureJobLab pairs realistic recruitment operations—such as multi-criteria job filtering, candidate resume submission, application management, and network latency diagnostics—with a rigorous, switchable security core. The system integrates a global defense switcher ($_SESSION['appsec_mode']) that allows evaluators to toggle in real time between Vulnerable Mode (demonstrating unsafe software construction patterns) and Secure Mitigated Mode (enforcing industry-standard defensive controls).")
    add_p(doc, "The laboratory scope is strictly constrained to five core vulnerabilities: (1) SQL Injection [CWE-89] in job query generation, (2) Reflected Cross-Site Scripting [CWE-79] in search query reflection, (3) OS Command Injection [CWE-78] in gateway network diagnostic execution, (4) Directory Traversal [CWE-22] in candidate document retrieval, and (5) Clickjacking [CWE-1021] targeting an irreversible account deletion action via an interactive UI Redressing sandbox.")
    add_p(doc, "Each vulnerability is examined through root-cause analysis, threat modeling, attack payload mechanics, execution telemetry, and verified defensive mitigation. Verification across all ten test scenarios confirms that parameterized statements, contextual output encoding, strict regex input whitelisting, basename path confinement, and HTTP framing prevention headers completely neutralize the corresponding threat vectors without impeding legitimate application workflows.")

    add_p(doc, "Keywords: Web Application Security, Dual-Engine Architecture, SQL Injection, Cross-Site Scripting, Command Injection, Directory Traversal, Clickjacking, CWE, Defense-in-Depth, 20CYS403.", bold_prefix="Index Terms — ")

    doc.add_page_break()

    # ==============================================================================
    # PAGE 4: TABLE OF CONTENTS (COMPACT FIT TO EXACTLY PAGE 4)
    # ==============================================================================
    add_h1(doc, "Table of Contents")

    for title, page_no in toc_mapping.items():
        p_t = doc.add_paragraph()
        p_t.paragraph_format.tab_stops.add_tab_stop(Inches(6.5), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        p_t.paragraph_format.space_before = Pt(0.5)
        p_t.paragraph_format.space_after = Pt(0.5)
        p_t.paragraph_format.line_spacing = 1.05

        is_ch = title.startswith("Chapter") or title.startswith("References")
        r1 = p_t.add_run(title)
        r1.font.name = "Calibri"
        r1.font.size = Pt(8.5 if not is_ch else 9.0)
        r1.font.bold = is_ch
        r1.font.color.rgb = COLOR_NAVY if is_ch else COLOR_SLATE

        r2 = p_t.add_run(f"\t{page_no}")
        r2.font.name = "Calibri"
        r2.font.size = Pt(8.5 if not is_ch else 9.0)
        r2.font.bold = is_ch
        r2.font.color.rgb = COLOR_NAVY if is_ch else COLOR_SLATE

    doc.add_page_break()

    # ==============================================================================
    # PAGE 5: LIST OF FIGURES & TABLES & ABBREVIATIONS
    # ==============================================================================
    add_h1(doc, "List of Figures & Tables")

    # Exactly 11 figures (Figure 2 dual engine removed)
    figures_list = [
        ("Figure 1", "SecureJobLab Four-Tier System Architecture & Interaction Flow", toc_mapping.get("Chapter 2: System Architecture & Dual-Engine Design", "7")),
        ("Figure 2", "Relational Database Schema & Data Dictionary (securejoblab)", toc_mapping.get("    3.2 Relational Database Schema Design", "9")),
        ("Figure 3", "SecureJobLab Authentication Screen (Candidate & Admin RBAC)", toc_mapping.get("Chapter 4: Application Functional Modules", "10")),
        ("Figure 4", "Recruitment Portal Interface: Verified Cybersecurity Openings", toc_mapping.get("    4.2 Instant Job Board & Filtering Engine", "10")),
        ("Figure 5", "Candidate Application Pipeline & Local Resume Storage Dashboard", toc_mapping.get("    4.3 Candidate Application Pipeline & Local Storage", "11")),
        ("Figure 6", "SQL Injection Demonstration: Insecure Extraction vs. Parameterized Defense", toc_mapping.get("    5.3 Secure Mitigation & Parameterized Statements", "13")),
        ("Figure 7", "Reflected XSS Demonstration: Live Alert Execution vs. Encoded Rendering", toc_mapping.get("    6.3 Secure Mitigation & Contextual Output Encoding", "15")),
        ("Figure 8", "OS Command Injection: Unsanitized Chaining vs. Regex Whitelist Interception", toc_mapping.get("    7.3 Secure Mitigation & Strict Whitelisting", "17")),
        ("Figure 9", "Directory Traversal: Sensitive File Extraction vs. Whitelist Denial", toc_mapping.get("    8.3 Secure Mitigation & Canonical Boundary Defense", "19")),
        ("Figure 10", "Clickjacking UI Redressing: 100% Revealed Mode vs. 30% Ghost Mode", toc_mapping.get("    9.2 Interactive UI Redressing Sandbox with Opacity", "20")),
        ("Figure 11", "Clickjacking Attack Triggered vs. Secure Mitigation (Frame Blocking)", toc_mapping.get("    9.3 Secure Mitigation & HTTP Framing Protection Headers", "21")),
    ]

    add_h2(doc, "List of Figures")
    for fig_id, fig_desc, p_num in figures_list:
        p_f = doc.add_paragraph()
        p_f.paragraph_format.tab_stops.add_tab_stop(Inches(6.5), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        p_f.paragraph_format.space_before = Pt(0.5)
        p_f.paragraph_format.space_after = Pt(0.5)
        p_f.paragraph_format.line_spacing = 1.05
        r = p_f.add_run(f"{fig_id}: ")
        r.font.bold = True
        r.font.size = Pt(8)
        r.font.color.rgb = COLOR_SLATE
        r2 = p_f.add_run(fig_desc)
        r2.font.size = Pt(8)
        r2.font.color.rgb = COLOR_BODY
        r3 = p_f.add_run(f"\t{p_num}")
        r3.font.size = Pt(8)
        r3.font.bold = True
        r3.font.color.rgb = COLOR_SLATE

    tables_list = [
        ("Table 1", "Core Technology Stack & Deployment Dependencies", toc_mapping.get("    3.1 Technology Stack Specification", "8")),
        ("Table 2", "Database Entity-Relationship Schema & Table Specifications", toc_mapping.get("    3.2 Relational Database Schema Design", "9")),
        ("Table 3", "Master 5-Vulnerability Security Comparison & Defense Matrix", toc_mapping.get("Chapter 10: Comparative Defense Matrix & Telemetry Analysis", "22")),
        ("Table 4", "Comprehensive Verification & Test Results Matrix (10 Scenarios)", toc_mapping.get("    11.2 Comprehensive Verification Results Table", "23")),
    ]

    add_h2(doc, "List of Tables")
    for tbl_id, tbl_desc, p_num in tables_list:
        p_t = doc.add_paragraph()
        p_t.paragraph_format.tab_stops.add_tab_stop(Inches(6.5), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        p_t.paragraph_format.space_before = Pt(0.5)
        p_t.paragraph_format.space_after = Pt(0.5)
        p_t.paragraph_format.line_spacing = 1.05
        r = p_t.add_run(f"{tbl_id}: ")
        r.font.bold = True
        r.font.size = Pt(8)
        r.font.color.rgb = COLOR_SLATE
        r2 = p_t.add_run(tbl_desc)
        r2.font.size = Pt(8)
        r2.font.color.rgb = COLOR_BODY
        r3 = p_t.add_run(f"\t{p_num}")
        r3.font.size = Pt(8)
        r3.font.bold = True
        r3.font.color.rgb = COLOR_SLATE

    add_h2(doc, "Abbreviations & Security Terminology")
    abbrevs_list = [
        ("AppSec", "Application Security"),
        ("CWE", "Common Weakness Enumeration"),
        ("OWASP", "Open Web Application Security Project"),
        ("SQLi", "SQL Injection (CWE-89)"),
        ("XSS", "Cross-Site Scripting (CWE-79)"),
        ("CSP", "Content Security Policy"),
        ("RBAC", "Role-Based Access Control"),
        ("DOM", "Document Object Model"),
        ("AST", "Abstract Syntax Tree"),
        ("SIEM", "Security Information and Event Management"),
        ("XHR", "XMLHttpRequest (AJAX)"),
        ("API", "Application Programming Interface"),
    ]

    for abbr, full in abbrevs_list:
        p_a = doc.add_paragraph()
        p_a.paragraph_format.space_before = Pt(0)
        p_a.paragraph_format.space_after = Pt(0.5)
        p_a.paragraph_format.line_spacing = 1.05
        ra = p_a.add_run(f"{abbr}: ")
        ra.font.bold = True
        ra.font.size = Pt(8)
        ra.font.color.rgb = COLOR_STEEL
        rf = p_a.add_run(full)
        rf.font.size = Pt(8)
        rf.font.color.rgb = COLOR_BODY

    doc.add_page_break()

    # ==============================================================================
    # CHAPTER 1: INTRODUCTION, PROBLEM STATEMENT & OBJECTIVES (Page 6)
    # ==============================================================================
    add_h1(doc, "Chapter 1: Introduction, Problem Statement & Objectives")
    add_h2(doc, "1.1 Context & Background")
    add_p(doc, "Web applications represent the predominant attack surface in modern enterprise infrastructure. High-throughput platforms handling human capital, financial transactions, and privileged communications are targeted relentlessly by automated scanners and sophisticated threat actors. In academic cybersecurity curricula, students frequently encounter theoretical definitions of software vulnerabilities without experiencing the contextual nuances of how vulnerabilities manifest within functional software features, or how defensive controls alter execution mechanics.")
    add_p(doc, "To bridge this pedagogical gap, SecureJobLab was conceived as an interactive, dual-engine recruitment portal. The application simulates an enterprise human-resources technology platform—Jobpilot—complete with role-based sign-in, instant job filtering, application submission with resume handling, and network diagnostics. Crucially, the entire architecture is wired to a global security switcher that allows students, researchers, and academic evaluators to observe the exact technical contrast between vulnerable software implementations and their corresponding secure mitigations.")

    add_h2(doc, "1.2 Problem Statement & Motivation")
    add_p(doc, "Conventional web security educational platforms typically suffer from three major design deficiencies: (1) Synthetic Separation: Vulnerability exercises are isolated into abstract forms lacking business logic; (2) Configuration Friction: Toggling defenses requires editing configuration files or restarting daemons; (3) Lack of Comparative Telemetry: Platforms display whether an exploit worked but fail to show the underlying database query, operating system command, or defensive interception telemetry. SecureJobLab resolves these limitations by embedding switchable security states directly into a high-fidelity recruitment platform.")

    add_h2(doc, "1.3 Project Objectives & Methodology")
    add_p(doc, "The key objectives governing the engineering of SecureJobLab include:")
    add_bullet(doc, "Dual-Engine Software Design: Implement a switchable security controller ($_SESSION['appsec_mode']) that alternates application logic between Vulnerable Mode and Secure Mode.", "• ")
    add_bullet(doc, "Pedagogical Realism: Integrate all security demonstrations into functional recruiting features including job search, candidate document inspection, diagnostic latency checks, and account management.", "• ")
    add_bullet(doc, "Transparent Security Telemetry: Deliver structured JSON telemetry displaying the executed SQL syntax, operating system commands, filtered file paths, and active defensive headers.", "• ")

    add_h2(doc, "1.4 Strict 5-Vulnerability Project Scope")
    add_p(doc, "To ensure rigorous evaluation and preserve pedagogical focus, SecureJobLab strictly delimits its scope to exactly five core vulnerabilities: (1) SQLi [CWE-89], (2) XSS [CWE-79], (3) OS Command Injection [CWE-78], (4) Directory Traversal [CWE-22], and (5) Clickjacking [CWE-1021]. All external or deprecated attack vectors are excluded.")

    add_callout(doc, "Strict Scope Delimitation: SecureJobLab explicitly covers only the five approved CWE modules. Unrelated or deprecated attack classes (such as CSRF, SSRF, CORS, broken authentication, or insecure file upload) are strictly excluded, ensuring focused, rigorous depth.", "SCOPE ENFORCEMENT", "blue")

    doc.add_page_break()

    # ==============================================================================
    # CHAPTER 2: SYSTEM ARCHITECTURE & DUAL-ENGINE DESIGN (Page 7)
    # ==============================================================================
    add_h1(doc, "Chapter 2: System Architecture & Dual-Engine Design")
    add_h2(doc, "2.1 Four-Tier Architecture Model")
    add_p(doc, "SecureJobLab is structured as a decoupled four-tier web architecture designed for modularity, low latency, and deterministic evaluation. The system separates user interaction, security state management, API request dispatching, and system resources.")

    add_image_box(doc, IMG_ARCH, "SecureJobLab Four-Tier System Architecture & Interaction Flow", width=Inches(4.5))

    add_p(doc, "The four architectural tiers operate as follows:")
    add_bullet(doc, "Presentation Tier: Developed in HTML5, CSS3, and JavaScript utilizing the Jobpilot design system. Provides the job search interface, candidate dashboard, authentication screens, and AppSec testing telemetry panels.", "1. ")
    add_bullet(doc, "Security Controller Tier: Governed by the global session state ($_SESSION['appsec_mode']). Coordinates between the Vulnerable engine and the Secure engine across both portal features and lab testing endpoints.", "2. ")
    add_bullet(doc, "Application & API Tier: Implemented in api.php and index.php. Acts as the centralized REST/AJAX router handling job CRUD operations, application submissions, and the five vulnerability testing routines.", "3. ")
    add_bullet(doc, "Data & Subsystem Tier: Encapsulates the MySQL relational database (securejoblab), the local filesystem (lab_files and uploads/resumes), and the host operating system shell subsystem.", "4. ")

    add_h2(doc, "2.2 The Dual-Engine Security Execution Model")
    add_p(doc, "The foundational innovation of SecureJobLab is its Dual-Engine Execution Pipeline. Rather than requiring evaluators to modify configuration files or restart services, the entire application toggles its defensive posture via an interactive navbar switch. Identical attack payloads traverse completely different execution paths depending on the active security mode:")
    add_bullet(doc, "🔴 Vulnerable Mode: Untrusted input flows without validation or escaping directly into dangerous execution sinks (mysqli_query(), browser DOM, shell_exec(), file_get_contents(), and unheadered iframe embedding). The attack succeeds, and exploit telemetry is recorded.", "• ")
    add_bullet(doc, "🟢 Secure Mode: The payload is intercepted by defensive mechanisms (parameterized query compilation, contextual htmlspecialchars() encoding, strict regex whitelisting, basename() isolation, and X-Frame-Options: DENY headers). The attack is completely neutralized, and defensive verification telemetry is recorded.", "• ")

    add_callout(doc, "Global State Synchronization: The active security mode is persisted across the PHP session ($_SESSION['appsec_mode']) and reflected dynamically in the UI navbar badge, enabling simultaneous testing across both functional views and lab pills.", "STATE PERSISTENCE", "blue")

    doc.add_page_break()

    # ==============================================================================
    # CHAPTER 3: TECHNOLOGY STACK & DATABASE ARCHITECTURE (Pages 8 & 9)
    # ==============================================================================
    add_h1(doc, "Chapter 3: Technology Stack & Database Architecture")
    add_h2(doc, "3.1 Technology Stack Specification")
    add_p(doc, "To guarantee deterministic behavior, rapid viva demonstrations, and frictionless portability on standard university laboratory machines, SecureJobLab is built on an enterprise open-source technology stack:")

    tech_data = [
        ("Web Server", "Apache HTTP Server 2.4", "Listens on port 80; manages HTTP requests, header emission, and PHP handler execution."),
        ("Database Engine", "MySQL 10.4 (MariaDB)", "Listens on port 3306; manages relational tables, indexes, and parameterized query execution."),
        ("Server Language", "PHP 8.2+ (OOP & Procedural)", "Executes backend routing, session state control, raw string parsing, and secure sanitization."),
        ("Frontend UI", "HTML5, CSS3, Bootstrap 5.3", "Jobpilot SaaS theme, interactive telemetry cards, modals, and responsive layout."),
        ("Asynchronous Comms", "Vanilla JavaScript (Fetch API)", "Non-blocking AJAX request dispatching, DOM updates, and live script execution handling."),
    ]

    tbl_tech = doc.add_table(rows=len(tech_data) + 1, cols=3)
    tbl_tech.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_tech.autofit = False
    tbl_tech.columns[0].width = Inches(1.5)
    tbl_tech.columns[1].width = Inches(1.8)
    tbl_tech.columns[2].width = Inches(3.2)

    for i, h in enumerate(["Component Layer", "Technology Selected", "Role in SecureJobLab"]):
        cell = tbl_tech.cell(0, i)
        set_cell_background(cell, HEX_NAVY)
        set_cell_margins(cell, top=35, bottom=35, left=45, right=45)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for row_idx, data in enumerate(tech_data, start=1):
        bg_col = HEX_LIGHT_GRAY if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(data):
            cell = tbl_tech.cell(row_idx, col_idx)
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=30, bottom=30, left=40, right=40)
            set_cell_borders(cell,
                top={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
                bottom={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
                left={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
                right={'val': 'single', 'sz': '4', 'color': HEX_BORDER}
            )
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.name = "Calibri"
            r.font.size = Pt(7.5)
            r.font.color.rgb = COLOR_BODY

    p_after_t = doc.add_paragraph()
    p_after_t.paragraph_format.space_before = Pt(3)

    add_p(doc, "The consolidated project architecture consists of exactly six root files: index.php (main application container), login.php (authentication), logout.php (session cleanup), api.php (AJAX and lab engine), clickjack_target.php (framed victim endpoint), and database.sql (seed schema). This self-contained structure prevents dependency drift and allows instant restoration on any standard XAMPP deployment.")

    add_p(doc, "All communication between client interfaces and the backend engine occurs via asynchronous JSON contracts, ensuring instantaneous DOM feedback during live laboratory testing.")

    doc.add_page_break()

    # Page 9: 3.2 Relational Database Schema Design
    add_h2(doc, "3.2 Relational Database Schema Design")
    add_p(doc, "The database schema for securejoblab is engineered with UTF-8 (utf8mb4) character encoding, ensuring pristine rendering of international currency symbols (such as the Indian Rupee ₹) without mojibake corruption. The schema consists of four relational tables:")

    add_image_box(doc, IMG_DB, "Relational Database Schema & Data Dictionary (securejoblab)", width=Inches(4.6))

    sch_data = [
        ("users", "id (INT)", "username, password, full_name, role", "Stores authentication credentials; password verification and RBAC roles."),
        ("jobs", "id (INT)", "title, company, location, salary, secret_notes", "Target for SQLi; secret_notes contains confidential compensation bands."),
        ("applications", "id (INT)", "job_title, applicant_name, resume_file, status", "Tracks candidate submissions; links to uploaded resume documents."),
        ("feedback", "id (INT)", "author, comment, created_at", "Stores recruiter feedback; used for output reflection testing."),
    ]

    tbl_schema = doc.add_table(rows=len(sch_data) + 1, cols=4)
    tbl_schema.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_schema.autofit = False
    tbl_schema.columns[0].width = Inches(1.1)
    tbl_schema.columns[1].width = Inches(1.1)
    tbl_schema.columns[2].width = Inches(2.0)
    tbl_schema.columns[3].width = Inches(2.3)

    for i, h in enumerate(["Table Name", "Primary Key", "Key Attributes", "Security / Functional Role"]):
        cell = tbl_schema.cell(0, i)
        set_cell_background(cell, HEX_NAVY)
        set_cell_margins(cell, top=35, bottom=35, left=45, right=45)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for row_idx, data in enumerate(sch_data, start=1):
        bg_col = HEX_LIGHT_GRAY if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(data):
            cell = tbl_schema.cell(row_idx, col_idx)
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=25, bottom=25, left=35, right=35)
            set_cell_borders(cell,
                top={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
                bottom={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
                left={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
                right={'val': 'single', 'sz': '4', 'color': HEX_BORDER}
            )
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.name = "Calibri"
            r.font.size = Pt(7.5)
            r.font.color.rgb = COLOR_BODY

    p_after_sch = doc.add_paragraph()
    p_after_sch.paragraph_format.space_before = Pt(3)

    add_p(doc, "Seed records are prepopulated in database.sql to provide authentic application data immediately upon deployment, including active openings from AWS, Stripe, Microsoft India, Razorpay, and CRED.")

    doc.add_page_break()

    # ==============================================================================
    # CHAPTER 4: APPLICATION FUNCTIONAL MODULES (Pages 10 & 11)
    # ==============================================================================
    add_h1(doc, "Chapter 4: Application Functional Modules")
    add_h2(doc, "4.1 Authentication & Role-Based Access Control (login.php)")
    add_p(doc, "The authentication portal (login.php) models a modern SaaS authentication screen with tabbed sign-in and registration interfaces. The authentication engine verifies credentials against the users table. Evaluators can sign in using candidate accounts (e.g., ram.karthik@securejob.io / candidate123) or administrative credentials.")

    add_image_box(doc, IMG_LOGIN, "SecureJobLab Authentication Screen (Candidate & Admin RBAC)", width=Inches(4.4))

    add_h2(doc, "4.2 Instant Job Board & Filtering Engine (index.php)")
    add_p(doc, "The primary job board presents five verified high-tier cybersecurity positions (Amazon Web Services, Stripe, Microsoft India, Razorpay, CRED). An instant AJAX search engine filters jobs dynamically across titles, companies, locations, and employment types without requiring complete page reloads.")

    add_image_box(doc, IMG_INDEX, "Recruitment Portal Interface: Verified Cybersecurity Openings", width=Inches(4.4))

    doc.add_page_break()

    # Page 11: 4.3 & 4.4 Candidate Applications & Utilities
    add_h2(doc, "4.3 Candidate Application Pipeline & Local Document Storage")
    add_p(doc, "Authenticated candidates can submit applications with customized cover notes and resume file attachments. Attached resumes are processed by api.php and stored locally under uploads/resumes/. The My Applications tab displays live application status tracking ('Interview Scheduled', 'Under Review') and allows candidate-driven application withdrawal.")

    add_image_box(doc, IMG_APPS, "Candidate Application Pipeline & Local Resume Storage Dashboard", width=Inches(4.4))

    add_h2(doc, "4.4 Network Latency & Diagnostic Utilities")
    add_p(doc, "To provide realistic functional grounding for server-side testing, SecureJobLab incorporates internal system administration utilities:")
    add_bullet(doc, "Network Gateway Latency Checker: Simulates ICMP host availability testing across company data centers via server-side diagnostic pings.", "• ")
    add_bullet(doc, "Candidate Document Viewer: Loads candidate resumes, cover notes, and certifications from isolated local folders.", "• ")
    add_bullet(doc, "Database State Reset Tool: Allows evaluators to reseed database tables to initial pristine values with a single click.", "• ")

    add_p(doc, "These utilities operate transparently within the application container, ensuring that all backend systems are directly accessible for pedagogical inspection.")

    doc.add_page_break()

    # ==============================================================================
    # CHAPTER 5: VULNERABILITY 1 — SQL INJECTION (SQLi) [CWE-89] (Pages 12 & 13)
    # ==============================================================================
    add_h1(doc, "Chapter 5: Vulnerability 1 — SQL Injection (SQLi) [CWE-89]")
    add_h2(doc, "5.1 Vulnerability Overview & Threat Dynamics")
    add_p(doc, "SQL Injection (CWE-89) occurs when untrusted user input is directly concatenated into a dynamic SQL query without syntax separation or parameter binding. In web applications, this allows threat actors to manipulate query logic, bypass authentication, extract confidential data, or execute administrative commands.")

    add_h2(doc, "5.2 Vulnerable Implementation & Insecure Code Listing")
    add_p(doc, "In SecureJobLab's Vulnerable Mode, the search parameter is interpolated directly into the database query string inside api.php:")

    add_code_block(doc,
"""// Vulnerable: Direct String Concatenation into SQL Query
$search = $_GET['search'] ?? '';
$query = "SELECT id, title, company, salary, secret_notes FROM jobs
          WHERE title LIKE '%" . $search . "%'";
$result = mysqli_query($conn, $query);""",
    title="api.php (Vulnerable Query Execution)")

    add_h3(doc, "Attack Execution & Data Exfiltration Mechanics")
    add_p(doc, "An attacker supplies the classic boolean bypass payload: ' OR 1=1 #. Because the input contains a single quote, it closes the literal string delimiter early. The subsequent OR 1=1 creates an unconditionally true condition, and the trailing hash (#) comments out the rest of the query. As a result, the database engine returns all job listings, including hidden executive compensation bands and confidential interview rubrics stored in secret_notes.")

    add_p(doc, "The vulnerability exposes sensitive data records that were never intended for public candidate viewing, completely circumventing application-level data isolation.")

    doc.add_page_break()

    # Page 13: SQLi Defense
    add_h2(doc, "5.3 Secure Mitigation & Parameterized Prepared Statements")
    add_p(doc, "In Secure Mode, dynamic string interpolation is replaced by Parameterized Prepared Statements using the PHP mysqli extension:")

    add_dual_code_comparison(doc,
"""// Vulnerable: String Concatenation
$query = "SELECT id, title, company, salary,
  secret_notes FROM jobs WHERE title = '$payload'";
$res = mysqli_query($conn, $query);""",
"""// Secure: Prepared Statement with Parameter Binding
$stmt = mysqli_prepare($conn, "SELECT id, title,
  company, salary, secret_notes FROM jobs
  WHERE title = ?");
mysqli_stmt_bind_param($stmt, "s", $payload);
mysqli_stmt_execute($stmt);
$res = mysqli_stmt_get_result($stmt);""",
    "Vulnerable Dynamic Query", "Secure Prepared Statement")

    add_p(doc, "In the secure implementation, the database engine compiles the SQL query structure into an Abstract Syntax Tree (AST) before user data is evaluated. The payload is bound strictly as a literal string. Supplying ' OR 1=1 # merely searches for a job whose literal title matches that exact sequence, returning zero records and completely neutralizing the attack.")

    add_dual_image_comparison(doc, IMG_M1_V, IMG_M1_S,
        "SQLi Vulnerable: 5 Records & Secret Notes Dumped",
        "SQLi Secure: Parameterized Defense Neutralizes Injection")

    add_callout(doc, "Defense Verified: Parameterized prepared statements (mysqli_prepare + mysqli_stmt_bind_param) separate query structure from data evaluation, eliminating SQL injection vulnerability regardless of input characters.", "KEY TAKEAWAY", "green")

    doc.add_page_break()

    # ==============================================================================
    # CHAPTER 6: VULNERABILITY 2 — CROSS-SITE SCRIPTING (XSS) [CWE-79] (Pages 14 & 15)
    # ==============================================================================
    add_h1(doc, "Chapter 6: Vulnerability 2 — Cross-Site Scripting (XSS) [CWE-79]")
    add_h2(doc, "6.1 Vulnerability Overview & Threat Dynamics")
    add_p(doc, "Cross-Site Scripting (CWE-79) occurs when an application receives untrusted data and includes it in a web page without proper validation or encoding. In a Reflected XSS attack, the malicious script payload is reflected off the web server to the victim's browser, where it executes in the user's security context.")

    add_h2(doc, "6.2 Vulnerable Implementation & Live Script Execution")
    add_p(doc, "In SecureJobLab's Vulnerable Mode, search queries entered on search.php or index.php are reflected directly into the Document Object Model (DOM) using raw innerHTML assignment or unescaped PHP echo:")

    add_code_block(doc,
"""// Vulnerable: Raw Reflection of User Input in DOM
$q = $_GET['q'] ?? '';
echo "<div class='alert alert-info'>Search results for: " . $q . "</div>";
// In Frontend JS:
resultsBanner.innerHTML = "Showing results for: " + data.query;""",
    title="search.php & api.php (Unsanitized Reflection)")

    add_h3(doc, "Attack Execution & Proof-of-Concept")
    add_p(doc, "When an evaluator submits <script>alert(\"XSS\");</script> or <img src=x onerror=alert('XSS')>, the browser treats the input as executable HTML/JavaScript rather than plain text. The script executes immediately, opening the browser's native alert dialog and proving arbitrary JavaScript execution capability.")

    add_p(doc, "In an enterprise recruiting portal, an attacker could exploit this vulnerability to steal session tokens, hijack recruiter accounts, or redirect applicants to phishing portals.")

    doc.add_page_break()

    # Page 15: XSS Defense
    add_h2(doc, "6.3 Secure Mitigation & Contextual Output Encoding")
    add_p(doc, "In Secure Mode, all reflected content is sanitized through contextual HTML entity encoding using htmlspecialchars() before output emission, and rendered in JavaScript via textContent:")

    add_dual_code_comparison(doc,
"""// Vulnerable: Raw Echo into DOM
echo "<div>Results: " . $q . "</div>";
// Frontend:
banner.innerHTML = "Query: " + q;""",
"""// Secure: Contextual HTML Entity Encoding
echo "<div>Results: " .
  htmlspecialchars($q, ENT_QUOTES, 'UTF-8') .
  "</div>";
// Frontend:
banner.textContent = "Query: " + q;""",
    "Vulnerable Raw Reflection", "Secure Contextual Encoding")

    add_p(doc, "By converting sensitive HTML control characters into benign entities (< becomes &lt;, > becomes &gt;, \" becomes &quot;, and ' becomes &#039;), the browser's HTML parser treats the payload strictly as printable text. Script execution is completely prevented.")

    add_dual_image_comparison(doc, IMG_M2_V, IMG_M2_S,
        "XSS Vulnerable: Script Executes Native Alert Dialog",
        "XSS Secure: htmlspecialchars() Safely Encodes Tags")

    add_callout(doc, "Defense Verified: Contextual output encoding (htmlspecialchars with ENT_QUOTES and UTF-8) instructs browser parsers to interpret user characters as literal text rather than executable markup.", "KEY TAKEAWAY", "green")

    doc.add_page_break()

    # ==============================================================================
    # CHAPTER 7: VULNERABILITY 3 — OS COMMAND INJECTION [CWE-78] (Pages 16 & 17)
    # ==============================================================================
    add_h1(doc, "Chapter 7: Vulnerability 3 — OS Command Injection [CWE-78]")
    add_h2(doc, "7.1 Vulnerability Overview & Threat Dynamics")
    add_p(doc, "OS Command Injection (CWE-78) occurs when an application passes untrusted data to a system shell without sanitizing shell metacharacters (&, |, ;, $, `, >). This allows an attacker to append arbitrary operating system commands, potentially compromising the host server.")

    add_h2(doc, "7.2 Vulnerable Implementation & Shell Chaining")
    add_p(doc, "SecureJobLab includes an internal network latency diagnostics utility simulating ping checks on company gateways. In Vulnerable Mode, user input is concatenated directly into the shell execution string:")

    add_code_block(doc,
"""// Vulnerable: Direct Shell Concatenation
$host = $_POST['host'] ?? '127.0.0.1';
$cmd = (strtoupper(substr(PHP_OS, 0, 3)) === 'WIN')
    ? "ping -n 1 " . $host
    : "ping -c 1 " . $host;
$output = shell_exec($cmd);""",
    title="api.php (Unsanitized shell_exec)")

    add_h3(doc, "Attack Execution & Host Subversion")
    add_p(doc, "An evaluator enters: 127.0.0.1 & whoami. The ampersand (&) operator acts as a shell command separator in both Windows cmd.exe and Unix bash. The operating system completes the ping command, then immediately executes whoami, returning the active system user (e.g., desktop-admin\\ram) in the telemetry box.")

    add_p(doc, "This allows unauthenticated attackers to execute arbitrary system binaries, inspect local system architecture, and escalate privileges.")

    doc.add_page_break()

    # Page 17: Command Injection Defense
    add_h2(doc, "7.3 Secure Mitigation & Strict Whitelisting")
    add_p(doc, "In Secure Mode, defense-in-depth is enforced by combining strict regular expression whitelisting with shell argument escaping via escapeshellarg():")

    add_dual_code_comparison(doc,
"""// Vulnerable: Unsanitized Concatenation
$cmd = "ping -n 1 " . $target;
$output = shell_exec($cmd);""",
"""// Secure: Strict Regex Whitelist + Argument Escaping
if (!preg_match('/^[a-zA-Z0-9.-]+$/', $target) ||
    strpos($target, '&') !== false) {
    die("Security Exception: Illegal characters");
}
$safe_target = escapeshellarg($target);
$cmd = "ping -n 1 " . $safe_target;
$output = shell_exec($cmd);""",
    "Vulnerable Concatenation", "Secure Whitelist + Escaping")

    add_p(doc, "The regular expression ^[a-zA-Z0-9.-]+$ ensures the input contains only valid alphanumeric characters, dots, and hyphens. All command separators (&, |, ;, $, `) are immediately rejected, preventing malicious command chaining.")

    add_dual_image_comparison(doc, IMG_M3_V, IMG_M3_S,
        "Cmd Inj Vulnerable: Executes ping followed by whoami",
        "Cmd Inj Secure: Regex Whitelist Intercepts Metacharacters")

    add_callout(doc, "Defense Verified: Combining strict regex whitelisting with escapeshellarg() prevents command chaining by enforcing syntactic conformance before any system call.", "KEY TAKEAWAY", "green")

    doc.add_page_break()

    # ==============================================================================
    # CHAPTER 8: VULNERABILITY 4 — DIRECTORY / PATH TRAVERSAL [CWE-22] (Pages 18 & 19)
    # ==============================================================================
    add_h1(doc, "Chapter 8: Vulnerability 4 — Directory / Path Traversal [CWE-22]")
    add_h2(doc, "8.1 Vulnerability Overview & Threat Dynamics")
    add_p(doc, "Directory Traversal (CWE-22), also known as Path Traversal, occurs when an application accepts input referencing files without properly restricting relative path operators (such as ../ or ..\\). This allows attackers to traverse directory hierarchies and access sensitive files outside the intended folder.")

    add_h2(doc, "8.2 Vulnerable Implementation & Path Climbing")
    add_p(doc, "SecureJobLab provides a Candidate Document Viewer that loads resumes, cover letters, and interview notes from a dedicated folder (lab_files/). In Vulnerable Mode, the requested file path is concatenated directly:")

    add_code_block(doc,
"""// Vulnerable: Direct Path Concatenation
$doc = $_GET['file'] ?? 'sample_resume.txt';
$filepath = __DIR__ . '/lab_files/' . $doc;
if (file_exists($filepath)) {
    echo file_get_contents($filepath);
}""",
    title="api.php (Unsanitized file_get_contents)")

    add_h3(doc, "Attack Execution & Sensitive File Extraction")
    add_p(doc, "An attacker supplies: ../database.sql. The relative path operator climbs out of the lab_files/ directory into the application root, reading the database schema file and revealing table definitions, administrator passwords, and seed data.")

    add_p(doc, "In enterprise production environments, an attacker using directory traversal can exfiltrate server configuration files (such as .env, wp-config.php, or /etc/passwd), leading to total host compromise.")

    doc.add_page_break()

    # Page 19: Directory Traversal Defense
    add_h2(doc, "8.3 Secure Mitigation & Canonical Boundary Defense")
    add_p(doc, "In Secure Mode, the application applies basename() stripping and validates the requested file against an explicit whitelist of approved documents:")

    add_dual_code_comparison(doc,
"""// Vulnerable: Relative Path Resolution
$path = 'lab_files/' . $doc;
return file_get_contents($path);""",
"""// Secure: basename() Stripping + Whitelist Validation
$clean = basename($doc); // Strips ../ and ..\\
$allowed = ['sample_resume.txt', 'job_offer_letter.txt'];
if (!in_array($clean, $allowed, true)) {
    die("Access Denied: Unapproved file request.");
}
$path = realpath(__DIR__ . '/lab_files/' . $clean);
return file_get_contents($path);""",
    "Vulnerable Relative Inclusion", "Secure Basename & Whitelist")

    add_p(doc, "basename() extracts only the trailing filename component, neutralizing directory traversal characters. The whitelist validation guarantees that even if a valid file exists in the directory, only explicitly approved documents are readable.")

    add_dual_image_comparison(doc, IMG_M4_V, IMG_M4_S,
        "Traversal Vulnerable: database.sql Exfiltrated",
        "Traversal Secure: basename() Whitelist Denies Access")

    add_callout(doc, "Defense Verified: basename() stripping combined with strict filename whitelisting confines file resolution to designated public files, completely blocking directory climbing.", "KEY TAKEAWAY", "green")

    doc.add_page_break()

    # ==============================================================================
    # CHAPTER 9: VULNERABILITY 5 — CLICKJACKING (UI REDRESSING) [CWE-1021] (Pages 20 & 21)
    # ==============================================================================
    add_h1(doc, "Chapter 9: Vulnerability 5 — Clickjacking (UI Redressing) [CWE-1021]")
    add_h2(doc, "9.1 Vulnerability Overview & High-Impact Destructive Scenario")
    add_p(doc, "Clickjacking (CWE-1021), also termed UI Redressing, occurs when an attacker renders a legitimate, authenticated application inside a transparent iframe overlaying an enticing decoy interface. When the victim clicks the visible decoy, the click lands on a hidden, sensitive button inside the framed application.")
    add_p(doc, "In SecureJobLab, the framed target (clickjack_target.php) models a destructive action: Permanent Account Deletion & Data Wipe for candidate Ram Karthik G (UID SJ-9042-ADMIN).")

    add_h2(doc, "9.2 Interactive UI Redressing Sandbox with Opacity Slider")
    add_p(doc, "To provide clear visual proof during academic examination, Module 5 integrates an interactive UI Redressing Sandbox featuring a live Opacity Slider (0% to 100%):")
    add_bullet(doc, "0% Stealth Mode: The destructive target iframe is completely transparent. The user sees only the decoy button: '🎉 Claim Your ₹50,000 Signing Bonus!'.", "• ")
    add_bullet(doc, "30% Ghost Mode: Demonstrates the alignment between the decoy button and the destructive '⚠️ Permanently Delete Account' button directly underneath.", "• ")
    add_bullet(doc, "100% Revealed Mode: The red destructive target box is visible, proving framing occurs without restriction.", "• ")

    add_dual_image_comparison(doc, IMG_M5_100, IMG_M5_30,
        "100% Revealed Mode: Destructive Delete Button",
        "30% Ghost Mode: Target Button Aligned Under Decoy")

    doc.add_page_break()

    # Page 21: Clickjacking Trigger & Defense
    add_h3(doc, "Exploit Execution & Destructive Action Trigger")
    add_p(doc, "When the user clicks the decoy button in Stealth Mode, the hijacked click executes the destructive account deletion form:")

    add_dual_image_comparison(doc, IMG_M5_TRIG, IMG_M5_S,
        "Exploit Triggered: Account Deletion Executed",
        "Defense Verified: Framing Blocked via X-Frame-Options")

    add_h2(doc, "9.3 Secure Mitigation & HTTP Framing Protection Headers")
    add_p(doc, "In Secure Mode, clickjack_target.php emits defense-in-depth HTTP security headers:")

    add_dual_code_comparison(doc,
"""// Vulnerable: Missing Framing Headers
// Browser permits third-party iframe embedding
// (No X-Frame-Options or CSP headers emitted)""",
"""// Secure: Strict Framing Defense Headers
header("X-Frame-Options: DENY");
header("Content-Security-Policy: frame-ancestors 'none'");""",
    "Vulnerable Framing Permitted", "Secure Framing Blocked")

    add_p(doc, "Modern web browsers inspect X-Frame-Options: DENY and CSP frame-ancestors 'none' prior to rendering framed content. When detected, the browser terminates iframe rendering, preventing UI redressing entirely.")

    add_callout(doc, "Defense Verified: X-Frame-Options: DENY and CSP frame-ancestors 'none' instruct modern browsers to reject all iframe embedding attempts, neutralizing Clickjacking.", "KEY TAKEAWAY", "green")

    doc.add_page_break()

    # ==============================================================================
    # CHAPTER 10: MASTER COMPARISON MATRIX & TELEMETRY (Page 22)
    # ==============================================================================
    add_h1(doc, "Chapter 10: Comparative Defense Matrix & Telemetry Analysis")
    add_h2(doc, "10.1 Master 5-Vulnerability Security Comparison Matrix")
    add_p(doc, "The following matrix provides a technical comparison of the five implemented vulnerabilities, summarizing their root causes, exploit impacts, mitigations, and verified statuses:")

    matrix_data = [
        ("SQL Injection (SQLi)", "CWE-89", "Unsanitized dynamic string interpolation in SQL queries.", "Parameterized Prepared Statements (mysqli_prepare).", "VERIFIED (PASS)"),
        ("Cross-Site Scripting (XSS)", "CWE-79", "Direct raw output reflection into DOM without encoding.", "Contextual HTML Entity Encoding (htmlspecialchars).", "VERIFIED (PASS)"),
        ("OS Command Injection", "CWE-78", "Direct concatenation of untrusted input into shell_exec().", "Strict Regex Whitelisting + Argument Escaping (escapeshellarg).", "VERIFIED (PASS)"),
        ("Directory Traversal", "CWE-22", "Uncanonicalized relative path inclusion (../).", "basename() Token Stripping + Explicit Whitelist Array.", "VERIFIED (PASS)"),
        ("Clickjacking (UI Redressing)", "CWE-1021", "Missing HTTP framing headers permitting iframe embedding.", "X-Frame-Options: DENY & CSP frame-ancestors 'none'.", "VERIFIED (PASS)"),
    ]

    tbl_master = doc.add_table(rows=len(matrix_data) + 1, cols=5)
    tbl_master.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_master.autofit = False
    tbl_master.columns[0].width = Inches(1.3)
    tbl_master.columns[1].width = Inches(1.0)
    tbl_master.columns[2].width = Inches(1.5)
    tbl_master.columns[3].width = Inches(1.7)
    tbl_master.columns[4].width = Inches(1.0)

    for i, h in enumerate(["Vulnerability", "CWE Class", "Root Cause", "Defense Mitigation", "Status"]):
        cell = tbl_master.cell(0, i)
        set_cell_background(cell, HEX_NAVY)
        set_cell_margins(cell, top=35, bottom=35, left=40, right=40)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for row_idx, data in enumerate(matrix_data, start=1):
        bg_col = HEX_LIGHT_GRAY if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(data):
            cell = tbl_master.cell(row_idx, col_idx)
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=30, bottom=30, left=40, right=40)
            set_cell_borders(cell,
                top={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
                bottom={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
                left={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
                right={'val': 'single', 'sz': '4', 'color': HEX_BORDER}
            )
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.name = "Calibri"
            r.font.size = Pt(7.5)
            if col_idx == 4:
                r.font.bold = True
                r.font.color.rgb = COLOR_GREEN
            else:
                r.font.color.rgb = COLOR_BODY

    p_after_tm = doc.add_paragraph()
    p_after_tm.paragraph_format.space_before = Pt(4)

    add_h2(doc, "10.2 Real-time Security Telemetry Engine")
    add_p(doc, "Every module in SecureJobLab communicates with api.php using JSON telemetry. When an evaluator dispatches an attack payload, the telemetry engine computes and renders:")
    add_bullet(doc, "Exploit Status: Clear diagnostic indicator stating whether the exploit succeeded or the defense held.", "• ")
    add_bullet(doc, "Executed Query / Shell Command: Exact runtime string compiled by the database or operating system.", "• ")
    add_bullet(doc, "Returned Data Records: Interactive table displaying extracted records or database error messages.", "• ")
    add_bullet(doc, "Mitigation Telemetry: Technical explanation of the security control neutralizing the attack.", "• ")

    doc.add_page_break()

    # ==============================================================================
    # CHAPTER 11: TESTING & VERIFICATION METHODOLOGY (Page 23)
    # ==============================================================================
    add_h1(doc, "Chapter 11: Testing & Verification Methodology")
    add_h2(doc, "11.1 Test Plan & Execution Strategy")
    add_p(doc, "Testing was conducted using a dual verification strategy: Automated Browser Testing in Microsoft Edge via Playwright validating HTTP responses and DOM states, paired with manual verification in web browsers verifying alert popups, UI Redressing sliders, and visual telemetry rendering.")

    add_h2(doc, "11.2 Comprehensive Verification Results Table (10 Scenarios)")
    add_p(doc, "The testing matrix evaluates each of the five vulnerabilities across both Vulnerable and Secure modes, yielding ten test scenarios:")

    test_cases = [
        ("TC-01", "SQLi (Vulnerable)", "' OR 1=1 #", "Bypasses query; returns all 5 jobs & secret notes.", "PASS"),
        ("TC-02", "SQLi (Secure)", "' OR 1=1 #", "Treated as literal string; 0 jobs returned; query intact.", "PASS"),
        ("TC-03", "XSS (Vulnerable)", "<script>alert('XSS')</script>", "Renders raw script in DOM; triggers native alert dialog.", "PASS"),
        ("TC-04", "XSS (Secure)", "<script>alert('XSS')</script>", "Encoded with htmlspecialchars(); displayed as safe text.", "PASS"),
        ("TC-05", "Cmd Inj (Vulnerable)", "127.0.0.1 & whoami", "Executes ping followed by whoami; prints server username.", "PASS"),
        ("TC-06", "Cmd Inj (Secure)", "127.0.0.1 & whoami", "Rejected by regex whitelist; system call blocked.", "PASS"),
        ("TC-07", "Traversal (Vulnerable)", "../database.sql", "Escapes folder; reads raw database schema file.", "PASS"),
        ("TC-08", "Traversal (Secure)", "../database.sql", "Tokens stripped; database.sql rejected by whitelist.", "PASS"),
        ("TC-09", "Clickjack (Vulnerable)", "Decoy Click (0% Opacity)", "Invisible iframe receives click; account deletion executed.", "PASS"),
        ("TC-10", "Clickjack (Secure)", "Decoy Click", "Framing blocked by X-Frame-Options: DENY; iframe blank.", "PASS"),
    ]

    tbl_test = doc.add_table(rows=len(test_cases) + 1, cols=5)
    tbl_test.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_test.autofit = False
    tbl_test.columns[0].width = Inches(0.8)
    tbl_test.columns[1].width = Inches(1.3)
    tbl_test.columns[2].width = Inches(1.7)
    tbl_test.columns[3].width = Inches(1.9)
    tbl_test.columns[4].width = Inches(0.8)

    for i, h in enumerate(["Test ID", "Module & Mode", "Payload / Input", "Expected Result", "Status"]):
        cell = tbl_test.cell(0, i)
        set_cell_background(cell, HEX_NAVY)
        set_cell_margins(cell, top=30, bottom=30, left=35, right=35)
        p = cell.paragraphs[0]
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(7.5)
        r.font.color.rgb = RGBColor(255, 255, 255)

    for row_idx, data in enumerate(test_cases, start=1):
        bg_col = HEX_LIGHT_GRAY if row_idx % 2 == 1 else "FFFFFF"
        for col_idx, text in enumerate(data):
            cell = tbl_test.cell(row_idx, col_idx)
            set_cell_background(cell, bg_col)
            set_cell_margins(cell, top=25, bottom=25, left=35, right=35)
            set_cell_borders(cell,
                top={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
                bottom={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
                left={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
                right={'val': 'single', 'sz': '4', 'color': HEX_BORDER}
            )
            p = cell.paragraphs[0]
            r = p.add_run(text)
            r.font.name = "Calibri"
            r.font.size = Pt(7.5)
            if col_idx == 4:
                r.font.bold = True
                r.font.color.rgb = COLOR_GREEN
            elif col_idx == 0:
                r.font.bold = True
                r.font.color.rgb = COLOR_NAVY
            else:
                r.font.color.rgb = COLOR_BODY

    p_after_tt = doc.add_paragraph()
    p_after_tt.paragraph_format.space_before = Pt(3)

    add_callout(doc, "Verification Summary: 10 out of 10 test cases passed with 100% adherence to expected behavioral specifications. Both exploitation mechanics and defensive mitigations were confirmed.", "TESTING SUMMARY", "green")

    doc.add_page_break()

    # ==============================================================================
    # CHAPTER 12: VIVA VOCE REFERENCE & SECURITY ANALYSIS (Page 24)
    # ==============================================================================
    add_h1(doc, "Chapter 12: Viva Voce Reference & Security Analysis")
    add_p(doc, "This chapter provides concise technical answers to key questions anticipated during the academic viva examination for Course 20CYS403:")

    add_h3(doc, "Q1: Why is prepared statement execution inherently immune to SQL Injection?")
    add_p(doc, "Prepared statements compile the SQL command structure beforehand into an Abstract Syntax Tree (AST). User-supplied data is transmitted separately and bound exclusively as parameter literals. The database query parser never re-interprets bound parameters as executable SQL grammar.")

    add_h3(doc, "Q2: Why does htmlspecialchars() neutralize XSS, and why are ENT_QUOTES necessary?")
    add_p(doc, "htmlspecialchars() replaces HTML meta-characters (&, <, >, \", ') with HTML entities (&amp;, &lt;, &gt;, &quot;, &#039;). The browser's DOM parser treats these as printable text rather than tag delimiters. ENT_QUOTES ensures single quotes are encoded, preventing attribute breakout attacks.")

    add_h3(doc, "Q3: What distinguishes escapeshellarg() from input whitelisting in Command Injection defense?")
    add_p(doc, "escapeshellarg() wraps arguments in single quotes and escapes existing quotes, ensuring shell parsers interpret the input as a single literal argument. Input whitelisting rejects characters entirely before any system call occurs, providing defense-in-depth.")

    add_h3(doc, "Q4: How does basename() prevent Directory Traversal attacks?")
    add_p(doc, "basename() extracts the trailing name component of a path, stripping path-traversal tokens like ../ and ..\\. In SecureJobLab, basename() is paired with an explicit whitelist array to ensure only approved document files can be accessed.")

    add_h3(doc, "Q5: How do X-Frame-Options and CSP frame-ancestors protect against Clickjacking?")
    add_p(doc, "X-Frame-Options: DENY instructs the browser to refuse rendering the target inside any frame. CSP frame-ancestors 'none' provides modern, granular defense. The browser terminates frame rendering before user interaction occurs.")

    add_h3(doc, "Q6: What is the security advantage of session-based dual-engine switching over environment flags?")
    add_p(doc, "Storing security mode in $_SESSION['appsec_mode'] allows multiple simultaneous evaluators to test vulnerable and secure paths concurrently on the same host without configuration restarts, providing immediate comparative telemetry.")

    doc.add_page_break()

    # ==============================================================================
    # CHAPTER 13 & 14: LIMITATIONS, FUTURE WORK & CONCLUSION (Page 25)
    # ==============================================================================
    add_h1(doc, "Chapter 13: Limitations & Future Enhancements")
    add_h2(doc, "13.1 Platform Limitations")
    add_bullet(doc, "Single Host Architecture: The application runs within a unified XAMPP environment; distributed cloud deployments are simulated locally.", "• ")
    add_bullet(doc, "Synchronous System Calls: Network diagnostic commands execute synchronously via PHP, introducing latency during high-timeout ping operations.", "• ")
    add_bullet(doc, "Controlled Storage: File upload and document traversal tests are restricted to local directories (lab_files and uploads/resumes).", "• ")

    add_h2(doc, "13.2 Future Enhancements")
    add_bullet(doc, "Automated CI/CD Security Gates: Integration of static application security testing (SAST) linters into automated deployment workflows.", "• ")
    add_bullet(doc, "Expanded Telemetry: Exporting security audit logs into external SIEM engines via Syslog or JSON streaming.", "• ")
    add_bullet(doc, "Containerized Deployment: Dockerizing the environment into multi-container topologies using Docker Compose.", "• ")

    add_h1(doc, "Chapter 14: Conclusion")
    add_p(doc, "The SecureJobLab platform successfully realizes a dual-engine web application security laboratory for the 20CYS403 course curriculum. By integrating realistic recruitment platform features with switchable security controls, the platform bridges the divide between theoretical AppSec principles and practical software engineering.")
    add_p(doc, "The project demonstrates that web application vulnerabilities stem from predictable software defects—unsafe string concatenation, unescaped output reflection, shell execution, uncanonicalized pathing, and missing HTTP headers. Implementing industry-standard defenses—parameterized prepared statements, contextual output encoding, strict regex whitelisting, basename path isolation, and frame-ancestor protections—neutralizes these threat vectors completely.")
    add_p(doc, "With exactly five vulnerabilities implemented, tested, and documented, SecureJobLab delivers a comprehensive laboratory demonstration suitable for academic viva evaluation.")

    doc.add_page_break()

    # ==============================================================================
    # REFERENCES & STANDARDS (Page 26)
    # ==============================================================================
    add_h1(doc, "References & Authoritative Standards")

    references_list = [
        ("[1] OWASP Foundation", "OWASP Top 10:2021 - The Ten Most Critical Web Application Security Risks", "https://owasp.org/Top10/"),
        ("[2] MITRE Corporation", "CWE-89: Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')", "https://cwe.mitre.org/data/definitions/89.html"),
        ("[3] MITRE Corporation", "CWE-79: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')", "https://cwe.mitre.org/data/definitions/79.html"),
        ("[4] MITRE Corporation", "CWE-78: Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection')", "https://cwe.mitre.org/data/definitions/78.html"),
        ("[5] MITRE Corporation", "CWE-22: Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')", "https://cwe.mitre.org/data/definitions/22.html"),
        ("[6] MITRE Corporation", "CWE-1021: Improper Restriction of Rendered UI Layers or Frames ('Clickjacking')", "https://cwe.mitre.org/data/definitions/1021.html"),
        ("[7] Mozilla Developer Network", "Content Security Policy (CSP): frame-ancestors Directive", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/frame-ancestors"),
        ("[8] Mozilla Developer Network", "X-Frame-Options Response Header Specification", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options"),
        ("[9] PHP Group", "PHP: Prepared Statements and Stored Procedures - PDO & MySQLi Manual", "https://www.php.net/manual/en/mysqli.quickstart.prepared-statements.php"),
        ("[10] National Institute of Standards and Technology (NIST)", "Special Publication 800-95: Guide to Secure Web Services", "https://csrc.nist.gov/publications/detail/sp/800-95/final"),
    ]

    for ref_id, ref_title, ref_url in references_list:
        p_r = doc.add_paragraph()
        p_r.paragraph_format.space_before = Pt(2)
        p_r.paragraph_format.space_after = Pt(2.5)
        p_r.paragraph_format.line_spacing = 1.10
        r_id = p_r.add_run(f"{ref_id} ")
        r_id.font.bold = True
        r_id.font.size = Pt(8.5)
        r_id.font.color.rgb = COLOR_NAVY
        r_t = p_r.add_run(f"{ref_title}. Available: ")
        r_t.font.size = Pt(8.5)
        r_t.font.color.rgb = COLOR_BODY
        r_u = p_r.add_run(ref_url)
        r_u.font.size = Pt(8)
        r_u.font.color.rgb = COLOR_BLUE
        r_u.font.italic = True

    doc.save(DOCX_OUT)
    print(f"Generated DOCX at: {DOCX_OUT}")

if __name__ == "__main__":
    build_report()
