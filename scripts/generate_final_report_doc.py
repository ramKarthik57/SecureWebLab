# -*- coding: utf-8 -*-
"""
generate_final_report_doc.py
Comprehensive Academic Project Report Generator for SecureJobLab.
Course Code: 20CYS403 (Web Application Security)
Output: C:\\Users\\Ram\\Desktop\\SecureWebLab\\SecureJobLab_Web_Application_Security_Report.docx
"""

import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

COLOR_NAVY = RGBColor(10, 37, 64)       # #0A2540
COLOR_SLATE = RGBColor(30, 41, 59)      # #1E293B
COLOR_BODY = RGBColor(51, 65, 85)       # #334155
COLOR_BLUE = RGBColor(2, 132, 199)      # #0284C7
COLOR_RED = RGBColor(207, 19, 34)       # #CF1322
COLOR_GREEN = RGBColor(22, 163, 74)     # #16A34A
COLOR_MUTED = RGBColor(100, 116, 139)   # #64748B

HEX_NAVY = "0A2540"
HEX_SLATE = "1E293B"
HEX_LIGHT_BLUE = "F0F9FF"
HEX_LIGHT_GRAY = "F8FAFC"
HEX_BORDER = "CBD5E1"
HEX_RED_BG = "FFF1F0"
HEX_RED_BORDER = "FFA39E"
HEX_GREEN_BG = "F6FFED"
HEX_GREEN_BORDER = "B7EB8F"

def set_cell_background(cell, hex_color):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_borders(cell, top=None, bottom=None, left=None, right=None):
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    edges = {'top': top, 'bottom': bottom, 'left': left, 'right': right}
    for edge, border_def in edges.items():
        if border_def:
            val = border_def.get('val', 'single')
            sz = border_def.get('sz', '4')
            color = border_def.get('color', 'auto')
            el = parse_xml(f'<w:{edge} {nsdecls("w")} w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>')
            tcBorders.append(el)
        else:
            el = parse_xml(f'<w:{edge} {nsdecls("w")} w:val="none"/>')
            tcBorders.append(el)
    tcPr.append(tcBorders)

def add_header_footer(doc):
    for s in doc.sections:
        s.top_margin = Inches(0.85)
        s.bottom_margin = Inches(0.85)
        s.left_margin = Inches(0.85)
        s.right_margin = Inches(0.85)

        header = s.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Course: 20CYS403 | Web Application Security Laboratory Report | SecureJobLab")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = COLOR_MUTED

        footer = s.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("SecureJobLab Platform — Exactly 5 CWE Security Modules | Page ")
        frun.font.name = "Calibri"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = COLOR_MUTED
        fldSimple = OxmlElement('w:fldSimple')
        fldSimple.set(qn('w:instr'), 'PAGE')
        fp._p.append(fldSimple)

def add_h1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(15)
    run.font.bold = True
    run.font.color.rgb = COLOR_NAVY
    return p

def add_h2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(11)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(12.5)
    run.font.bold = True
    run.font.color.rgb = COLOR_SLATE
    return p

def add_h3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(7)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = COLOR_BLUE
    return p

def add_p(doc, text, bold_prefix=None, space_after=3):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(10)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_SLATE
    r_body = p.add_run(text)
    r_body.font.name = "Calibri"
    r_body.font.size = Pt(10)
    r_body.font.color.rgb = COLOR_BODY
    return p

def add_bullet(doc, text, bold_prefix=None):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.12
    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        r_pre.font.name = "Calibri"
        r_pre.font.size = Pt(9.5)
        r_pre.font.bold = True
        r_pre.font.color.rgb = COLOR_SLATE
    r_body = p.add_run(text)
    r_body.font.name = "Calibri"
    r_body.font.size = Pt(9.5)
    r_body.font.color.rgb = COLOR_BODY
    return p

def add_callout(doc, text, title="SECURITY SUMMARY", ctype="blue"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)
    cell = tbl.cell(0, 0)
    set_cell_margins(cell, top=70, bottom=70, left=120, right=120)

    if ctype == "red":
        bg_col, border_col, title_col, bar_col = HEX_RED_BG, HEX_RED_BORDER, COLOR_RED, "CF1322"
    elif ctype == "green":
        bg_col, border_col, title_col, bar_col = HEX_GREEN_BG, HEX_GREEN_BORDER, COLOR_GREEN, "16A34A"
    else:
        bg_col, border_col, title_col, bar_col = HEX_LIGHT_BLUE, "BAE6FD", COLOR_BLUE, "0284C7"

    set_cell_background(cell, bg_col)
    set_cell_borders(cell,
        top={'val': 'single', 'sz': '4', 'color': border_col},
        bottom={'val': 'single', 'sz': '4', 'color': border_col},
        right={'val': 'single', 'sz': '4', 'color': border_col},
        left={'val': 'single', 'sz': '24', 'color': bar_col}
    )

    cp = cell.paragraphs[0]
    cp.paragraph_format.space_before = Pt(0)
    cp.paragraph_format.space_after = Pt(0)
    rt = cp.add_run(f"[{title}] ")
    rt.font.name = "Calibri"
    rt.font.size = Pt(9.5)
    rt.font.bold = True
    rt.font.color.rgb = title_col

    rb = cp.add_run(text)
    rb.font.name = "Calibri"
    rb.font.size = Pt(9)
    rb.font.color.rgb = COLOR_BODY

    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(3)

def add_code_block(doc, code_str, caption=None):
    if caption:
        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.space_before = Pt(3)
        p_cap.paragraph_format.space_after = Pt(1)
        rc = p_cap.add_run(f"Listing: {caption}")
        rc.font.name = "Calibri"
        rc.font.size = Pt(8.5)
        rc.font.bold = True
        rc.font.color.rgb = COLOR_MUTED

    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)
    cell = tbl.cell(0, 0)
    set_cell_margins(cell, top=50, bottom=50, left=90, right=90)
    set_cell_background(cell, HEX_LIGHT_GRAY)
    set_cell_borders(cell,
        top={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
        bottom={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
        right={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
        left={'val': 'single', 'sz': '18', 'color': "0284C7"}
    )
    cp = cell.paragraphs[0]
    cp.paragraph_format.space_before = Pt(0)
    cp.paragraph_format.space_after = Pt(0)
    cp.paragraph_format.line_spacing = 1.05
    run = cp.add_run(code_str)
    run.font.name = "Consolas"
    run.font.size = Pt(8)
    run.font.color.rgb = RGBColor(30, 41, 59)

    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(3)

def add_dual_code_comparison(doc, vuln_code, sec_code, vuln_title="Vulnerable Code (Unsafe)", sec_title="Secure Mitigated Code (Defended)"):
    tbl = doc.add_table(rows=2, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(3.2)
    tbl.columns[1].width = Inches(3.2)

    c0, c1 = tbl.cell(0, 0), tbl.cell(0, 1)
    set_cell_background(c0, HEX_RED_BG)
    set_cell_background(c1, HEX_GREEN_BG)
    set_cell_margins(c0, top=40, bottom=40, left=60, right=60)
    set_cell_margins(c1, top=40, bottom=40, left=60, right=60)
    set_cell_borders(c0,
        top={'val': 'single', 'sz': '4', 'color': HEX_RED_BORDER},
        bottom={'val': 'single', 'sz': '4', 'color': HEX_RED_BORDER},
        left={'val': 'single', 'sz': '12', 'color': "CF1322"},
        right={'val': 'single', 'sz': '4', 'color': HEX_RED_BORDER}
    )
    set_cell_borders(c1,
        top={'val': 'single', 'sz': '4', 'color': HEX_GREEN_BORDER},
        bottom={'val': 'single', 'sz': '4', 'color': HEX_GREEN_BORDER},
        left={'val': 'single', 'sz': '12', 'color': "16A34A"},
        right={'val': 'single', 'sz': '4', 'color': HEX_GREEN_BORDER}
    )

    p0 = c0.paragraphs[0]
    p0.paragraph_format.space_before = Pt(0)
    p0.paragraph_format.space_after = Pt(0)
    r0 = p0.add_run(f"🔴 {vuln_title}")
    r0.font.name = "Calibri"
    r0.font.size = Pt(8.5)
    r0.font.bold = True
    r0.font.color.rgb = COLOR_RED

    p1 = c1.paragraphs[0]
    p1.paragraph_format.space_before = Pt(0)
    p1.paragraph_format.space_after = Pt(0)
    r1 = p1.add_run(f"🟢 {sec_title}")
    r1.font.name = "Calibri"
    r1.font.size = Pt(8.5)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_GREEN

    cb0, cb1 = tbl.cell(1, 0), tbl.cell(1, 1)
    set_cell_background(cb0, HEX_LIGHT_GRAY)
    set_cell_background(cb1, HEX_LIGHT_GRAY)
    set_cell_margins(cb0, top=50, bottom=50, left=60, right=60)
    set_cell_margins(cb1, top=50, bottom=50, left=60, right=60)
    set_cell_borders(cb0,
        top={'val': 'none'},
        bottom={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
        left={'val': 'single', 'sz': '12', 'color': "CF1322"},
        right={'val': 'single', 'sz': '4', 'color': HEX_BORDER}
    )
    set_cell_borders(cb1,
        top={'val': 'none'},
        bottom={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
        left={'val': 'single', 'sz': '12', 'color': "16A34A"},
        right={'val': 'single', 'sz': '4', 'color': HEX_BORDER}
    )

    pc0 = cb0.paragraphs[0]
    pc0.paragraph_format.space_before = Pt(0)
    pc0.paragraph_format.space_after = Pt(0)
    pc0.paragraph_format.line_spacing = 1.05
    rc0 = pc0.add_run(vuln_code)
    rc0.font.name = "Consolas"
    rc0.font.size = Pt(7.5)
    rc0.font.color.rgb = COLOR_SLATE

    pc1 = cb1.paragraphs[0]
    pc1.paragraph_format.space_before = Pt(0)
    pc1.paragraph_format.space_after = Pt(0)
    pc1.paragraph_format.line_spacing = 1.05
    rc1 = pc1.add_run(sec_code)
    rc1.font.name = "Consolas"
    rc1.font.size = Pt(7.5)
    rc1.font.color.rgb = COLOR_SLATE

    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(3)

def add_image_box(doc, img_path, caption, width=Inches(6.2)):
    if not os.path.exists(img_path):
        print(f"Warning: image path does not exist: {img_path}")
        return

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(5)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    p.add_run().add_picture(img_path, width=width)

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(2)
    p_cap.paragraph_format.space_after = Pt(5)
    rc = p_cap.add_run(f"Figure: {caption}")
    rc.font.name = "Calibri"
    rc.font.size = Pt(8.5)
    rc.font.italic = True
    rc.font.color.rgb = COLOR_MUTED

def add_dual_image_comparison(doc, img_vuln, img_sec, cap_vuln, cap_sec):
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(3.2)
    tbl.columns[1].width = Inches(3.2)

    c0, c1 = tbl.cell(0, 0), tbl.cell(0, 1)
    set_cell_margins(c0, top=30, bottom=30, left=30, right=30)
    set_cell_margins(c1, top=30, bottom=30, left=30, right=30)

    if os.path.exists(img_vuln):
        p0 = c0.paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p0.add_run().add_picture(img_vuln, width=Inches(3.1))
        p0_cap = c0.add_paragraph()
        p0_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p0_cap.add_run(f"🔴 {cap_vuln}")
        r.font.name = "Calibri"
        r.font.size = Pt(8)
        r.font.bold = True
        r.font.color.rgb = COLOR_RED

    if os.path.exists(img_sec):
        p1 = c1.paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p1.add_run().add_picture(img_sec, width=Inches(3.1))
        p1_cap = c1.add_paragraph()
        p1_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p1_cap.add_run(f"🟢 {cap_sec}")
        r.font.name = "Calibri"
        r.font.size = Pt(8)
        r.font.bold = True
        r.font.color.rgb = COLOR_GREEN

    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(0)
    p_after.paragraph_format.space_after = Pt(3)

print("Starting complete academic document generation...")

doc = Document()
add_header_footer(doc)

# Paths to assets
base_dir = r"C:\Users\Ram\Desktop\SecureWebLab"
brain_dir = r"C:\Users\Ram\.gemini\antigravity\brain\c8b0a563-d19e-4bda-8029-b51cdb82bfb9"
lab5_dir = os.path.join(brain_dir, "lab_5vuln_screenshots")

img_arch = os.path.join(base_dir, "diagram_architecture.png")
img_dual = os.path.join(base_dir, "diagram_dual_engine.png")
img_db = os.path.join(base_dir, "diagram_db_schema.png")

img_login = os.path.join(brain_dir, "screenshot_login_verified.png")
img_index = os.path.join(brain_dir, "screenshot_index_verified.png")
img_apps = os.path.join(brain_dir, "screenshot_applications_verified.png")

img_m1_v = os.path.join(lab5_dir, "mod1_vulnerable.png")
img_m1_s = os.path.join(lab5_dir, "mod1_secure.png")
img_m2_v = os.path.join(lab5_dir, "mod2_vulnerable.png")
img_m2_s = os.path.join(lab5_dir, "mod2_secure.png")
img_m3_v = os.path.join(lab5_dir, "mod3_vulnerable.png")
img_m3_s = os.path.join(lab5_dir, "mod3_secure.png")
img_m4_v = os.path.join(lab5_dir, "mod4_vulnerable.png")
img_m4_s = os.path.join(lab5_dir, "mod4_secure.png")
img_m5_100 = os.path.join(lab5_dir, "clickjack_harmful_100pct.png")
img_m5_30 = os.path.join(lab5_dir, "clickjack_harmful_30pct.png")
img_m5_trig = os.path.join(lab5_dir, "clickjack_harmful_triggered.png")
img_m5_s = os.path.join(lab5_dir, "mod5_secure.png")

# ==============================================================================
# COVER PAGE
# ==============================================================================
p_top_sp = doc.add_paragraph()
p_top_sp.paragraph_format.space_before = Pt(20)

p_inst = doc.add_paragraph()
p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p_inst.add_run("DEPARTMENT OF CYBERSECURITY & COMPUTER ENGINEERING\n")
r.font.name = "Calibri"
r.font.size = Pt(13)
r.font.bold = True
r.font.color.rgb = COLOR_NAVY
r2 = p_inst.add_run("20CYS403: WEB APPLICATION SECURITY LABORATORY\nACADEMIC PROJECT REPORT")
r2.font.name = "Calibri"
r2.font.size = Pt(11)
r2.font.bold = True
r2.font.color.rgb = COLOR_BLUE

p_rule = doc.add_paragraph()
p_rule.alignment = WD_ALIGN_PARAGRAPH.CENTER
r_rule = p_rule.add_run("―" * 48)
r_rule.font.color.rgb = COLOR_BLUE

# Title Box
tbl_t = doc.add_table(rows=1, cols=1)
tbl_t.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_t.autofit = False
tbl_t.columns[0].width = Inches(6.5)
c_t = tbl_t.cell(0, 0)
set_cell_background(c_t, HEX_LIGHT_BLUE)
set_cell_margins(c_t, top=140, bottom=140, left=160, right=160)
set_cell_borders(c_t,
    top={'val': 'single', 'sz': '8', 'color': '0284C7'},
    bottom={'val': 'single', 'sz': '8', 'color': '0284C7'},
    left={'val': 'single', 'sz': '24', 'color': '0A2540'},
    right={'val': 'single', 'sz': '8', 'color': '0284C7'}
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
rt2.font.size = Pt(11.5)
rt2.font.italic = True
rt2.font.color.rgb = COLOR_SLATE

p_sp = doc.add_paragraph()
p_sp.paragraph_format.space_before = Pt(30)

# Metadata Block
tbl_meta = doc.add_table(rows=4, cols=2)
tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_meta.autofit = False
tbl_meta.columns[0].width = Inches(3.2)
tbl_meta.columns[1].width = Inches(3.3)

meta_data = [
    ("Candidate / Student Persona:", "Ram Karthik (Cybersecurity Specialist)"),
    ("Course Name & Code:", "Web Application Security (20CYS403)"),
    ("Evaluation Scope:", "5 Core CWE Modules (SQLi, XSS, Cmd Injection, Traversal, Clickjacking)"),
    ("Platform Architecture:", "Apache 2.4, PHP 8.x, MySQL 10.4 (MariaDB), AJAX, Bootstrap 5"),
]

for idx, (label, val) in enumerate(meta_data):
    cell_l = tbl_meta.cell(idx, 0)
    cell_r = tbl_meta.cell(idx, 1)
    set_cell_margins(cell_l, top=40, bottom=40, left=60, right=60)
    set_cell_margins(cell_r, top=40, bottom=40, left=60, right=60)
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
p_sp2.paragraph_format.space_before = Pt(40)

p_foot = doc.add_paragraph()
p_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER
rf = p_foot.add_run("Academic Year 2026 | Comprehensive Laboratory & Viva Demonstration Package")
rf.font.name = "Calibri"
rf.font.size = Pt(9.5)
rf.font.color.rgb = COLOR_MUTED

doc.add_page_break()

# ==============================================================================
# CERTIFICATE & DECLARATION
# ==============================================================================
add_h1(doc, "Certificate of Originality & Project Declaration")
add_callout(doc, "This project is prepared strictly for the academic course 20CYS403 (Web Application Security). All vulnerable and secure implementations are isolated on local infrastructure (localhost) using simulated candidate records and controlled lab files.", "ACADEMIC DECLARATION", "blue")

add_p(doc, "This is to certify that the project report entitled \"SecureJobLab: Job Recruitment Vulnerability Demonstration & Defense Platform\" submitted by Ram Karthik in partial fulfillment of the academic requirements for the course 20CYS403 Web Application Security represents authentic, original work conducted under laboratory supervision.")
add_p(doc, "The laboratory implementation rigorously implements, analyzes, and demonstrates exactly five web application security vulnerabilities classified under the Common Weakness Enumeration (CWE) framework:")
add_bullet(doc, "SQL Injection (SQLi) — CWE-89: Direct query concatenation versus Parameterized Prepared Statements.", "1. ")
add_bullet(doc, "Cross-Site Scripting (XSS) — CWE-79: Reflected execution versus Contextual HTML Entity Encoding.", "2. ")
add_bullet(doc, "OS Command Injection — CWE-78: Unsanitized shell concatenation versus Strict Regex Whitelisting and Argument Escaping.", "3. ")
add_bullet(doc, "Directory / Path Traversal — CWE-22: Arbitrary file inclusion versus Basename Whitelisting and Canonical Boundary Isolation.", "4. ")
add_bullet(doc, "Clickjacking (UI Redressing) — CWE-1021: Framed destructive actions versus HTTP Framing Defense Headers (X-Frame-Options and CSP).", "5. ")

add_p(doc, "I hereby declare that this report has been authored with technical diligence, that no external or unapproved vulnerability modules have been included, and that all code snippets, telemetry graphs, and screenshots accurately reflect the live execution behavior of the SecureJobLab system.")

p_sig = doc.add_paragraph()
p_sig.paragraph_format.space_before = Pt(30)
r_sig1 = p_sig.add_run("Candidate Signature: ___________________________          Date: October 6, 2026\n")
r_sig1.font.bold = True
r_sig1.font.color.rgb = COLOR_SLATE
r_sig2 = p_sig.add_run("Name: Ram Karthik (AppSec Specialist / Candidate Persona)\nCourse Code: 20CYS403 — Web Application Security")
r_sig2.font.color.rgb = COLOR_BODY

doc.add_page_break()

# ==============================================================================
# ACKNOWLEDGEMENTS & ABSTRACT
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
# TABLE OF CONTENTS & LIST OF TABLES/FIGURES
# ==============================================================================
add_h1(doc, "Table of Contents")

toc_items = [
    ("Chapter 1: Introduction, Problem Statement & Objectives", "1"),
    ("    1.1 Context & Background", "1"),
    ("    1.2 Problem Statement", "1"),
    ("    1.3 Project Objectives", "2"),
    ("    1.4 Strict 5-Vulnerability Project Scope", "2"),
    ("Chapter 2: System Architecture & Dual-Engine Design", "3"),
    ("    2.1 Four-Tier Architecture Model", "3"),
    ("    2.2 The Dual-Engine Security Execution Model", "4"),
    ("    2.3 Request Lifecycle & State Management", "5"),
    ("Chapter 3: Technology Stack & Database Architecture", "6"),
    ("    3.1 Technology Stack Specification", "6"),
    ("    3.2 Relational Database Design & Schema Dictionary", "7"),
    ("Chapter 4: Application Functional Modules", "8"),
    ("    4.1 Authentication & Role-Based Access Control", "8"),
    ("    4.2 Instant Job Board & Filtering Engine", "9"),
    ("    4.3 Candidate Application Pipeline & Document Viewer", "9"),
    ("    4.4 Network Latency & Diagnostic Utilities", "10"),
    ("Chapter 5: Vulnerability 1 — SQL Injection (SQLi) [CWE-89]", "11"),
    ("    5.1 Vulnerability Overview & Threat Dynamics", "11"),
    ("    5.2 Vulnerable Implementation & Attack Execution", "11"),
    ("    5.3 Secure Mitigation & Parameterized Prepared Statements", "13"),
    ("Chapter 6: Vulnerability 2 — Cross-Site Scripting (XSS) [CWE-79]", "14"),
    ("    6.1 Vulnerability Overview & Threat Dynamics", "14"),
    ("    6.2 Vulnerable Implementation & Live Script Execution", "14"),
    ("    6.3 Secure Mitigation & Contextual Output Encoding", "16"),
    ("Chapter 7: Vulnerability 3 — OS Command Injection [CWE-78]", "17"),
    ("    7.1 Vulnerability Overview & Threat Dynamics", "17"),
    ("    7.2 Vulnerable Implementation & Shell Chaining", "17"),
    ("    7.3 Secure Mitigation & Strict Whitelisting", "19"),
    ("Chapter 8: Vulnerability 4 — Directory / Path Traversal [CWE-22]", "20"),
    ("    8.1 Vulnerability Overview & Threat Dynamics", "20"),
    ("    8.2 Vulnerable Implementation & Path Climbing", "20"),
    ("    8.3 Secure Mitigation & Canonical Boundary Defense", "22"),
    ("Chapter 9: Vulnerability 5 — Clickjacking (UI Redressing) [CWE-1021]", "23"),
    ("    9.1 Vulnerability Overview & High-Impact Scenario", "23"),
    ("    9.2 Interactive UI Redressing Sandbox with Opacity Slider", "23"),
    ("    9.3 Secure Mitigation & HTTP Framing Protection Headers", "25"),
    ("Chapter 10: Comparative Defense Matrix & Telemetry Analysis", "26"),
    ("    10.1 Master Vulnerability Comparison Matrix", "26"),
    ("    10.2 Real-time Security Telemetry Engine", "27"),
    ("Chapter 11: Testing & Verification Methodology", "28"),
    ("    11.1 Test Plan & Execution Strategy", "28"),
    ("    11.2 Comprehensive Verification Results Table", "29"),
    ("Chapter 12: Viva Voce Reference & Security Analysis", "30"),
    ("Chapter 13: Limitations & Future Enhancements", "31"),
    ("Chapter 14: Conclusion", "32"),
    ("References & Authoritative Standards", "33"),
]

for title, page_no in toc_items:
    p_t = doc.add_paragraph()
    p_t.paragraph_format.space_before = Pt(1)
    p_t.paragraph_format.space_after = Pt(1)
    is_ch = title.startswith("Chapter") or title.startswith("References")
    r1 = p_t.add_run(title)
    r1.font.name = "Calibri"
    r1.font.size = Pt(9.5 if not is_ch else 10)
    r1.font.bold = is_ch
    r1.font.color.rgb = COLOR_NAVY if is_ch else COLOR_SLATE

    # Dot leaders
    dots_count = max(5, 75 - len(title))
    r_dot = p_t.add_run(" " + "." * dots_count + " ")
    r_dot.font.color.rgb = COLOR_MUTED
    r_dot.font.size = Pt(8.5)

    r2 = p_t.add_run(page_no)
    r2.font.name = "Calibri"
    r2.font.size = Pt(9.5 if not is_ch else 10)
    r2.font.bold = is_ch
    r2.font.color.rgb = COLOR_NAVY if is_ch else COLOR_SLATE

doc.add_page_break()

# ==============================================================================
# LIST OF FIGURES & TABLES & ABBREVIATIONS
# ==============================================================================
add_h1(doc, "List of Figures & Tables")

figures = [
    ("Figure 1", "SecureJobLab Four-Tier System Architecture & Interaction Flow"),
    ("Figure 2", "Comparative Dual-Engine Execution Pipeline (Vulnerable vs. Secure)"),
    ("Figure 3", "Relational Database Schema & Data Dictionary (securejoblab)"),
    ("Figure 4", "SQL Injection Demonstration: Insecure Extraction vs. Parameterized Defense"),
    ("Figure 5", "Reflected XSS Demonstration: Live Alert Execution vs. Encoded Rendering"),
    ("Figure 6", "OS Command Injection: Unsanitized Chaining vs. Regex Whitelist Interception"),
    ("Figure 7", "Directory Traversal: Sensitive File Extraction vs. Whitelist Denial"),
    ("Figure 8", "Clickjacking UI Redressing Sandbox at 100% Opacity (Harmful Button Revealed)"),
    ("Figure 9", "Clickjacking UI Redressing Sandbox at 30% Opacity (Ghost Alignment Mode)"),
    ("Figure 10", "Clickjacking Exploit Triggered: Unauthorized Account Deletion Execution"),
    ("Figure 11", "Clickjacking Defended: Browser Iframe Blocking via X-Frame-Options: DENY"),
    ("Figure 12", "SecureJobLab Authentication Screen (Candidate & Admin RBAC)"),
    ("Figure 13", "Recruitment Portal Interface: Verified Cybersecurity Openings"),
    ("Figure 14", "Candidate Application Pipeline & Local Resume Storage Dashboard"),
]

add_h2(doc, "List of Figures")
for fig_id, fig_desc in figures:
    p_f = doc.add_paragraph()
    p_f.paragraph_format.space_before = Pt(1)
    p_f.paragraph_format.space_after = Pt(2)
    r = p_f.add_run(f"{fig_id}: ")
    r.font.bold = True
    r.font.color.rgb = COLOR_SLATE
    r2 = p_f.add_run(fig_desc)
    r2.font.color.rgb = COLOR_BODY

tables = [
    ("Table 1", "Core Technology Stack & Deployment Dependencies"),
    ("Table 2", "Database Entity-Relationship Schema & Table Specifications"),
    ("Table 3", "Master 5-Vulnerability Security Comparison & Defense Matrix"),
    ("Table 4", "Comprehensive Verification & Test Results Matrix (10 Scenarios)"),
]

add_h2(doc, "List of Tables")
for tbl_id, tbl_desc in tables:
    p_t = doc.add_paragraph()
    p_t.paragraph_format.space_before = Pt(1)
    p_t.paragraph_format.space_after = Pt(2)
    r = p_t.add_run(f"{tbl_id}: ")
    r.font.bold = True
    r.font.color.rgb = COLOR_SLATE
    r2 = p_t.add_run(tbl_desc)
    r2.font.color.rgb = COLOR_BODY

add_h2(doc, "Abbreviations & Security Terminology")
abbrevs = [
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

for abbr, full in abbrevs:
    p_a = doc.add_paragraph()
    p_a.paragraph_format.space_before = Pt(1)
    p_a.paragraph_format.space_after = Pt(1)
    ra = p_a.add_run(f"{abbr}: ")
    ra.font.bold = True
    ra.font.color.rgb = COLOR_BLUE
    rf = p_a.add_run(full)
    rf.font.color.rgb = COLOR_BODY

doc.add_page_break()

# ==============================================================================
# CHAPTER 1: INTRODUCTION, PROBLEM STATEMENT & SCOPE
# ==============================================================================
add_h1(doc, "Chapter 1: Introduction, Problem Statement & Objectives")

add_h2(doc, "1.1 Context & Background")
add_p(doc, "Web applications represent the predominant attack surface in modern enterprise infrastructure. High-throughput platforms handling human capital, financial transactions, and privileged communications are targeted relentlessly by automated scanners and sophisticated threat actors. In academic cybersecurity curricula, students frequently encounter theoretical definitions of software vulnerabilities without experiencing the contextual nuances of how vulnerabilities manifest within functional software features, or how defensive controls alter execution mechanics.")
add_p(doc, "To bridge this pedagogical gap, SecureJobLab was conceived as an interactive, dual-engine recruitment portal. The application simulates an enterprise human-resources technology platform—Jobpilot—complete with role-based sign-in, instant job filtering, application submission with resume handling, and network diagnostics. Crucially, the entire architecture is wired to a global security switcher that allows students, researchers, and academic evaluators to observe the exact technical contrast between vulnerable software implementations and their corresponding secure mitigations.")

add_h2(doc, "1.2 Problem Statement")
add_p(doc, "Software development practices routinely suffer from systemic vulnerabilities introduced by insufficient input validation, dynamic query interpolation, unescaped system calls, and omitted HTTP security headers. Traditional training environments suffer from several deficiencies:")
add_bullet(doc, "Artificial Environments: Vulnerabilities are isolated inside disconnected forms that bear no resemblance to commercial web workflows.", "• ")
add_bullet(doc, "Omission of Mitigations: Labs frequently demonstrate how an exploit functions without providing a functional, verified defense implementation in the same codebase.", "• ")
add_bullet(doc, "Scope Overload: Comprehensive vulnerability scanners introduce dozens of overlapping flaws, confusing evaluators during viva presentations.", "• ")
add_bullet(doc, "Static Telemetry: Traditional labs provide static text outputs rather than live database query inspection, execution timers, and DOM structure telemetry.", "• ")

add_h2(doc, "1.3 Project Objectives")
add_p(doc, "The primary objectives of the SecureJobLab platform are established as follows:")
add_bullet(doc, "Design and construct an enterprise-grade job recruitment platform operating with realistic workflows.", "1. ")
add_bullet(doc, "Implement a switchable Dual-Engine Architecture enabling instant toggling between Vulnerable Mode and Secure Mitigated Mode.", "2. ")
add_bullet(doc, "Integrate live, structured Security Telemetry providing database query logs, resolved filesystem paths, OS command outputs, and HTTP header analyses.", "3. ")
add_bullet(doc, "Incorporate native browser interactivity, such as real-time alert dialogs upon explicit test execution and an interactive Opacity Slider sandbox for UI Redressing.", "4. ")
add_bullet(doc, "Maintain a consolidated codebase strictly adhering to six core files, ensuring deterministic, error-free deployment on standard XAMPP environments.", "5. ")

add_h2(doc, "1.4 Strict Project Scope: Exactly Five Vulnerabilities")
add_callout(doc, "The scope of SecureJobLab is strictly delimited to five core vulnerabilities defined in the 20CYS403 course curriculum. No external, secondary, or deprecated modules (such as CSRF, SSRF, CORS, broken authentication, or insecure file upload) are implemented. This absolute delimitation ensures deep, rigorous technical coverage suitable for academic evaluation.", "SCOPE ENFORCEMENT", "blue")

add_p(doc, "The five vulnerabilities implemented and verified in this report are:")
add_bullet(doc, "SQL Injection (SQLi) — CWE-89: Manipulation of SQL query grammar through unsanitized user input.", "1. ")
add_bullet(doc, "Cross-Site Scripting (XSS) — CWE-79: Injection of malicious scripts executed within the victim's browser context.", "2. ")
add_bullet(doc, "OS Command Injection — CWE-78: Injection of shell metacharacters resulting in unauthorized host command execution.", "3. ")
add_bullet(doc, "Directory / Path Traversal — CWE-22: Access to files outside the designated webroot through uncanonicalized path traversal tokens.", "4. ")
add_bullet(doc, "Clickjacking (UI Redressing) — CWE-1021: Hijacking authenticated user clicks by overlaying transparent iframes over destructive endpoints.", "5. ")

doc.add_page_break()

# ==============================================================================
# CHAPTER 2: SYSTEM ARCHITECTURE & DUAL-ENGINE DESIGN
# ==============================================================================
add_h1(doc, "Chapter 2: System Architecture & Dual-Engine Design")

add_h2(doc, "2.1 Four-Tier Architecture Model")
add_p(doc, "SecureJobLab is structured as a decoupled four-tier web architecture designed for modularity, low latency, and deterministic evaluation. The system separates user interaction, security state management, API request dispatching, and system resources.")

add_image_box(doc, img_arch, "SecureJobLab Four-Tier System Architecture & Interaction Flow", width=Inches(6.2))

add_p(doc, "The four architectural tiers operate as follows:")
add_bullet(doc, "Presentation Tier: Developed in HTML5, CSS3, and JavaScript utilizing the Jobpilot design system. Provides the job search interface, candidate dashboard, authentication screens, and AppSec testing telemetry panels.", "1. ")
add_bullet(doc, "Security Controller Tier: Governed by the global session state ($_SESSION['appsec_mode']). Coordinates between the Vulnerable engine and the Secure engine across both portal features and lab testing endpoints.", "2. ")
add_bullet(doc, "Application & API Tier: Implemented in api.php and index.php. Acts as the centralized REST/AJAX router handling job CRUD operations, application submissions, and the five vulnerability testing routines.", "3. ")
add_bullet(doc, "Data & Subsystem Tier: Encapsulates the MySQL relational database (securejoblab), the local filesystem (lab_files and uploads/resumes), and the host operating system shell subsystem.", "4. ")

add_h2(doc, "2.2 The Dual-Engine Security Execution Model")
add_p(doc, "The foundational innovation of SecureJobLab is its Dual-Engine Execution Pipeline. Rather than requiring evaluators to modify configuration files or restart services, the entire application toggles its defensive posture via an interactive navbar switch.")

add_image_box(doc, img_dual, "Comparative Dual-Engine Execution Pipeline (Vulnerable vs. Secure Mitigated)", width=Inches(6.2))

add_p(doc, "As illustrated in Figure 2, identical attack payloads traverse completely different execution paths depending on the active security mode:")
add_bullet(doc, "🔴 Vulnerable Mode: Untrusted input flows without validation or escaping directly into dangerous execution sinks (mysqli_query(), browser DOM, shell_exec(), file_get_contents(), and unheadered iframe embedding). The attack succeeds, and exploit telemetry is recorded.", "• ")
add_bullet(doc, "🟢 Secure Mode: The payload is intercepted by defensive mechanisms (parameterized query compilation, contextual htmlspecialchars() encoding, strict regex whitelisting, basename() isolation, and X-Frame-Options: DENY headers). The attack is completely neutralized, and defensive verification telemetry is recorded.", "• ")

doc.add_page_break()

# ==============================================================================
# CHAPTER 3: TECHNOLOGY STACK & DATABASE ARCHITECTURE
# ==============================================================================
add_h1(doc, "Chapter 3: Technology Stack & Database Architecture")

add_h2(doc, "3.1 Technology Stack Specification")
add_p(doc, "To guarantee deterministic behavior, rapid viva demonstrations, and frictionless portability on standard university laboratory machines, SecureJobLab is built on an enterprise open-source technology stack:")

# Table 1: Tech Stack
tbl_tech = doc.add_table(rows=6, cols=3)
tbl_tech.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_tech.autofit = False
tbl_tech.columns[0].width = Inches(1.8)
tbl_tech.columns[1].width = Inches(1.8)
tbl_tech.columns[2].width = Inches(2.9)

headers_tech = ["Component Layer", "Technology Selected", "Role in SecureJobLab"]
for i, h in enumerate(headers_tech):
    cell = tbl_tech.cell(0, i)
    set_cell_background(cell, HEX_NAVY)
    set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
    p = cell.paragraphs[0]
    r = p.add_run(h)
    r.font.bold = True
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor(255, 255, 255)

tech_data = [
    ("Web Server", "Apache HTTP Server 2.4", "Listens on port 80; manages HTTP requests, header emission, and PHP handler execution."),
    ("Database Engine", "MySQL 10.4 (MariaDB)", "Listens on port 3306; manages relational tables, indexes, and parameterized query execution."),
    ("Server Language", "PHP 8.2+ (OOP & Procedural)", "Executes backend routing, session state control, raw string parsing, and secure sanitization."),
    ("Frontend UI", "HTML5, CSS3, Bootstrap 5.3", "Jobpilot SaaS theme, interactive telemetry cards, modals, and responsive layout."),
    ("Asynchronous Comms", "Vanilla JavaScript (Fetch API)", "Non-blocking AJAX request dispatching, DOM updates, and live script execution handling."),
]

for row_idx, data in enumerate(tech_data, start=1):
    bg_col = HEX_LIGHT_GRAY if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, text in enumerate(data):
        cell = tbl_tech.cell(row_idx, col_idx)
        set_cell_background(cell, bg_col)
        set_cell_margins(cell, top=50, bottom=50, left=70, right=70)
        set_cell_borders(cell,
            top={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
            bottom={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
            left={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
            right={'val': 'single', 'sz': '4', 'color': HEX_BORDER}
        )
        p = cell.paragraphs[0]
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(9)
        r.font.color.rgb = COLOR_BODY

p_after_t1 = doc.add_paragraph()
p_after_t1.paragraph_format.space_before = Pt(4)

add_h2(doc, "3.2 Relational Database Schema Design")
add_p(doc, "The database schema for securejoblab is engineered with UTF-8 (utf8mb4) character encoding, ensuring pristine rendering of international currency symbols (such as the Indian Rupee ₹) without mojibake corruption. The schema consists of four relational tables:")

add_image_box(doc, img_db, "Relational Database Schema & Data Dictionary (securejoblab)", width=Inches(6.2))

# Table 2: Schema Dictionary
tbl_schema = doc.add_table(rows=5, cols=4)
tbl_schema.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_schema.autofit = False
tbl_schema.columns[0].width = Inches(1.3)
tbl_schema.columns[1].width = Inches(1.4)
tbl_schema.columns[2].width = Inches(1.8)
tbl_schema.columns[3].width = Inches(2.0)

headers_sch = ["Table Name", "Primary Key", "Key Attributes", "Security / Functional Role"]
for i, h in enumerate(headers_sch):
    cell = tbl_schema.cell(0, i)
    set_cell_background(cell, HEX_NAVY)
    set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
    p = cell.paragraphs[0]
    r = p.add_run(h)
    r.font.bold = True
    r.font.size = Pt(9.5)
    r.font.color.rgb = RGBColor(255, 255, 255)

sch_data = [
    ("users", "id (INT)", "username, password, full_name, role", "Stores authentication credentials; password verification and RBAC roles."),
    ("jobs", "id (INT)", "title, company, location, salary, secret_notes", "Target for SQLi; secret_notes contains confidential compensation bands."),
    ("applications", "id (INT)", "job_title, applicant_name, resume_file, status", "Tracks submissions for Ram Karthik; links to uploaded resume documents."),
    ("feedback", "id (INT)", "author, comment, created_at", "Stores recruiter feedback; used for output reflection testing."),
]

for row_idx, data in enumerate(sch_data, start=1):
    bg_col = HEX_LIGHT_GRAY if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, text in enumerate(data):
        cell = tbl_schema.cell(row_idx, col_idx)
        set_cell_background(cell, bg_col)
        set_cell_margins(cell, top=50, bottom=50, left=70, right=70)
        set_cell_borders(cell,
            top={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
            bottom={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
            left={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
            right={'val': 'single', 'sz': '4', 'color': HEX_BORDER}
        )
        p = cell.paragraphs[0]
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(9)
        r.font.color.rgb = COLOR_BODY

doc.add_page_break()

# ==============================================================================
# CHAPTER 4: CORE FUNCTIONAL MODULES
# ==============================================================================
add_h1(doc, "Chapter 4: Application Functional Modules")

add_h2(doc, "4.1 Authentication & Role-Based Access Control (login.php)")
add_p(doc, "The authentication portal (login.php) models a modern SaaS authentication screen with tabbed sign-in and registration interfaces. The authentication engine verifies credentials against the users table. Default seed credentials provide evaluator access for the candidate persona Ram Karthik (ram.karthik@securejob.io / candidate123) and system administrators.")

add_image_box(doc, img_login, "SecureJobLab Authentication Screen (Candidate & Admin RBAC)", width=Inches(5.8))

add_h2(doc, "4.2 Instant Job Board & Filtering Engine (index.php)")
add_p(doc, "The primary job board presents five verified high-tier cybersecurity positions (Amazon Web Services, Stripe, Microsoft India, Razorpay, CRED). An instant AJAX search engine filters jobs dynamically across titles, companies, locations, and employment types without requiring complete page reloads.")

add_image_box(doc, img_index, "Recruitment Portal Interface: Verified Cybersecurity Openings", width=Inches(5.8))

add_h2(doc, "4.3 Candidate Application Pipeline & Local Document Storage")
add_p(doc, "Authenticated candidates can submit applications with customized cover notes and resume file attachments. Attached resumes are processed by api.php and stored locally under uploads/resumes/. The My Applications tab (Figure 14) displays live application status tracking ('Interview Scheduled', 'Under Review') and allows candidate-driven application withdrawal.")

add_image_box(doc, img_apps, "Candidate Application Pipeline & Local Resume Storage Dashboard", width=Inches(5.8))

doc.add_page_break()

# ==============================================================================
# CHAPTER 5: MODULE 1 — SQL INJECTION (SQLi) [CWE-89]
# ==============================================================================
add_h1(doc, "Chapter 5: Vulnerability 1 — SQL Injection (SQLi) [CWE-89]")

add_h2(doc, "5.1 Vulnerability Overview & Threat Dynamics")
add_p(doc, "SQL Injection (CWE-89) occurs when untrusted user input is directly concatenated into a dynamic SQL query without syntax separation or parameter binding. In web applications, this allows threat actors to manipulate query logic, bypass authentication, extract confidential data, or execute administrative commands.")

add_h2(doc, "5.2 Vulnerable Implementation & Attack Execution")
add_p(doc, "In SecureJobLab's Vulnerable Mode, the search parameter is interpolated directly into the database query string inside api.php:")

add_code_block(doc,
"""// Vulnerable SQL Construction (api.php)
$query = "SELECT id, title, company, salary, secret_notes FROM jobs WHERE title = '$payload'";
$res = mysqli_query($conn, $query);""",
"Vulnerable Dynamic SQL Interpolation")

add_p(doc, "When an evaluator supplies an authentication bypass or tautological payload, the query syntax is fundamentally altered:")
add_bullet(doc, "Test Payload: ' OR 1=1 #", "• ")
add_bullet(doc, "Executed Query: SELECT id, title, company, salary, secret_notes FROM jobs WHERE title = '' OR 1=1 #'", "• ")
add_bullet(doc, "Observed Behavior: The WHERE clause evaluates to true for every row in the table. The application dumps all job records, including confidential executive compensation notes and clearance bands.", "• ")

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

add_dual_image_comparison(doc, img_m1_v, img_m1_s,
    "SQLi Vulnerable: 5 Records & Secret Notes Dumped",
    "SQLi Secure: Parameterized Defense Neutralizes Injection")

add_callout(doc, "Defense Verified: Parameterized prepared statements (mysqli_prepare + mysqli_stmt_bind_param) separate query structure from data evaluation, eliminating SQL injection vulnerability regardless of input characters.", "KEY TAKEAWAY", "green")

doc.add_page_break()

# ==============================================================================
# CHAPTER 6: MODULE 2 — CROSS-SITE SCRIPTING (XSS) [CWE-79]
# ==============================================================================
add_h1(doc, "Chapter 6: Vulnerability 2 — Cross-Site Scripting (XSS) [CWE-79]")

add_h2(doc, "6.1 Vulnerability Overview & Threat Dynamics")
add_p(doc, "Cross-Site Scripting (CWE-79) arises when an application includes untrusted user data in an HTTP response without context-aware sanitization or encoding. When rendered by a victim's browser, the injected code executes in the security context of the vulnerable application, allowing session hijacking, credential theft, and DOM tampering.")

add_h2(doc, "6.2 Vulnerable Implementation & Live Script Execution")
add_p(doc, "In Vulnerable Mode, user-supplied search parameters or candidate review notes are reflected directly into the Document Object Model (DOM) without sanitization:")

add_code_block(doc,
"""// Vulnerable Reflection (api.php / index.php)
echo json_encode(['rendered_html' => $input]);
// Frontend DOM Sink (index.php)
previewEl.innerHTML = res.rendered_html;""",
"Vulnerable Raw HTML/Script Injection")

add_p(doc, "To ensure realistic viva demonstration, clicking 'Execute Test' in Vulnerable Mode dynamically executes script payloads, triggering native browser dialog popups:")
add_bullet(doc, "Test Payload: <script>alert('XSS: ' + document.domain)</script>", "• ")
add_bullet(doc, "Observed Behavior: The browser displays an alert popup displaying 'XSS: localhost'. Arbitrary JavaScript executes within the active session context.", "• ")

add_h2(doc, "6.3 Secure Mitigation & Contextual Output Encoding")
add_p(doc, "In Secure Mode, output reflection is secured using PHP's htmlspecialchars() function with strict entity mapping:")

add_dual_code_comparison(doc,
"""// Vulnerable: Raw Unencoded Reflection
$rendered = $input;
echo $rendered;""",
"""// Secure: Contextual HTML Entity Encoding
$safe = htmlspecialchars($input, ENT_QUOTES, 'UTF-8');
echo $safe;""",
"Vulnerable Raw Output", "Secure htmlspecialchars() Encoding")

add_p(doc, "By converting sensitive HTML control characters into benign entities (< becomes &lt;, > becomes &gt;, \" becomes &quot;, and ' becomes &#039;), the browser's HTML parser treats the payload strictly as printable text. Script execution is completely prevented.")

add_dual_image_comparison(doc, img_m2_v, img_m2_s,
    "XSS Vulnerable: Native Alert & Arbitrary Script Executed",
    "XSS Secure: Entity-Encoded Output Rendered Harmlessly")

add_callout(doc, "Defense Verified: Contextual output encoding (htmlspecialchars with ENT_QUOTES and UTF-8) instructs browser parsers to interpret user characters as literal text rather than executable markup.", "KEY TAKEAWAY", "green")

doc.add_page_break()

# ==============================================================================
# CHAPTER 7: MODULE 3 — OS COMMAND INJECTION [CWE-78]
# ==============================================================================
add_h1(doc, "Chapter 7: Vulnerability 3 — OS Command Injection [CWE-78]")

add_h2(doc, "7.1 Vulnerability Overview & Threat Dynamics")
add_p(doc, "OS Command Injection (CWE-78) occurs when untrusted input is passed directly to an operating system shell interpreter (e.g., cmd.exe, /bin/sh) without validation. By appending shell metacharacters (&, |, ;, `), an attacker can execute arbitrary operating system commands with the privileges of the web server process.")

add_h2(doc, "7.2 Vulnerable Implementation & Shell Chaining")
add_p(doc, "SecureJobLab implements an enterprise network latency diagnostic utility. In Vulnerable Mode, the target IP or hostname is concatenated directly into a shell execution string:")

add_code_block(doc,
"""// Vulnerable OS Shell Concatenation (api.php)
$cmd = "ping -n 1 " . $host;
$output = shell_exec($cmd);""",
"Vulnerable System Call Concatenation")

add_p(doc, "When an evaluator injects command separators, the shell executes secondary operating system binaries:")
add_bullet(doc, "Test Payload: 127.0.0.1 & whoami", "• ")
add_bullet(doc, "Executed Shell Command: ping -n 1 127.0.0.1 & whoami", "• ")
add_bullet(doc, "Observed Behavior: The ping command executes, immediately followed by the whoami binary. The server's OS username (desktop-ram\\ram) is returned in the telemetry output.", "• ")

add_h2(doc, "7.3 Secure Mitigation & Strict Whitelisting")
add_p(doc, "In Secure Mode, user input is validated against a strict regular expression whitelist and escaped using escapeshellarg():")

add_dual_code_comparison(doc,
"""// Vulnerable: Direct Shell Call
$cmd = "ping -n 1 " . $host;
$output = shell_exec($cmd);""",
"""// Secure: Regex Whitelist & Argument Escaping
if (preg_match('/^[a-zA-Z0-9.-]+$/', $host)) {
    $clean_host = escapeshellarg($host);
    $cmd = "ping -n 1 " . $clean_host;
    $output = shell_exec($cmd);
} else {
    // Reject input containing &, |, ;, `, spaces
    throw new SecurityException("Invalid Host");
}""",
"Vulnerable shell_exec()", "Secure Regex Whitelist + escapeshellarg()")

add_p(doc, "The regular expression enforces that the input consists exclusively of alphanumeric characters, dots, and hyphens. Any payload containing command separators (&, |, ;, spaces) is rejected before reaching the operating system shell.")

add_dual_image_comparison(doc, img_m3_v, img_m3_s,
    "Command Injection Vulnerable: whoami Executed on Host",
    "Command Injection Secure: Delimiters Rejected by Whitelist")

add_callout(doc, "Defense Verified: Input whitelist validation combined with escapeshellarg() prevents command separator injection and enforces strict system call boundaries.", "KEY TAKEAWAY", "green")

doc.add_page_break()

# ==============================================================================
# CHAPTER 8: MODULE 4 — DIRECTORY / PATH TRAVERSAL [CWE-22]
# ==============================================================================
add_h1(doc, "Chapter 8: Vulnerability 4 — Directory / Path Traversal [CWE-22]")

add_h2(doc, "8.1 Vulnerability Overview & Threat Dynamics")
add_p(doc, "Directory Traversal (CWE-22) occurs when an application accepts path input without validation, allowing directory climbing sequences (../ or ..\\) to navigate outside the intended folder hierarchy. This allows unauthorized reading of sensitive server configuration files, credentials, or source code.")

add_h2(doc, "8.2 Vulnerable Implementation & Path Climbing")
add_p(doc, "SecureJobLab features a candidate document and resume inspector. In Vulnerable Mode, the requested filename parameter is concatenated directly onto the document directory path:")

add_code_block(doc,
"""// Vulnerable Path Concatenation (api.php)
$path = __DIR__ . '/lab_files/' . $file;
if (file_exists($path)) {
    $content = file_get_contents($path);
}""",
"Vulnerable Uncanonicalized Path Concatenation")

add_p(doc, "By supplying relative traversal tokens, an attacker escapes the lab_files directory:")
add_bullet(doc, "Test Payload: ../database.sql", "• ")
add_bullet(doc, "Resolved Path: C:\\xampp\\htdocs\\SecureJobLab\\database.sql", "• ")
add_bullet(doc, "Observed Behavior: The application escapes lab_files/ and reads the database schema file, exposing table definitions, database credentials, and seed user records.", "• ")

add_h2(doc, "8.3 Secure Mitigation & Canonical Boundary Defense")
add_p(doc, "In Secure Mode, the application enforces filename isolation via basename() and validates requests against an explicit whitelist array:")

add_dual_code_comparison(doc,
"""// Vulnerable: Unrestricted Relative Path
$path = __DIR__ . '/lab_files/' . $file;
$content = file_get_contents($path);""",
"""// Secure: Basename Extraction & Whitelist Match
$safe_file = basename($file);
$whitelist = ['resume.txt', 'secret_flag.txt', 
  'coverletter.txt', 'certificate.txt'];
if (in_array($safe_file, $whitelist, true)) {
    $path = __DIR__ . '/lab_files/' . $safe_file;
    $content = file_get_contents($path);
} else {
    // Access Denied: Unauthorized file
}""",
"Vulnerable Relative Inclusion", "Secure basename() + Whitelist Array")

add_p(doc, "The basename() function strips directory traversal tokens (../). Even if an attacker supplies ../database.sql, the sanitized string resolves to database.sql, which is rejected by the whitelist check. Access is strictly confined to authorized candidate documents.")

add_dual_image_comparison(doc, img_m4_v, img_m4_s,
    "Directory Traversal Vulnerable: database.sql Extracted",
    "Directory Traversal Secure: Access Denied by Whitelist")

add_callout(doc, "Defense Verified: basename() token stripping combined with an explicit whitelist array guarantees sandbox confinement and prevents filesystem traversal.", "KEY TAKEAWAY", "green")

doc.add_page_break()

# ==============================================================================
# CHAPTER 9: MODULE 5 — CLICKJACKING [CWE-1021]
# ==============================================================================
add_h1(doc, "Chapter 9: Vulnerability 5 — Clickjacking (UI Redressing) [CWE-1021]")

add_h2(doc, "9.1 Vulnerability Overview & High-Impact Destructive Scenario")
add_p(doc, "Clickjacking (CWE-1021), also termed UI Redressing, occurs when an attacker renders a legitimate, authenticated application inside a transparent iframe overlaying an enticing decoy interface. When the victim clicks the visible decoy, the click lands on a hidden, sensitive button inside the framed application.")
add_p(doc, "In SecureJobLab, the framed target (clickjack_target.php) models a destructive action: Permanent Account Deletion & Data Wipe for candidate Ram Karthik (UID SJ-9042-ADMIN).")

add_h2(doc, "9.2 Interactive UI Redressing Sandbox with Opacity Slider")
add_p(doc, "To provide clear visual proof during academic examination, Module 5 integrates an interactive UI Redressing Sandbox featuring a live Opacity Slider (0% to 100%):")
add_bullet(doc, "0% Stealth Mode: The destructive target iframe is completely transparent. The user sees only the decoy button: '🎉 Claim Your ₹50,000 Signing Bonus!'.", "• ")
add_bullet(doc, "30% Ghost Mode (Figure 9): Demonstrates the alignment between the decoy button and the destructive '⚠️ Permanently Delete Account' button directly underneath.", "• ")
add_bullet(doc, "100% Revealed Mode (Figure 8): The red destructive target box is visible, proving framing occurs without restriction.", "• ")

add_image_box(doc, img_m5_100, "Clickjacking UI Redressing Sandbox at 100% Opacity (Harmful Button Revealed)", width=Inches(5.6))
add_image_box(doc, img_m5_30, "Clickjacking UI Redressing Sandbox at 30% Opacity (Ghost Alignment Mode)", width=Inches(5.6))

add_p(doc, "When the user clicks the decoy button in Stealth Mode, the hijacked click executes the destructive account deletion form:")

add_image_box(doc, img_m5_trig, "Clickjacking Exploit Triggered: Unauthorized Account Deletion Execution", width=Inches(5.6))

add_h2(doc, "9.3 Secure Mitigation & HTTP Framing Protection Headers")
add_p(doc, "In Secure Mode, clickjack_target.php emits defense-in-depth HTTP security headers:")

add_dual_code_comparison(doc,
"""// Vulnerable: Missing Framing Headers
// Browser permits third-party iframe embedding
// (No X-Frame-Options or CSP headers emitted)""",
"""// Secure: Strict Framing Defense Headers
header("X-Frame-Options: DENY");
header("Content-Security-Policy: frame-ancestors 'none'");""",
"Vulnerable: Framing Permitted", "Secure: Framing Blocked via Headers")

add_p(doc, "Modern web browsers inspect X-Frame-Options: DENY and CSP frame-ancestors 'none' prior to rendering framed content. When detected, the browser terminates iframe rendering, preventing UI redressing entirely.")

add_image_box(doc, img_m5_s, "Clickjacking Defended: Browser Iframe Blocking via X-Frame-Options: DENY", width=Inches(5.6))

add_callout(doc, "Defense Verified: X-Frame-Options: DENY and CSP frame-ancestors 'none' instruct modern browsers to reject all iframe embedding attempts, neutralizing Clickjacking.", "KEY TAKEAWAY", "green")

doc.add_page_break()

# ==============================================================================
# CHAPTER 10: COMPARATIVE DEFENSE MATRIX & TELEMETRY
# ==============================================================================
add_h1(doc, "Chapter 10: Comparative Defense Matrix & Telemetry Analysis")

add_h2(doc, "10.1 Master 5-Vulnerability Security Comparison Matrix")
add_p(doc, "The following matrix provides a technical comparison of the five implemented vulnerabilities, summarizing their root causes, exploit impacts, mitigations, and verified statuses:")

# Table 3: Master Comparison Matrix
tbl_master = doc.add_table(rows=6, cols=5)
tbl_master.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_master.autofit = False
tbl_master.columns[0].width = Inches(1.3)
tbl_master.columns[1].width = Inches(1.1)
tbl_master.columns[2].width = Inches(1.4)
tbl_master.columns[3].width = Inches(1.6)
tbl_master.columns[4].width = Inches(1.1)

headers_m = ["Vulnerability", "CWE Class", "Root Cause", "Defense Mitigation", "Status"]
for i, h in enumerate(headers_m):
    cell = tbl_master.cell(0, i)
    set_cell_background(cell, HEX_NAVY)
    set_cell_margins(cell, top=60, bottom=60, left=60, right=60)
    p = cell.paragraphs[0]
    r = p.add_run(h)
    r.font.bold = True
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(255, 255, 255)

matrix_data = [
    ("SQL Injection (SQLi)", "CWE-89", "Unsanitized dynamic string interpolation in SQL queries.", "Parameterized Prepared Statements (mysqli_prepare).", "VERIFIED (PASS)"),
    ("Cross-Site Scripting (XSS)", "CWE-79", "Direct raw output reflection into DOM without encoding.", "Contextual HTML Entity Encoding (htmlspecialchars).", "VERIFIED (PASS)"),
    ("OS Command Injection", "CWE-78", "Direct concatenation of untrusted input into shell_exec().", "Strict Regex Whitelisting + Argument Escaping (escapeshellarg).", "VERIFIED (PASS)"),
    ("Directory Traversal", "CWE-22", "Uncanonicalized relative path inclusion (../).", "basename() Token Stripping + Explicit Whitelist Array.", "VERIFIED (PASS)"),
    ("Clickjacking (UI Redressing)", "CWE-1021", "Missing HTTP framing headers permitting iframe embedding.", "X-Frame-Options: DENY & CSP frame-ancestors 'none'.", "VERIFIED (PASS)"),
]

for row_idx, data in enumerate(matrix_data, start=1):
    bg_col = HEX_LIGHT_GRAY if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, text in enumerate(data):
        cell = tbl_master.cell(row_idx, col_idx)
        set_cell_background(cell, bg_col)
        set_cell_margins(cell, top=50, bottom=50, left=60, right=60)
        set_cell_borders(cell,
            top={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
            bottom={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
            left={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
            right={'val': 'single', 'sz': '4', 'color': HEX_BORDER}
        )
        p = cell.paragraphs[0]
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        if col_idx == 4:
            r.font.bold = True
            r.font.color.rgb = COLOR_GREEN
        else:
            r.font.color.rgb = COLOR_BODY

p_after_tm = doc.add_paragraph()
p_after_tm.paragraph_format.space_before = Pt(6)

add_h2(doc, "10.2 Real-time Security Telemetry Engine")
add_p(doc, "Every module in SecureJobLab communicates with api.php using JSON telemetry. When an evaluator dispatches an attack payload, the telemetry engine computes and renders:")
add_bullet(doc, "Exploit Status: Clear diagnostic indicator stating whether the exploit succeeded or the defense held.", "• ")
add_bullet(doc, "Executed Query / Shell Command: Exact runtime string compiled by the database or operating system.", "• ")
add_bullet(doc, "Returned Data Records: Interactive table displaying extracted records or database error messages.", "• ")
add_bullet(doc, "Mitigation Telemetry: Technical explanation of the security control neutralizing the attack.", "• ")

doc.add_page_break()

# ==============================================================================
# CHAPTER 11: TESTING & VERIFICATION METHODOLOGY
# ==============================================================================
add_h1(doc, "Chapter 11: Testing & Verification Methodology")

add_h2(doc, "11.1 Test Plan & Execution Strategy")
add_p(doc, "Testing was conducted using a dual verification strategy:")
add_bullet(doc, "Automated Browser Testing: Automated browser test suites in Microsoft Edge via Playwright validating HTTP responses, status codes, and DOM mutations.", "1. ")
add_bullet(doc, "Manual Verification: Direct evaluation in web browsers verifying alert popups, UI Redressing sliders, and visual telemetry rendering.", "2. ")

add_h2(doc, "11.2 Comprehensive Verification Results Table (10 Scenarios)")
add_p(doc, "The testing matrix evaluates each of the five vulnerabilities across both Vulnerable and Secure modes, yielding ten test scenarios:")

# Table 4: Test Cases Table
tbl_test = doc.add_table(rows=11, cols=5)
tbl_test.alignment = WD_TABLE_ALIGNMENT.CENTER
tbl_test.autofit = False
tbl_test.columns[0].width = Inches(0.8)
tbl_test.columns[1].width = Inches(1.3)
tbl_test.columns[2].width = Inches(1.7)
tbl_test.columns[3].width = Inches(1.9)
tbl_test.columns[4].width = Inches(0.8)

headers_tc = ["Test ID", "Module & Mode", "Payload / Input", "Expected Result", "Status"]
for i, h in enumerate(headers_tc):
    cell = tbl_test.cell(0, i)
    set_cell_background(cell, HEX_NAVY)
    set_cell_margins(cell, top=50, bottom=50, left=50, right=50)
    p = cell.paragraphs[0]
    r = p.add_run(h)
    r.font.bold = True
    r.font.size = Pt(8.5)
    r.font.color.rgb = RGBColor(255, 255, 255)

test_cases = [
    ("TC-01", "SQLi (Vulnerable)", "' OR 1=1 #", "Bypasses query; returns all 5 jobs & secret notes.", "PASS"),
    ("TC-02", "SQLi (Secure)", "' OR 1=1 #", "Treated as literal string; 0 jobs returned; query intact.", "PASS"),
    ("TC-03", "XSS (Vulnerable)", "<script>alert('XSS')</script>", "Renders raw script in DOM; triggers native alert dialog.", "PASS"),
    ("TC-04", "XSS (Secure)", "<script>alert('XSS')</script>", "Encoded with htmlspecialchars(); displayed as safe text.", "PASS"),
    ("TC-05", "Cmd Inj (Vulnerable)", "127.0.0.1 & whoami", "Executes ping followed by whoami; prints server username.", "PASS"),
    ("TC-06", "Cmd Inj (Secure)", "127.0.0.1 & whoami", "Rejected by regex whitelist; system call blocked.", "PASS"),
    ("TC-07", "Traversal (Vulnerable)", "../database.sql", "Escapes folder; reads raw database schema file.", "PASS"),
    ("TC-08", "Traversal (Secure)", "../database.sql", "Tokens stripped; database.sql rejected by whitelist.", "PASS"),
    ("TC-09", "Clickjack (Vulnerable)", "Decoy Button Click (0% Opacity)", "Invisible iframe receives click; account deletion executed.", "PASS"),
    ("TC-10", "Clickjack (Secure)", "Decoy Button Click", "Framing blocked by X-Frame-Options: DENY; iframe blank.", "PASS"),
]

for row_idx, data in enumerate(test_cases, start=1):
    bg_col = HEX_LIGHT_GRAY if row_idx % 2 == 1 else "FFFFFF"
    for col_idx, text in enumerate(data):
        cell = tbl_test.cell(row_idx, col_idx)
        set_cell_background(cell, bg_col)
        set_cell_margins(cell, top=40, bottom=40, left=50, right=50)
        set_cell_borders(cell,
            top={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
            bottom={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
            left={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
            right={'val': 'single', 'sz': '4', 'color': HEX_BORDER}
        )
        p = cell.paragraphs[0]
        r = p.add_run(text)
        r.font.name = "Calibri"
        r.font.size = Pt(8)
        if col_idx == 4:
            r.font.bold = True
            r.font.color.rgb = COLOR_GREEN
        elif col_idx == 0:
            r.font.bold = True
            r.font.color.rgb = COLOR_NAVY
        else:
            r.font.color.rgb = COLOR_BODY

p_after_tt = doc.add_paragraph()
p_after_tt.paragraph_format.space_before = Pt(6)

add_callout(doc, "Verification Summary: 10 out of 10 test cases passed with 100% adherence to expected behavioral specifications. Both exploitation mechanics and defensive mitigations were confirmed.", "TESTING SUMMARY", "green")

doc.add_page_break()

# ==============================================================================
# CHAPTER 12: VIVA VOCE REFERENCE GUIDE
# ==============================================================================
add_h1(doc, "Chapter 12: Viva Voce Reference & Security Analysis")
add_p(doc, "This chapter provides concise technical answers to key questions anticipated during the academic viva examination for Course 20CYS403:")

add_h2(doc, "Q1: Why is prepared statement execution inherently immune to SQL Injection?")
add_p(doc, "Prepared statements compile the SQL command structure beforehand into an Abstract Syntax Tree (AST). User-supplied data is transmitted separately and bound exclusively as parameter literals. The database query parser never re-interprets bound parameters as executable SQL grammar.")

add_h2(doc, "Q2: Why does htmlspecialchars() neutralize XSS, and why are ENT_QUOTES necessary?")
add_p(doc, "htmlspecialchars() replaces HTML meta-characters (&, <, >, \", ') with HTML entities (&amp;, &lt;, &gt;, &quot;, &#039;). The browser's DOM parser treats these as printable text rather than tag delimiters. ENT_QUOTES ensures single quotes are encoded, preventing attribute breakout attacks.")

add_h2(doc, "Q3: What distinguishes escapeshellarg() from input whitelisting in Command Injection defense?")
add_p(doc, "escapeshellarg() wraps arguments in single quotes and escapes existing quotes, ensuring shell parsers interpret the input as a single literal argument. Input whitelisting rejects characters entirely before any system call occurs, providing defense-in-depth.")

add_h2(doc, "Q4: How does basename() prevent Directory Traversal attacks?")
add_p(doc, "basename() extracts the trailing name component of a path, stripping path-traversal tokens like ../ and ..\\. In SecureJobLab, basename() is paired with an explicit whitelist array to ensure only approved document files can be accessed.")

add_h2(doc, "Q5: How do X-Frame-Options and CSP frame-ancestors protect against Clickjacking?")
add_p(doc, "X-Frame-Options: DENY instructs the browser to refuse rendering the target inside any frame. CSP frame-ancestors 'none' provides modern, granular defense. The browser terminates frame rendering before user interaction occurs.")

doc.add_page_break()

# ==============================================================================
# CHAPTERS 13 & 14: LIMITATIONS, FUTURE ENHANCEMENTS & CONCLUSION
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
# REFERENCES
# ==============================================================================
add_h1(doc, "References & Authoritative Standards")

references = [
    ("[1] OWASP Foundation", "OWASP Top 10:2021 — The Ten Most Critical Web Application Security Risks", "https://owasp.org/Top10/"),
    ("[2] MITRE Corporation", "CWE-89: Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection')", "https://cwe.mitre.org/data/definitions/89.html"),
    ("[3] MITRE Corporation", "CWE-79: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting')", "https://cwe.mitre.org/data/definitions/79.html"),
    ("[4] MITRE Corporation", "CWE-78: Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection')", "https://cwe.mitre.org/data/definitions/78.html"),
    ("[5] MITRE Corporation", "CWE-22: Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal')", "https://cwe.mitre.org/data/definitions/22.html"),
    ("[6] MITRE Corporation", "CWE-1021: Improper Restriction of Rendered UI Layers or Frames ('Clickjacking')", "https://cwe.mitre.org/data/definitions/1021.html"),
    ("[7] Mozilla Developer Network", "Content Security Policy (CSP): frame-ancestors Directive", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/frame-ancestors"),
    ("[8] Mozilla Developer Network", "X-Frame-Options Response Header Specification", "https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options"),
    ("[9] PHP Group", "PHP: Prepared Statements and Stored Procedures — PDO & MySQLi Manual", "https://www.php.net/manual/en/mysqli.quickstart.prepared-statements.php"),
    ("[10] National Institute of Standards and Technology (NIST)", "Special Publication 800-95: Guide to Secure Web Services", "https://csrc.nist.gov/publications/detail/sp/800-95/final"),
]

for ref_id, ref_title, ref_url in references:
    p_r = doc.add_paragraph()
    p_r.paragraph_format.space_before = Pt(2)
    p_r.paragraph_format.space_after = Pt(3)
    p_r.paragraph_format.line_spacing = 1.15
    r_id = p_r.add_run(f"{ref_id} ")
    r_id.font.bold = True
    r_id.font.color.rgb = COLOR_NAVY
    r_t = p_r.add_run(f"{ref_title}. Available: ")
    r_t.font.color.rgb = COLOR_BODY
    r_u = p_r.add_run(ref_url)
    r_u.font.color.rgb = COLOR_BLUE
    r_u.font.italic = True

out_docx = os.path.join(base_dir, "SecureJobLab_Web_Application_Security_Report.docx")
doc.save(out_docx)
print("Successfully generated Word document at:", out_docx)
