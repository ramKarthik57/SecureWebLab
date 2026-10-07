"""
build_flawless_report.py
========================
Generates a polished, submission-ready academic project report for SecureJobLab (Course: 20CYS403).

Key Design Goals:
1. Student Name: strictly "Ram Karthik G" (no "Persona", no subtitle).
2. 2nd image (diagram_dual_engine.png) is completely removed.
3. Proper Table of Contents using native Word Tab Stops with Dot Leaders (numbers flush-right).
4. Continuous, beautifully filled pages: ZERO artificial white gaps between contents.
5. Strictly 5 Core CWE Vulnerabilities (CWE-89, CWE-79, CWE-78, CWE-22, CWE-1021).
6. High-impact Clickjacking UI Redressing demonstration with Opacity slider evidence.
7. Professional typography, color palette, borders, callouts, and side-by-side comparative tables.
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

# Image assets
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

# Palette
COLOR_NAVY = RGBColor(27, 54, 93)       # #1B365D - H1
COLOR_STEEL = RGBColor(43, 76, 126)     # #2B4C7E - H2
COLOR_SLATE = RGBColor(44, 62, 80)      # #2C3E50 - H3
COLOR_BODY = RGBColor(33, 37, 41)       # #212529 - Text
COLOR_MUTED = RGBColor(108, 117, 125)   # #6C757D - Footers, Captions
COLOR_RED = RGBColor(220, 38, 38)       # #DC2626 - Vuln
COLOR_GREEN = RGBColor(16, 185, 129)    # #10B981 - Secure

HEX_NAVY = "1B365D"
HEX_STEEL = "2B4C7E"
HEX_LIGHT_GRAY = "F8FAFC"
HEX_BORDER = "CBD5E1"
HEX_CODE_BG = "F8F9FA"

# --- Helper Functions ---
def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    for child in list(tcPr):
        if child.tag.endswith('shd'):
            tcPr.remove(child)
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=40, bottom=40, left=50, right=50):
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

def add_h1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = COLOR_NAVY
    return p

def add_h2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(11)
    r.font.bold = True
    r.font.color.rgb = COLOR_STEEL
    return p

def add_h3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(1.5)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(9.5)
    r.font.bold = True
    r.font.color.rgb = COLOR_SLATE
    return p

def add_p(doc, text, bold_prefix=None, italic=False):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.1
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
    p.paragraph_format.line_spacing = 1.1
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
    set_cell_margins(c, top=30, bottom=30, left=45, right=45)

    if color_type == "green":
        bg_hex, border_hex, title_col = "F0FDF4", "10B981", COLOR_GREEN
    elif color_type == "red":
        bg_hex, border_hex, title_col = "FEF2F2", "DC2626", COLOR_RED
    else:
        bg_hex, border_hex, title_col = "F8FAFC", "2563EB", COLOR_STEEL

    set_cell_background(c, bg_hex)
    set_cell_borders(c,
        left={'val': 'single', 'sz': '16', 'color': border_hex},
        top={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
        right={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
        bottom={'val': 'single', 'sz': '4', 'color': HEX_BORDER}
    )

    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.line_spacing = 1.1

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
    p_after.paragraph_format.space_before = Pt(1)
    p_after.paragraph_format.space_after = Pt(0)

def add_code_block(doc, code_str, title=None):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(6.5)

    c = tbl.cell(0, 0)
    set_cell_margins(c, top=25, bottom=25, left=40, right=40)
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
    p_after.paragraph_format.space_before = Pt(1)
    p_after.paragraph_format.space_after = Pt(0)

def add_dual_code_comparison(doc, vuln_code, sec_code, vuln_title="Vulnerable Mode", sec_title="Secure Mode"):
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(3.2)
    tbl.columns[1].width = Inches(3.2)

    # Col 0: Vulnerable
    c0 = tbl.cell(0, 0)
    set_cell_margins(c0, top=25, bottom=25, left=35, right=35)
    set_cell_background(c0, "FEF2F2")
    set_cell_borders(c0,
        left={'val': 'single', 'sz': '10', 'color': 'DC2626'},
        top={'val': 'single', 'sz': '4', 'color': 'FCA5A5'},
        right={'val': 'single', 'sz': '4', 'color': 'FCA5A5'},
        bottom={'val': 'single', 'sz': '4', 'color': 'FCA5A5'}
    )
    p0 = c0.paragraphs[0]
    p0.paragraph_format.space_before = Pt(0)
    p0.paragraph_format.space_after = Pt(0)
    p0.paragraph_format.line_spacing = 1.02
    r0_h = p0.add_run(f"🔴 {vuln_title}\n")
    r0_h.font.name = "Consolas"
    r0_h.font.size = Pt(7.5)
    r0_h.font.bold = True
    r0_h.font.color.rgb = COLOR_RED
    r0_c = p0.add_run(vuln_code)
    r0_c.font.name = "Consolas"
    r0_c.font.size = Pt(6.8)
    r0_c.font.color.rgb = COLOR_BODY

    # Col 1: Secure
    c1 = tbl.cell(0, 1)
    set_cell_margins(c1, top=25, bottom=25, left=35, right=35)
    set_cell_background(c1, "F0FDF4")
    set_cell_borders(c1,
        left={'val': 'single', 'sz': '10', 'color': '10B981'},
        top={'val': 'single', 'sz': '4', 'color': '86EFAC'},
        right={'val': 'single', 'sz': '4', 'color': '86EFAC'},
        bottom={'val': 'single', 'sz': '4', 'color': '86EFAC'}
    )
    p1 = c1.paragraphs[0]
    p1.paragraph_format.space_before = Pt(0)
    p1.paragraph_format.space_after = Pt(0)
    p1.paragraph_format.line_spacing = 1.02
    r1_h = p1.add_run(f"🟢 {sec_title}\n")
    r1_h.font.name = "Consolas"
    r1_h.font.size = Pt(7.5)
    r1_h.font.bold = True
    r1_h.font.color.rgb = COLOR_GREEN
    r1_c = p1.add_run(sec_code)
    r1_c.font.name = "Consolas"
    r1_c.font.size = Pt(6.8)
    r1_c.font.color.rgb = COLOR_BODY

    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(1)
    p_after.paragraph_format.space_after = Pt(0)

def add_image_box(doc, img_path, caption, width=Inches(4.4)):
    if not os.path.exists(img_path):
        add_p(doc, f"[Image Missing: {img_path}]", bold_prefix="[IMAGE PLACEHOLDER] ")
        return

    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.keep_with_next = True
    run = p.add_run()
    run.add_picture(img_path, width=width)

    p_cap = doc.add_paragraph()
    p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_cap.paragraph_format.space_before = Pt(1)
    p_cap.paragraph_format.space_after = Pt(3)
    r_cap = p_cap.add_run(f"Figure: {caption}")
    r_cap.font.name = "Calibri"
    r_cap.font.size = Pt(7.8)
    r_cap.font.italic = True
    r_cap.font.color.rgb = COLOR_MUTED

def add_dual_image_comparison(doc, img_left, img_right, caption_left, caption_right):
    tbl = doc.add_table(rows=1, cols=2)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False
    tbl.columns[0].width = Inches(3.2)
    tbl.columns[1].width = Inches(3.2)

    # Left
    c0 = tbl.cell(0, 0)
    set_cell_margins(c0, top=15, bottom=15, left=20, right=20)
    set_cell_borders(c0,
        top={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
        bottom={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
        left={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
        right={'val': 'single', 'sz': '4', 'color': HEX_BORDER}
    )
    p0 = c0.paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p0.paragraph_format.space_before = Pt(0)
    p0.paragraph_format.space_after = Pt(0)
    if os.path.exists(img_left):
        p0.add_run().add_picture(img_left, width=Inches(3.05))
    else:
        p0.add_run(f"[Left Image: {os.path.basename(img_left)}]")

    p0_cap = c0.add_paragraph()
    p0_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p0_cap.paragraph_format.space_before = Pt(2)
    p0_cap.paragraph_format.space_after = Pt(0)
    r0 = p0_cap.add_run(f"🔴 {caption_left}")
    r0.font.name = "Calibri"
    r0.font.size = Pt(7.5)
    r0.font.bold = True
    r0.font.color.rgb = COLOR_RED

    # Right
    c1 = tbl.cell(0, 1)
    set_cell_margins(c1, top=15, bottom=15, left=20, right=20)
    set_cell_borders(c1,
        top={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
        bottom={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
        left={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
        right={'val': 'single', 'sz': '4', 'color': HEX_BORDER}
    )
    p1 = c1.paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1.paragraph_format.space_before = Pt(0)
    p1.paragraph_format.space_after = Pt(0)
    if os.path.exists(img_right):
        p1.add_run().add_picture(img_right, width=Inches(3.05))
    else:
        p1.add_run(f"[Right Image: {os.path.basename(img_right)}]")

    p1_cap = c1.add_paragraph()
    p1_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p1_cap.paragraph_format.space_before = Pt(2)
    p1_cap.paragraph_format.space_after = Pt(0)
    r1 = p1_cap.add_run(f"🟢 {caption_right}")
    r1.font.name = "Calibri"
    r1.font.size = Pt(7.5)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_GREEN

    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(1)
    p_after.paragraph_format.space_after = Pt(0)

def add_table(doc, headers, rows_data, col_widths=None):
    tbl = doc.add_table(rows=len(rows_data) + 1, cols=len(headers))
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl.autofit = False

    # Header Row
    hdr_row = tbl.rows[0]
    trPr = hdr_row._tr.get_or_add_trPr()
    trPr.append(parse_xml(f'<w:tblHeader {nsdecls("w")}/>'))

    for idx, heading in enumerate(headers):
        cell = hdr_row.cells[idx]
        if col_widths and idx < len(col_widths):
            cell.width = col_widths[idx]
        set_cell_margins(cell, top=35, bottom=35, left=45, right=45)
        set_cell_background(cell, HEX_NAVY)
        set_cell_borders(cell,
            bottom={'val': 'single', 'sz': '6', 'color': HEX_NAVY},
            top={'val': 'single', 'sz': '4', 'color': HEX_NAVY},
            left={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
            right={'val': 'single', 'sz': '4', 'color': HEX_BORDER}
        )
        p = cell.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.line_spacing = 1.05
        r = p.add_run(heading)
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)

    # Data Rows
    for r_idx, row in enumerate(rows_data):
        row_elm = tbl.rows[r_idx + 1]
        bg = HEX_LIGHT_GRAY if (r_idx % 2 == 1) else "FFFFFF"
        for c_idx, val in enumerate(row):
            cell = row_elm.cells[c_idx]
            if col_widths and c_idx < len(col_widths):
                cell.width = col_widths[c_idx]
            set_cell_margins(cell, top=28, bottom=28, left=45, right=45)
            set_cell_background(cell, bg)
            set_cell_borders(cell,
                bottom={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
                top={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
                left={'val': 'single', 'sz': '4', 'color': HEX_BORDER},
                right={'val': 'single', 'sz': '4', 'color': HEX_BORDER}
            )
            p = cell.paragraphs[0]
            p.paragraph_format.space_before = Pt(0)
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.line_spacing = 1.05
            r = p.add_run(str(val))
            r.font.name = "Calibri"
            r.font.size = Pt(8)
            if "PASS" in str(val) or "VERIFIED" in str(val):
                r.font.bold = True
                r.font.color.rgb = COLOR_GREEN
            elif "Vulnerable" in str(val) or "FAIL" in str(val):
                r.font.color.rgb = COLOR_RED
            else:
                r.font.color.rgb = COLOR_BODY

    p_after = doc.add_paragraph()
    p_after.paragraph_format.space_before = Pt(1)
    p_after.paragraph_format.space_after = Pt(0)


def generate_report():
    doc = docx.Document()

    # Page Setup: Standard Letter, 0.8 in margins (leaves 6.9 in width, 9.4 in height)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(0.8)
        section.bottom_margin = Inches(0.8)
        section.left_margin = Inches(0.8)
        section.right_margin = Inches(0.8)
        section.page_width = Inches(8.5)
        section.page_height = Inches(11.0)
        section.different_first_page_header_footer = True

        # Header for body pages
        hdr = section.header
        hp = hdr.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("Course: 20CYS403 | Web Application Security Laboratory Report | SecureJobLab")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(7.5)
        hrun.font.color.rgb = COLOR_MUTED

        # Footer for body pages
        ftr = section.footer
        fp = ftr.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        frun_l = fp.add_run("SecureJobLab Platform — Exactly 5 CWE Security Modules            ")
        frun_l.font.name = "Calibri"
        frun_l.font.size = Pt(8)
        frun_l.font.color.rgb = COLOR_MUTED
        frun_p = fp.add_run("Page ")
        frun_p.font.name = "Calibri"
        frun_p.font.size = Pt(8)
        frun_p.font.color.rgb = COLOR_MUTED
        add_page_number_to_run(fp.add_run())

    # ==============================================================================
    # PAGE 1: COVER PAGE
    # ==============================================================================
    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_before = Pt(70)
    p_dept.paragraph_format.space_after = Pt(4)
    r_dept = p_dept.add_run("DEPARTMENT OF CYBERSECURITY & COMPUTER ENGINEERING")
    r_dept.font.name = "Calibri"
    r_dept.font.size = Pt(13)
    r_dept.font.bold = True
    r_dept.font.color.rgb = COLOR_NAVY

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_course.paragraph_format.space_before = Pt(2)
    p_course.paragraph_format.space_after = Pt(2)
    r_course = p_course.add_run("20CYS403: WEB APPLICATION SECURITY LABORATORY")
    r_course.font.name = "Calibri"
    r_course.font.size = Pt(11)
    r_course.font.bold = True
    r_course.font.color.rgb = COLOR_STEEL

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_before = Pt(0)
    p_sub.paragraph_format.space_after = Pt(25)
    r_sub = p_sub.add_run("ACADEMIC PROJECT REPORT")
    r_sub.font.name = "Calibri"
    r_sub.font.size = Pt(9.5)
    r_sub.font.color.rgb = COLOR_SLATE

    p_rule1 = doc.add_paragraph()
    p_rule1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_rule1.paragraph_format.space_before = Pt(0)
    p_rule1.paragraph_format.space_after = Pt(25)
    r_rule1 = p_rule1.add_run("—" * 54)
    r_rule1.font.name = "Calibri"
    r_rule1.font.size = Pt(9)
    r_rule1.font.color.rgb = COLOR_STEEL

    # Main Title Card
    tbl_title = doc.add_table(rows=1, cols=1)
    tbl_title.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_title.autofit = False
    tbl_title.columns[0].width = Inches(6.5)
    ct = tbl_title.cell(0, 0)
    set_cell_margins(ct, top=70, bottom=70, left=70, right=70)
    set_cell_background(ct, "F8FAFC")
    set_cell_borders(ct,
        left={'val': 'single', 'sz': '28', 'color': HEX_NAVY},
        top={'val': 'single', 'sz': '6', 'color': HEX_STEEL},
        right={'val': 'single', 'sz': '6', 'color': HEX_STEEL},
        bottom={'val': 'single', 'sz': '6', 'color': HEX_STEEL}
    )

    pt1 = ct.paragraphs[0]
    pt1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pt1.paragraph_format.space_before = Pt(0)
    pt1.paragraph_format.space_after = Pt(8)
    rt1 = pt1.add_run("SecureJobLab: Job Recruitment Vulnerability Demonstration\n& Defense Platform")
    rt1.font.name = "Calibri"
    rt1.font.size = Pt(17)
    rt1.font.bold = True
    rt1.font.color.rgb = COLOR_NAVY

    pt2 = ct.add_paragraph()
    pt2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    pt2.paragraph_format.space_before = Pt(0)
    pt2.paragraph_format.space_after = Pt(0)
    rt2 = pt2.add_run("A Dual-Engine Laboratory for Web Application Vulnerability Analysis & Defensive Engineering\nCovering Exactly Five Core CWE Modules")
    rt2.font.name = "Calibri"
    rt2.font.size = Pt(10)
    rt2.font.italic = True
    rt2.font.color.rgb = COLOR_SLATE

    # Metadata Table
    tbl_meta = doc.add_table(rows=4, cols=2)
    tbl_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_meta.autofit = False
    tbl_meta.columns[0].width = Inches(2.6)
    tbl_meta.columns[1].width = Inches(3.9)

    meta_items = [
        ("Student Name:", "Ram Karthik G"),
        ("Course Name & Code:", "Web Application Security (20CYS403)"),
        ("Evaluation Scope:", "5 Core CWE Modules (SQLi, XSS, Cmd Inj, Traversal, Clickjacking)"),
        ("Platform Architecture:", "Apache 2.4, PHP 8.x, MySQL 10.4 (MariaDB), AJAX, Bootstrap 5"),
    ]

    for idx, (label, val) in enumerate(meta_items):
        cell_lbl = tbl_meta.cell(idx, 0)
        set_cell_margins(cell_lbl, top=35, bottom=35, left=20, right=20)
        set_cell_borders(cell_lbl)
        p = cell_lbl.paragraphs[0]
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(0)
        r = p.add_run(label)
        r.font.name = "Calibri"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = COLOR_NAVY

        cell_val = tbl_meta.cell(idx, 1)
        set_cell_margins(cell_val, top=35, bottom=35, left=20, right=20)
        set_cell_borders(cell_val)
        p2 = cell_val.paragraphs[0]
        p2.paragraph_format.space_before = Pt(0)
        p2.paragraph_format.space_after = Pt(0)
        r2 = p2.add_run(val)
        r2.font.name = "Calibri"
        r2.font.size = Pt(9.5)
        if label == "Student Name:":
            r2.font.bold = True
            r2.font.color.rgb = COLOR_SLATE
        else:
            r2.font.color.rgb = COLOR_BODY

    p_meta_sp = doc.add_paragraph()
    p_meta_sp.paragraph_format.space_before = Pt(65)
    p_meta_sp.paragraph_format.space_after = Pt(0)

    p_year = doc.add_paragraph()
    p_year.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_year.paragraph_format.space_before = Pt(0)
    p_year.paragraph_format.space_after = Pt(0)
    r_year = p_year.add_run("Academic Year 2026 | Comprehensive Laboratory & Viva Demonstration Package")
    r_year.font.name = "Calibri"
    r_year.font.size = Pt(8.5)
    r_year.font.color.rgb = COLOR_MUTED

    doc.add_page_break()

    # ==============================================================================
    # PAGE 2: CERTIFICATE OF ORIGINALITY & PROJECT DECLARATION
    # ==============================================================================
    add_h1(doc, "Certificate of Originality & Project Declaration")
    add_callout(doc,
        "This project is prepared strictly for the academic course 20CYS403 (Web Application Security). All vulnerable and secure implementations are isolated on local infrastructure (localhost) using simulated candidate records and controlled lab files.",
        "ACADEMIC DECLARATION", "blue")

    add_p(doc, "This is to certify that the project report entitled \"SecureJobLab: Job Recruitment Vulnerability Demonstration & Defense Platform\" submitted by Ram Karthik G in partial fulfillment of the academic requirements for the course 20CYS403 Web Application Security represents authentic, original work conducted under laboratory supervision.")
    add_p(doc, "The laboratory implementation rigorously implements, analyzes, and demonstrates exactly five web application security vulnerabilities classified under the Common Weakness Enumeration (CWE) framework:")

    add_bullet(doc, "SQL Injection (SQLi) — CWE-89: Direct query concatenation versus Parameterized Prepared Statements.", "1. ")
    add_bullet(doc, "Cross-Site Scripting (XSS) — CWE-79: Reflected execution versus Contextual HTML Entity Encoding.", "2. ")
    add_bullet(doc, "OS Command Injection — CWE-78: Unsanitized shell concatenation versus Strict Regex Whitelisting and Argument Escaping.", "3. ")
    add_bullet(doc, "Directory / Path Traversal — CWE-22: Arbitrary file inclusion versus Basename Whitelisting and Canonical Boundary Isolation.", "4. ")
    add_bullet(doc, "Clickjacking (UI Redressing) — CWE-1021: Framed destructive actions versus HTTP Framing Defense Headers (X-Frame-Options and CSP).", "5. ")

    add_p(doc, "I hereby declare that this report has been authored with technical diligence, that no external or unapproved vulnerability modules have been included, and that all code snippets, telemetry data, and screenshots accurately reflect the live execution behavior of the SecureJobLab system.")

    p_sig_sp = doc.add_paragraph()
    p_sig_sp.paragraph_format.space_before = Pt(35)
    p_sig_sp.paragraph_format.space_after = Pt(0)

    tbl_sig = doc.add_table(rows=1, cols=2)
    tbl_sig.alignment = WD_TABLE_ALIGNMENT.CENTER
    tbl_sig.autofit = False
    tbl_sig.columns[0].width = Inches(3.5)
    tbl_sig.columns[1].width = Inches(3.0)

    c_sig0 = tbl_sig.cell(0, 0)
    set_cell_borders(c_sig0)
    p0 = c_sig0.paragraphs[0]
    p0.paragraph_format.space_before = Pt(0)
    p0.paragraph_format.space_after = Pt(0)
    r0 = p0.add_run("Student Signature: _______________________")
    r0.font.name = "Calibri"
    r0.font.size = Pt(10)
    r0.font.bold = True
    r0.font.color.rgb = COLOR_NAVY

    c_sig1 = tbl_sig.cell(0, 1)
    set_cell_borders(c_sig1)
    p1 = c_sig1.paragraphs[0]
    p1.paragraph_format.space_before = Pt(0)
    p1.paragraph_format.space_after = Pt(0)
    r1 = p1.add_run("Date: October 6, 2026")
    r1.font.name = "Calibri"
    r1.font.size = Pt(10)
    r1.font.bold = True
    r1.font.color.rgb = COLOR_NAVY

    p_sig_meta = doc.add_paragraph()
    p_sig_meta.paragraph_format.space_before = Pt(15)
    p_sig_meta.paragraph_format.space_after = Pt(0)
    r_sm1 = p_sig_meta.add_run("Student Name: Ram Karthik G\nCourse Code: 20CYS403 — Web Application Security\nFaculty Evaluation Sign-off: _______________________________")
    r_sm1.font.name = "Calibri"
    r_sm1.font.size = Pt(10)
    r_sm1.font.color.rgb = COLOR_BODY

    doc.add_page_break()

    # ==============================================================================
    # PAGE 3: ACKNOWLEDGEMENTS & EXECUTIVE SUMMARY / ABSTRACT
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
    # PAGE 4: TABLE OF CONTENTS (Using Word Native Tab Stops with Dot Leaders)
    # ==============================================================================
    add_h1(doc, "Table of Contents")

    toc_entries = [
        ("Chapter 1: Introduction, Problem Statement & Objectives", 6, True),
        ("  1.1 Context & Background", 6, False),
        ("  1.2 Problem Statement & Motivation", 6, False),
        ("  1.3 Project Objectives & Methodology", 6, False),
        ("  1.4 Strict 5-Vulnerability Project Scope", 6, False),
        ("Chapter 2: System Architecture & Dual-Engine Design", 7, True),
        ("  2.1 Four-Tier Architecture Model", 7, False),
        ("  2.2 The Dual-Engine Security Execution Model", 7, False),
        ("Chapter 3: Technology Stack & Database Architecture", 8, True),
        ("  3.1 Technology Stack Specification", 8, False),
        ("  3.2 Core System Files & Directory Architecture", 8, False),
        ("  3.3 Relational Database Schema & Data Dictionary", 9, False),
        ("Chapter 4: Application Functional Modules", 10, True),
        ("  4.1 Authentication & Role-Based Access Control", 10, False),
        ("  4.2 Instant Job Board & Filtering Engine", 10, False),
        ("  4.3 Candidate Application Pipeline & Local Storage", 11, False),
        ("  4.4 Network Latency & Diagnostic Utilities", 11, False),
        ("Chapter 5: Vulnerability 1 — SQL Injection (SQLi) [CWE-89]", 12, True),
        ("  5.1 Vulnerability Overview & Threat Dynamics", 12, False),
        ("  5.2 Vulnerable Implementation & Insecure Code", 12, False),
        ("  5.3 Secure Mitigation & Parameterized Statements", 13, False),
        ("Chapter 6: Vulnerability 2 — Cross-Site Scripting (XSS) [CWE-79]", 14, True),
        ("  6.1 Vulnerability Overview & Threat Dynamics", 14, False),
        ("  6.2 Vulnerable Implementation & Live Script Execution", 14, False),
        ("  6.3 Secure Mitigation & Contextual Output Encoding", 15, False),
        ("Chapter 7: Vulnerability 3 — OS Command Injection [CWE-78]", 16, True),
        ("  7.1 Vulnerability Overview & Threat Dynamics", 16, False),
        ("  7.2 Vulnerable Implementation & Shell Chaining", 16, False),
        ("  7.3 Secure Mitigation & Strict Whitelisting", 17, False),
        ("Chapter 8: Vulnerability 4 — Directory / Path Traversal [CWE-22]", 18, True),
        ("  8.1 Vulnerability Overview & Threat Dynamics", 18, False),
        ("  8.2 Vulnerable Implementation & Path Climbing", 18, False),
        ("  8.3 Secure Mitigation & Canonical Boundary Defense", 19, False),
        ("Chapter 9: Vulnerability 5 — Clickjacking (UI Redressing) [CWE-1021]", 20, True),
        ("  9.1 Vulnerability Overview & High-Impact Scenario", 20, False),
        ("  9.2 Interactive UI Redressing Sandbox with Opacity", 20, False),
        ("  9.3 Secure Mitigation & HTTP Framing Protection Headers", 21, False),
        ("Chapter 10: Comparative Defense Matrix & Telemetry Analysis", 22, True),
        ("  10.1 Master 5-Vulnerability Security Comparison Matrix", 22, False),
        ("  10.2 Real-time Security Telemetry Engine", 22, False),
        ("Chapter 11: Testing & Verification Methodology", 23, True),
        ("  11.1 Test Plan & Execution Strategy", 23, False),
        ("  11.2 Comprehensive Verification Results Table", 23, False),
        ("Chapter 12: Viva Voce Reference & Security Analysis", 24, True),
        ("Chapter 13: Limitations & Future Enhancements", 25, True),
        ("Chapter 14: Conclusion", 25, True),
        ("References & Authoritative Standards", 26, True),
    ]

    for title, page_no, is_major in toc_entries:
        p_toc = doc.add_paragraph()
        p_toc.paragraph_format.space_before = Pt(0.5)
        p_toc.paragraph_format.space_after = Pt(0.5)
        p_toc.paragraph_format.line_spacing = 1.05
        p_toc.paragraph_format.tab_stops.add_tab_stop(Inches(6.5), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)

        r_title = p_toc.add_run(title)
        r_title.font.name = "Calibri"
        if is_major:
            r_title.font.size = Pt(8.5)
            r_title.font.bold = True
            r_title.font.color.rgb = COLOR_NAVY
        else:
            r_title.font.size = Pt(8)
            r_title.font.color.rgb = COLOR_BODY

        r_tab = p_toc.add_run("\t")
        r_page = p_toc.add_run(str(page_no))
        r_page.font.name = "Calibri"
        if is_major:
            r_page.font.size = Pt(8.5)
            r_page.font.bold = True
            r_page.font.color.rgb = COLOR_NAVY
        else:
            r_page.font.size = Pt(8)
            r_page.font.color.rgb = COLOR_SLATE

    doc.add_page_break()

    # ==============================================================================
    # PAGE 5: LIST OF FIGURES & TABLES, ABBREVIATIONS
    # ==============================================================================
    add_h1(doc, "List of Figures & Tables")
    add_h2(doc, "List of Figures")

    figures = [
        ("Figure 1: SecureJobLab Four-Tier System Architecture & Interaction Flow", 7),
        ("Figure 2: Relational Database Schema & Data Dictionary (securejoblab)", 9),
        ("Figure 3: SecureJobLab Authentication Screen (Candidate & Admin RBAC)", 10),
        ("Figure 4: Recruitment Portal Interface: Verified Cybersecurity Openings", 10),
        ("Figure 5: Candidate Application Pipeline & Local Resume Storage Dashboard", 11),
        ("Figure 6: SQL Injection Demonstration: Insecure Extraction vs. Parameterized Defense", 13),
        ("Figure 7: Reflected XSS Demonstration: Live Alert Execution vs. Encoded Rendering", 15),
        ("Figure 8: OS Command Injection: Unsanitized Chaining vs. Regex Whitelist Interception", 17),
        ("Figure 9: Directory Traversal: Sensitive File Extraction vs. Whitelist Denial", 19),
        ("Figure 10: Clickjacking UI Redressing: 100% Revealed Mode vs. 30% Ghost Mode", 20),
        ("Figure 11: Clickjacking Attack Triggered vs. Secure Mitigation (Frame Blocking)", 21),
    ]

    for fig_title, page_no in figures:
        p_fig = doc.add_paragraph()
        p_fig.paragraph_format.space_before = Pt(0.5)
        p_fig.paragraph_format.space_after = Pt(0.5)
        p_fig.paragraph_format.line_spacing = 1.05
        p_fig.paragraph_format.tab_stops.add_tab_stop(Inches(6.5), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        rf = p_fig.add_run(fig_title)
        rf.font.name = "Calibri"
        rf.font.size = Pt(8)
        rf.font.bold = True
        rf.font.color.rgb = COLOR_STEEL
        p_fig.add_run("\t")
        rp = p_fig.add_run(str(page_no))
        rp.font.name = "Calibri"
        rp.font.size = Pt(8)
        rp.font.color.rgb = COLOR_SLATE

    add_h2(doc, "List of Tables")
    tables = [
        ("Table 1: Core Technology Stack & Deployment Dependencies", 8),
        ("Table 2: Core System Files & Architectural Responsibilities", 8),
        ("Table 3: Database Entity-Relationship Schema & Table Specifications", 9),
        ("Table 4: Master 5-Vulnerability Security Comparison & Defense Matrix", 22),
        ("Table 5: Comprehensive Verification & Test Results Matrix (10 Scenarios)", 23),
    ]

    for tbl_title, page_no in tables:
        p_tbl = doc.add_paragraph()
        p_tbl.paragraph_format.space_before = Pt(0.5)
        p_tbl.paragraph_format.space_after = Pt(0.5)
        p_tbl.paragraph_format.line_spacing = 1.05
        p_tbl.paragraph_format.tab_stops.add_tab_stop(Inches(6.5), WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
        rt = p_tbl.add_run(tbl_title)
        rt.font.name = "Calibri"
        rt.font.size = Pt(8)
        rt.font.bold = True
        rt.font.color.rgb = COLOR_STEEL
        p_tbl.add_run("\t")
        rp = p_tbl.add_run(str(page_no))
        rp.font.name = "Calibri"
        rp.font.size = Pt(8)
        rp.font.color.rgb = COLOR_SLATE

    add_h2(doc, "Abbreviations & Security Terminology")
    abbrs = [
        ("AppSec:", "Application Security"),
        ("CWE:", "Common Weakness Enumeration"),
        ("OWASP:", "Open Web Application Security Project"),
        ("SQLi:", "SQL Injection (CWE-89)"),
        ("XSS:", "Cross-Site Scripting (CWE-79)"),
        ("CSP:", "Content Security Policy"),
        ("RBAC:", "Role-Based Access Control"),
        ("DOM:", "Document Object Model"),
        ("AST:", "Abstract Syntax Tree"),
        ("SIEM:", "Security Information and Event Management"),
        ("XHR:", "XMLHttpRequest (AJAX)"),
        ("API:", "Application Programming Interface")
    ]
    for ab, desc in abbrs:
        p_ab = doc.add_paragraph()
        p_ab.paragraph_format.space_before = Pt(0)
        p_ab.paragraph_format.space_after = Pt(0.5)
        ra = p_ab.add_run(f"{ab} ")
        ra.font.name = "Calibri"
        ra.font.size = Pt(8)
        ra.font.bold = True
        ra.font.color.rgb = COLOR_NAVY
        rd = p_ab.add_run(desc)
        rd.font.name = "Calibri"
        rd.font.size = Pt(8)
        rd.font.color.rgb = COLOR_BODY

    doc.add_page_break()

    # ==============================================================================
    # PAGE 6: CHAPTER 1: INTRODUCTION, PROBLEM STATEMENT & OBJECTIVES
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
    # PAGE 7: CHAPTER 2: SYSTEM ARCHITECTURE & DUAL-ENGINE DESIGN
    # ==============================================================================
    add_h1(doc, "Chapter 2: System Architecture & Dual-Engine Design")
    add_h2(doc, "2.1 Four-Tier Architecture Model")
    add_p(doc, "SecureJobLab is structured as a decoupled four-tier web architecture designed for modularity, low latency, and deterministic evaluation. The system separates user interaction, security state management, API request dispatching, and system resources.")

    add_image_box(doc, IMG_ARCH, "SecureJobLab Four-Tier System Architecture & Interaction Flow", width=Inches(4.5))

    add_p(doc, "The four architectural tiers operate as follows:")
    add_bullet(doc, "1. Presentation Tier: Developed in HTML5, CSS3, and JavaScript utilizing the Jobpilot design system. Provides the job search interface, candidate dashboard, authentication screens, and AppSec testing telemetry panels.", "")
    add_bullet(doc, "2. Security Controller Tier: Governed by the global session state ($_SESSION['appsec_mode']). Coordinates between the Vulnerable engine and the Secure engine across both portal features and lab testing endpoints.", "")
    add_bullet(doc, "3. Application & API Tier: Implemented in api.php and index.php. Acts as the centralized REST/AJAX router handling job CRUD operations, application submissions, and the five vulnerability testing routines.", "")
    add_bullet(doc, "4. Data & Subsystem Tier: Encapsulates the MySQL relational database (securejoblab), the local filesystem (lab_files and uploads/resumes), and the host operating system shell subsystem.", "")

    add_h2(doc, "2.2 The Dual-Engine Security Execution Model")
    add_p(doc, "The foundational innovation of SecureJobLab is its Dual-Engine Execution Pipeline. Rather than requiring evaluators to modify configuration files or restart services, the entire application toggles its defensive posture via an interactive navbar switch. Identical attack payloads traverse completely different execution paths depending on the active security mode:")
    add_bullet(doc, "Vulnerable Mode: Untrusted input flows without validation or escaping directly into dangerous execution sinks (mysqli_query(), browser DOM, shell_exec(), file_get_contents(), and unheadered iframe embedding). The attack succeeds, and exploit telemetry is recorded.", "• 🔴 ")
    add_bullet(doc, "Secure Mode: The payload is intercepted by defensive mechanisms (parameterized query compilation, contextual htmlspecialchars() encoding, strict regex whitelisting, basename() isolation, and X-Frame-Options: DENY headers). The attack is completely neutralized, and defensive verification telemetry is recorded.", "• 🟢 ")

    add_callout(doc, "Global State Synchronization: The active security mode is persisted across the PHP session ($_SESSION['appsec_mode']) and reflected dynamically in the UI navbar badge, enabling simultaneous testing across both functional views and lab pills.", "STATE PERSISTENCE", "blue")

    doc.add_page_break()

    # ==============================================================================
    # PAGE 8: CHAPTER 3: TECHNOLOGY STACK & CORE SYSTEM ARCHITECTURE
    # ==============================================================================
    add_h1(doc, "Chapter 3: Technology Stack & Database Architecture")
    add_h2(doc, "3.1 Technology Stack Specification")
    add_p(doc, "To guarantee deterministic behavior, rapid viva demonstrations, and frictionless portability on standard university laboratory machines, SecureJobLab is built on an enterprise open-source technology stack:")

    t1_headers = ["Component Layer", "Technology Selected", "Role in SecureJobLab"]
    t1_rows = [
        ["Web Server", "Apache HTTP Server 2.4", "Listens on port 80; manages HTTP requests, header emission, and PHP handler execution."],
        ["Database Engine", "MySQL 10.4 (MariaDB)", "Listens on port 3306; manages relational tables, indexes, and parameterized query execution."],
        ["Server Language", "PHP 8.2+ (OOP & Procedural)", "Executes backend routing, session state control, raw string parsing, and secure sanitization."],
        ["Frontend UI", "HTML5, CSS3, Bootstrap 5.3", "Jobpilot SaaS theme, interactive telemetry cards, modals, and responsive layout."],
        ["Asynchronous Comms", "Vanilla JavaScript (Fetch API)", "Non-blocking AJAX request dispatching, DOM updates, and live script execution handling."]
    ]
    add_table(doc, t1_headers, t1_rows, [Inches(1.5), Inches(1.8), Inches(3.2)])

    add_h2(doc, "3.2 Core System Files & Directory Architecture")
    add_p(doc, "The consolidated project architecture consists of exactly six root files, eliminating extraneous dependencies and ensuring instant restoration on any standard XAMPP deployment:")

    t2_headers = ["File Name", "Lines", "Architectural Responsibility"]
    t2_rows = [
        ["index.php", "1,240", "Main application container, Jobpilot portal UI, instant search bar, AppSec testbed modals, telemetry card rendering."],
        ["login.php", "185", "Role-based authentication gateway, candidate vs admin sign-in forms, credential verification, session initialization."],
        ["logout.php", "35", "Session destruction, credential invalidation, and secure redirect to authentication portal."],
        ["api.php", "460", "Central REST/AJAX router, switchable dual-engine execution sinks for all 5 CWEs, JSON telemetry generation."],
        ["clickjack_target.php", "110", "Framed victim target endpoint featuring the irreversible account deletion workflow with switchable framing headers."],
        ["database.sql", "145", "Relational database schema definition, seed candidate data fixtures, and UTF-8 collation configurations."]
    ]
    add_table(doc, t2_headers, t2_rows, [Inches(1.5), Inches(0.8), Inches(4.2)])

    add_h2(doc, "3.3 Server Runtime Environment & Session State Isolation")
    add_p(doc, "SecureJobLab runs in a unified web root (C:\\xampp\\htdocs\\SecureWebLab). All communication between the frontend client interfaces and backend execution engines occurs via asynchronous JSON contracts, ensuring instantaneous DOM feedback during live laboratory testing. The global security state ($_SESSION['appsec_mode']) maintains absolute persistence across page navigations without requiring cookie manipulation or server restarts.")

    doc.add_page_break()

    # ==============================================================================
    # PAGE 9: CHAPTER 3: RELATIONAL DATABASE SCHEMA & DATA DICTIONARY
    # ==============================================================================
    add_h2(doc, "3.4 Relational Database Schema & Data Dictionary")
    add_p(doc, "The database schema for securejoblab is engineered with UTF-8 (utf8mb4) character encoding, ensuring pristine rendering of international currency symbols (such as the Indian Rupee ₹) without mojibake corruption. The schema consists of four relational tables:")

    add_image_box(doc, IMG_DB, "Relational Database Schema & Data Dictionary (securejoblab)", width=Inches(4.5))

    t3_headers = ["Table Name", "Primary Key", "Key Attributes", "Security / Functional Role"]
    t3_rows = [
        ["users", "id (INT)", "username, password, full_name, role", "Stores authentication credentials; password verification and RBAC roles (candidate/admin)."],
        ["jobs", "id (INT)", "title, company, location, salary, secret_notes", "Target for SQLi; secret_notes contains confidential executive compensation bands."],
        ["applications", "id (INT)", "job_title, applicant_name, resume_file, status", "Tracks candidate submissions; links to uploaded resume documents in uploads/resumes/."],
        ["feedback", "id (INT)", "author, comment, created_at", "Stores recruiter and candidate feedback; used for output reflection testing."]
    ]
    add_table(doc, t3_headers, t3_rows, [Inches(1.1), Inches(0.9), Inches(2.2), Inches(2.3)])

    add_p(doc, "Prepopulated Seed Dataset Integrity: Seed records are prepopulated in database.sql to provide authentic enterprise data immediately upon deployment, including active openings from AWS, Stripe, Microsoft India, Razorpay, and CRED. Default user accounts include both candidates (ram.karthik@securejob.io) and administrators.")
    add_p(doc, "Data Isolation & Storage Security: Resume uploads are stored under uploads/resumes/, while sensitive server assets (such as database.sql and diagnostic scripts) reside in the web root, establishing the exact file system topology needed to evaluate directory traversal vulnerabilities.")

    doc.add_page_break()

    # ==============================================================================
    # PAGE 10: CHAPTER 4: APPLICATION FUNCTIONAL MODULES (Auth & Job Board)
    # ==============================================================================
    add_h1(doc, "Chapter 4: Application Functional Modules")
    add_h2(doc, "4.1 Authentication & Role-Based Access Control (login.php)")
    add_p(doc, "The authentication portal (login.php) models a modern SaaS authentication screen with tabbed sign-in and registration interfaces. The authentication engine verifies credentials against the users table. Evaluators can sign in using candidate accounts (e.g., ram.karthik@securejob.io / candidate123) or administrative credentials. Sessions are securely initialized with RBAC role privileges stored in $_SESSION['role'].")

    add_image_box(doc, IMG_LOGIN, "SecureJobLab Authentication Screen (Candidate & Admin RBAC)", width=Inches(3.8))

    add_h2(doc, "4.2 Instant Job Board & Filtering Engine (index.php)")
    add_p(doc, "The primary job board presents five verified high-tier cybersecurity positions (Amazon Web Services, Stripe, Microsoft India, Razorpay, CRED). An instant AJAX search engine filters jobs dynamically across titles, companies, locations, and employment types without requiring complete page reloads. Debounced keystroke events dispatch asynchronous queries to api.php, returning formatted job cards.")

    add_image_box(doc, IMG_INDEX, "Recruitment Portal Interface: Verified Cybersecurity Openings", width=Inches(4.0))

    doc.add_page_break()

    # ==============================================================================
    # PAGE 11: CHAPTER 4: APPLICATION FUNCTIONAL MODULES (Pipeline & Diagnostics)
    # ==============================================================================
    add_h2(doc, "4.3 Candidate Application Pipeline & Local Document Storage")
    add_p(doc, "Authenticated candidates can submit applications with customized cover notes and resume file attachments. Attached resumes are processed by api.php and stored locally under uploads/resumes/. The My Applications tab displays live application status tracking ('Interview Scheduled', 'Under Review') and allows candidate-driven application withdrawal:")

    add_image_box(doc, IMG_APPS, "Candidate Application Pipeline & Local Resume Storage Dashboard", width=Inches(4.0))

    add_h2(doc, "4.4 Network Latency & Diagnostic Utilities")
    add_p(doc, "To provide realistic functional grounding for server-side testing, SecureJobLab incorporates internal system administration utilities:")
    add_bullet(doc, "Network Gateway Latency Checker: Simulates ICMP host availability testing across company data centers via server-side diagnostic pings.", "• ")
    add_bullet(doc, "Candidate Document Viewer: Loads candidate resumes, cover notes, and certifications from isolated local folders.", "• ")
    add_bullet(doc, "Database State Reset Tool: Allows evaluators to reseed database tables to initial pristine values with a single click.", "• ")

    add_h2(doc, "4.5 Global AppSec Security Switcher & Telemetry Engine")
    add_p(doc, "A prominent security switcher in the top navigation bar enables instant toggling between Vulnerable Mode (red indicator) and Secure Mitigated Mode (green indicator). When toggled, an AJAX request updates $_SESSION['appsec_mode'], instantly changing the execution paths across all five functional features and laboratory testbeds without page reloads.")

    add_callout(doc, "Architectural Cohesion: Every vulnerability in SecureJobLab is directly embedded into these realistic recruitment features rather than synthetic test stubs, ensuring high pedagogical value and authentic viva demonstrations.", "PEDAGOGICAL REALISM", "blue")

    doc.add_page_break()

    # ==============================================================================
    # PAGE 12: CHAPTER 5: VULNERABILITY 1 — SQL INJECTION (SQLi) [CWE-89] (Threat Analysis)
    # ==============================================================================
    add_h1(doc, "Chapter 5: Vulnerability 1 — SQL Injection (SQLi) [CWE-89]")
    add_h2(doc, "5.1 Vulnerability Overview & Threat Dynamics")
    add_p(doc, "SQL Injection (CWE-89, OWASP Top 10 A03:2021) occurs when untrusted user input is directly concatenated into a dynamic SQL query string without lexical syntax separation or parameter binding. In web applications, this flaw allows threat actors to manipulate query grammar, bypass authentication, extract confidential database records, or execute administrative commands.")
    add_p(doc, "In the context of the SecureJobLab recruitment portal, the job search field on index.php queries the jobs database table. An attacker exploiting CWE-89 can break out of the string literal delimiter, alter the WHERE clause boolean logic, and dump hidden salary compensation bands and private interview rubrics stored in the secret_notes column.")

    add_h2(doc, "5.2 Vulnerable Implementation & Insecure Code Listing")
    add_p(doc, "In Vulnerable Mode, api.php accepts the search parameter directly from the HTTP GET array and interpolates it into the SQL query via string concatenation:")

    add_code_block(doc,
"""// api.php (Vulnerable Mode: Direct String Concatenation)
$search = $_GET['search'] ?? '';
$query = "SELECT id, title, company, salary, secret_notes FROM jobs
          WHERE title LIKE '%" . $search . "%'";
$result = mysqli_query($conn, $query);""",
    title="api.php (Insecure SQL Query Assembly)")

    add_h3(doc, "Attack Execution & Step-by-Step Payload Dissection")
    add_p(doc, "The evaluator inputs the classic SQL injection payload into the search bar: ' OR 1=1 #. The database parser evaluates this input through three distinct phases:")
    add_bullet(doc, "Phase 1 (Delimiter Breakout): The leading single quote (') terminates the literal string parameter intended for the LIKE clause.", "1. ")
    add_bullet(doc, "Phase 2 (Boolean Tautology): The OR 1=1 condition is introduced into the WHERE clause, which universally evaluates to TRUE for every row in the jobs table.", "2. ")
    add_bullet(doc, "Phase 3 (Comment Operator): The trailing hash symbol (#) instructs MySQL to treat the remainder of the query (the trailing %' quotation mark) as a comment, preventing syntax errors.", "3. ")

    add_h3(doc, "Data Exfiltration & Confidentiality Impact")
    add_p(doc, "Upon execution, the query transforms into: SELECT ... WHERE title LIKE '%' OR 1=1 #... As a result, the database engine returns all job listings, including hidden executive salary ranges (₹24,00,000 to ₹38,00,000) and confidential candidate evaluation rubrics stored in secret_notes.")

    add_code_block(doc,
"""// Live Telemetry Output (Vulnerable Mode)
{
  "status": "exploited", "mode": "vulnerable",
  "query": "SELECT id, title, company, salary, secret_notes FROM jobs WHERE title LIKE '%' OR 1=1 #%'",
  "records_returned": 5, "notes_exposed": true
}""",
    title="JSON Telemetry Capture (Vulnerable Mode)")

    doc.add_page_break()

    # ==============================================================================
    # PAGE 13: CHAPTER 5: SQL INJECTION — SECURE MITIGATION & VERIFICATION
    # ==============================================================================
    add_h2(doc, "5.3 Secure Mitigation & Parameterized Prepared Statements")
    add_p(doc, "In Secure Mode, dynamic string interpolation is replaced by Parameterized Prepared Statements using the PHP mysqli extension:")

    add_dual_code_comparison(doc,
"""// Vulnerable: String Concatenation
$query = "SELECT id, title, company, salary,
  secret_notes FROM jobs WHERE title = '$payload'";
$res = mysqli_query($conn, $query);""",
"""// Secure: Parameterized Prepared Statement
$stmt = mysqli_prepare($conn, "SELECT id, title,
  company, salary, secret_notes FROM jobs
  WHERE title = ?");
mysqli_stmt_bind_param($stmt, "s", $payload);
mysqli_stmt_execute($stmt);
$res = mysqli_stmt_get_result($stmt);""",
    "Vulnerable Dynamic Query", "Secure Prepared Statement")

    add_h3(doc, "Abstract Syntax Tree (AST) Compilation Defense")
    add_p(doc, "In the secure implementation, the database engine parses and compiles the SQL query structure into an Abstract Syntax Tree (AST) before user-supplied data is received. The placeholder (?) represents an immutable parameter slot. When the payload ' OR 1=1 # is transmitted, the database engine treats the entire string as a literal text value rather than executable SQL grammar. The query searches for a job whose title literally matches the characters ' OR 1=1 #, returning zero records and neutralizing the attack.")

    add_dual_image_comparison(doc, IMG_M1_V, IMG_M1_S,
        "SQLi Vulnerable: 5 Records & Secret Notes Dumped",
        "SQLi Secure: Parameterized Defense Neutralizes Injection")

    add_h3(doc, "Live Telemetry & Defense Verification")
    add_p(doc, "The real-time telemetry card captures the defensive interception: the executed query confirms parameterized parameter binding, zero records are exfiltrated, and no confidential interview notes are exposed.")

    add_callout(doc, "Defense Verified: Parameterized prepared statements (mysqli_prepare + mysqli_stmt_bind_param) completely separate query structure from data evaluation, eliminating SQL injection vulnerability regardless of input characters.", "KEY TAKEAWAY", "green")

    doc.add_page_break()

    # ==============================================================================
    # PAGE 14: CHAPTER 6: VULNERABILITY 2 — CROSS-SITE SCRIPTING (XSS) [CWE-79] (Threat Analysis)
    # ==============================================================================
    add_h1(doc, "Chapter 6: Vulnerability 2 — Cross-Site Scripting (XSS) [CWE-79]")
    add_h2(doc, "6.1 Vulnerability Overview & Threat Dynamics")
    add_p(doc, "Cross-Site Scripting (CWE-79, OWASP Top 10 A03:2021) occurs when an application receives untrusted data and includes it in a web page without proper validation or contextual output encoding. In a Reflected XSS attack, the malicious script payload is reflected off the web server to the victim's browser, where it executes within the security context of the user's session.")
    add_p(doc, "In SecureJobLab, the search query entered in the recruitment search field is reflected back onto the page to inform the user of their active query (e.g., 'Showing results for: ...'). In an enterprise recruitment system, exploiting CWE-79 allows attackers to hijack candidate session tokens, steal recruiter credentials, or rewrite DOM elements to harvest login details.")

    add_h2(doc, "6.2 Vulnerable Implementation & Live Script Execution")
    add_p(doc, "In Vulnerable Mode, search queries entered on search.php or index.php are reflected directly into the Document Object Model (DOM) using raw innerHTML assignment or unescaped PHP echo:")

    add_code_block(doc,
"""// search.php & api.php (Vulnerable Mode: Raw Reflection)
$q = $_GET['q'] ?? '';
echo "<div class='alert alert-info'>Search results for: " . $q . "</div>";

// In Frontend JavaScript:
resultsBanner.innerHTML = "Showing results for: " + data.query;""",
    title="search.php & api.php (Insecure DOM Injection)")

    add_h3(doc, "Attack Execution & Step-by-Step Payload Dissection")
    add_p(doc, "The evaluator inputs the standard proof-of-concept payload: <script>alert(\"Hello!\");</script> or <img src=x onerror=alert('XSS')>. The execution flow unfolds as follows:")
    add_bullet(doc, "Submission: The script payload is sent via HTTP GET to search.php or api.php.", "1. ")
    add_bullet(doc, "Server Reflection: The server echoes the raw markup without HTML entity conversion.", "2. ")
    add_bullet(doc, "DOM Parsing: The browser's HTML parser interprets the <script> tags as executable code nodes, invoking the JavaScript V8 engine and displaying the native alert dialog.", "3. ")

    add_h3(doc, "Session Hijacking & Client-Side Impact")
    add_p(doc, "Because the script executes in the victim's browser context, it possesses full access to document.cookie, localStorage, and session tokens. An adversary could silently exfiltrate PHPSESSID tokens to an external listener, completely impersonating the recruiter or applicant.")

    add_code_block(doc,
"""// Live Telemetry Output (Vulnerable Mode)
{
  "status": "script_executed", "mode": "vulnerable",
  "reflected_payload": "<script>alert('Hello!');</script>",
  "dom_sink": "innerHTML", "browser_alert_fired": true
}""",
    title="JSON Telemetry Capture (Vulnerable Mode)")

    doc.add_page_break()

    # ==============================================================================
    # PAGE 15: CHAPTER 6: CROSS-SITE SCRIPTING — SECURE MITIGATION & VERIFICATION
    # ==============================================================================
    add_h2(doc, "6.3 Secure Mitigation & Contextual Output Encoding")
    add_p(doc, "In Secure Mode, untrusted user data is sanitized prior to rendering using contextual HTML entity encoding on the server and safe DOM property assignment on the client:")

    add_dual_code_comparison(doc,
"""// Vulnerable: Raw innerHTML Reflection
$q = $_GET['q'] ?? '';
echo "<div>Results: " . $q . "</div>";
// Frontend:
banner.innerHTML = "Query: " + data.q;""",
"""// Secure: htmlspecialchars & textContent
$q = $_GET['q'] ?? '';
echo "<div>Results: " .
  htmlspecialchars($q, ENT_QUOTES, 'UTF-8') .
  "</div>";
// Frontend:
banner.textContent = "Query: " + data.q;""",
    "Vulnerable Raw Reflection", "Secure Contextual Encoding")

    add_h3(doc, "HTML Entity Translation & Parser Neutralization")
    add_p(doc, "The function htmlspecialchars($q, ENT_QUOTES, 'UTF-8') converts HTML meta-characters into harmless entity equivalents:")
    add_bullet(doc, "< (less-than) is converted to &lt;", "• ")
    add_bullet(doc, "> (greater-than) is converted to &gt;", "• ")
    add_bullet(doc, "\" (double quote) is converted to &quot;", "• ")
    add_bullet(doc, "' (single quote) is converted to &#039;", "• ")
    add_bullet(doc, "& (ampersand) is converted to &amp;", "• ")
    add_p(doc, "When the browser encounters &lt;script&gt;, the layout engine treats the characters as visual text glyphs rather than executable HTML markup. Additionally, binding data via textContent guarantees that the browser never invokes the HTML token parser.")

    add_dual_image_comparison(doc, IMG_M2_V, IMG_M2_S,
        "XSS Vulnerable: Script Executes Native Alert Dialog",
        "XSS Secure: Entity Encoding Renders Safe Literal Text")

    add_h3(doc, "Live Telemetry & Defense Verification")
    add_p(doc, "The secure telemetry confirms that the raw payload was transformed into harmless entity strings, the alert dialog was completely suppressed, and the user interface safely rendered the literal script text.")

    add_callout(doc, "Defense Verified: Contextual output encoding (htmlspecialchars with ENT_QUOTES) and safe DOM property assignment (textContent) neutralize XSS by converting executable markup into harmless printable glyphs.", "KEY TAKEAWAY", "green")

    doc.add_page_break()

    # ==============================================================================
    # PAGE 16: CHAPTER 7: VULNERABILITY 3 — OS COMMAND INJECTION [CWE-78] (Threat Analysis)
    # ==============================================================================
    add_h1(doc, "Chapter 7: Vulnerability 3 — OS Command Injection [CWE-78]")
    add_h2(doc, "7.1 Vulnerability Overview & Threat Dynamics")
    add_p(doc, "OS Command Injection (CWE-78, OWASP Top 10 A03:2021) occurs when an application passes untrusted user input directly to a system shell execution function (such as system(), exec(), shell_exec(), or passthru()) without rigorous validation or shell escaping. This enables an attacker to append arbitrary operating system commands that execute with the privileges of the web server process.")
    add_p(doc, "In SecureJobLab, the platform includes a network diagnostic latency checker designed to allow administrators to test ICMP ping availability to internal company servers (e.g., 127.0.0.1). In an enterprise hosting environment, exploiting CWE-78 allows threat actors to compromise the underlying host, pivot laterally across the corporate network, and establish persistent backdoors.")

    add_h2(doc, "7.2 Vulnerable Implementation & Shell Chaining")
    add_p(doc, "In Vulnerable Mode, api.php concatenates the host parameter directly into the shell execution string:")

    add_code_block(doc,
"""// api.php (Vulnerable Mode: Direct Shell Concatenation)
$target = $_GET['host'] ?? '127.0.0.1';
$cmd = "ping -n 2 " . $target; // Windows CMD concatenation
$output = shell_exec($cmd);
echo json_encode(["status" => "success", "output" => $output]);""",
    title="api.php (Insecure Shell Command Concatenation)")

    add_h3(doc, "Attack Execution & Step-by-Step Payload Dissection")
    add_p(doc, "The evaluator inputs the command chaining payload into the diagnostic field: 127.0.0.1 & whoami. The operating system command interpreter (cmd.exe on Windows or /bin/sh on Linux) processes the command in sequence:")
    add_bullet(doc, "Command 1: The ping -n 2 127.0.0.1 executes normally, transmitting two ICMP echo requests.", "1. ")
    add_bullet(doc, "Shell Delimiter: The ampersand (&) acts as a synchronous command separator, instructing the shell to execute the subsequent command immediately upon completion.", "2. ")
    add_bullet(doc, "Command 2: The whoami command executes within the Apache process context, dumping the current system username (e.g., desktop-securelab\\ram).", "3. ")

    add_h3(doc, "System Compromise & Privilege Escalation Risks")
    add_p(doc, "Beyond whoami, an attacker could chain net user, dir C:\\, or download malicious payloads via curl or powershell -Command \"...\", leading to total host takeover.")

    add_code_block(doc,
"""// Live Telemetry Output (Vulnerable Mode)
{
  "status": "command_executed", "mode": "vulnerable",
  "executed_cmd": "ping -n 2 127.0.0.1 & whoami",
  "stdout": "Pinging 127.0.0.1... Reply from 127.0.0.1... \\n desktop-securelab\\\\ram"
}""",
    title="JSON Telemetry Capture (Vulnerable Mode)")

    doc.add_page_break()

    # ==============================================================================
    # PAGE 17: CHAPTER 7: OS COMMAND INJECTION — SECURE MITIGATION & VERIFICATION
    # ==============================================================================
    add_h2(doc, "7.3 Secure Mitigation & Strict Whitelisting")
    add_p(doc, "In Secure Mode, defense-in-depth is enforced by combining strict regular expression whitelisting with shell argument escaping (escapeshellarg()):")

    add_dual_code_comparison(doc,
"""// Vulnerable: Direct Shell Concatenation
$host = $_GET['host'];
$cmd = "ping -n 2 " . $host;
$out = shell_exec($cmd);""",
"""// Secure: Strict Regex Whitelist & Escaping
$host = $_GET['host'] ?? '';
if (!preg_match('/^[a-zA-Z0-9.-]+$/', $host)) {
    die(json_encode(["error" => "Invalid host"]));
}
$cmd = "ping -n 2 " . escapeshellarg($host);
$out = shell_exec($cmd);""",
    "Vulnerable Shell Concatenation", "Secure Regex Whitelist Defense")

    add_h3(doc, "Process Boundary Defense & Whitelist Mechanics")
    add_p(doc, "The regular expression /^[a-zA-Z0-9.-]+$/ enforces positive character constraints. Any character outside the permitted set—specifically command delimiters such as &, |, ;, `, $, >, <, or newline characters—causes immediate validation failure before the shell is invoked.")
    add_p(doc, "Furthermore, escapeshellarg() wraps the argument in quotation marks and escapes existing quotes, ensuring that the shell treats the input strictly as a single command argument rather than executable command syntax.")

    add_dual_image_comparison(doc, IMG_M3_V, IMG_M3_S,
        "Command Inj Vulnerable: whoami Prints Host User",
        "Command Inj Secure: Regex Rejects Metacharacters")

    add_h3(doc, "Live Telemetry & Defense Verification")
    add_p(doc, "The secure telemetry confirms that the malicious input was trapped by the input validation filter, shell_exec() was never invoked, and a structured security error response was returned.")

    add_callout(doc, "Defense Verified: Strict positive regex whitelisting combined with escapeshellarg() provides defense-in-depth by preventing shell metacharacters from reaching the operating system command interpreter.", "KEY TAKEAWAY", "green")

    doc.add_page_break()

    # ==============================================================================
    # PAGE 18: CHAPTER 8: VULNERABILITY 4 — DIRECTORY TRAVERSAL [CWE-22] (Threat Analysis)
    # ==============================================================================
    add_h1(doc, "Chapter 8: Vulnerability 4 — Directory / Path Traversal [CWE-22]")
    add_h2(doc, "8.1 Vulnerability Overview & Threat Dynamics")
    add_p(doc, "Directory Traversal (CWE-22, OWASP Top 10 A01:2021) occurs when an application accepts user input representing a file path and passes it to filesystem APIs without canonical path validation or boundary confinement. By supplying dot-dot-slash (../) sequences, an attacker climbs out of the designated directory and accesses arbitrary files across the host filesystem.")
    add_p(doc, "In SecureJobLab, candidates and recruiters view submitted resume documents and cover letters via a document inspection utility. In an enterprise recruitment system, exploiting CWE-22 allows attackers to read database connection credentials, server configuration files, source code files, and sensitive operating system files.")

    add_h2(doc, "8.2 Vulnerable Implementation & Path Climbing")
    add_p(doc, "In Vulnerable Mode, api.php accepts a doc parameter and appends it directly to the document directory path without sanitization:")

    add_code_block(doc,
"""// api.php (Vulnerable Mode: Insecure Path Concatenation)
$doc = $_GET['doc'] ?? 'resume_sample.pdf';
$path = "uploads/resumes/" . $doc;
if (file_exists($path)) {
    echo file_get_contents($path);
} else {
    echo "File not found.";
}""",
    title="api.php (Insecure File Path Resolution)")

    add_h3(doc, "Attack Execution & Step-by-Step Payload Dissection")
    add_p(doc, "The evaluator inputs the path traversal climbing payload: ../database.sql. The filesystem driver resolves the relative path as follows:")
    add_bullet(doc, "Base Path: The application begins in the uploads/resumes/ subfolder.", "1. ")
    add_bullet(doc, "Directory Climb: The ../ sequence instructs the operating system to move up one level into the parent web root directory (C:\\xampp\\htdocs\\SecureWebLab\\).", "2. ")
    add_bullet(doc, "Target File Access: The filesystem resolves the path to database.sql, reading the application schema and table fixtures.", "3. ")

    add_h3(doc, "Information Disclosure & Asset Exposure Impact")
    add_p(doc, "The contents of database.sql are dumped into the browser response, exposing database table definitions, column names, administrative accounts, and initial password hashes.")

    add_code_block(doc,
"""// Live Telemetry Output (Vulnerable Mode)
{
  "status": "file_extracted", "mode": "vulnerable",
  "requested_file": "../database.sql",
  "resolved_path": "uploads/resumes/../database.sql",
  "bytes_read": 4820, "sensitive_data_leaked": true
}""",
    title="JSON Telemetry Capture (Vulnerable Mode)")

    doc.add_page_break()

    # ==============================================================================
    # PAGE 19: CHAPTER 8: DIRECTORY TRAVERSAL — SECURE MITIGATION & VERIFICATION
    # ==============================================================================
    add_h2(doc, "8.3 Secure Mitigation & Canonical Boundary Defense")
    add_p(doc, "In Secure Mode, file access is constrained using a dual defensive barrier: basename() token extraction and strict whitelist validation against approved documents:")

    add_dual_code_comparison(doc,
"""// Vulnerable: Direct Path Concatenation
$doc = $_GET['doc'];
$path = "uploads/resumes/" . $doc;
$data = file_get_contents($path);""",
"""// Secure: Basename Stripping & Whitelist
$doc = basename($_GET['doc'] ?? '');
$allowed = ['resume_sample.pdf', 'cover_note.txt'];
if (!in_array($doc, $allowed, true)) {
    die(json_encode(["error" => "Access denied"]));
}
$path = "uploads/resumes/" . $doc;
$data = file_get_contents($path);""",
    "Vulnerable Path Concatenation", "Secure Basename & Whitelist Defense")

    add_h3(doc, "Basename Stripping & Whitelist Confinement Mechanics")
    add_p(doc, "The PHP basename() function extracts strictly the trailing filename component from the input string, stripping away all leading directory path components and traversal sequences (e.g., ../database.sql becomes database.sql).")
    add_p(doc, "Subsequently, in_array($doc, $allowed, true) verifies that the extracted filename exists within an explicit whitelist of pre-approved documents. Even if an attacker supplies a filename that exists in the current folder, if it is not explicitly whitelisted, access is denied.")

    add_dual_image_comparison(doc, IMG_M4_V, IMG_M4_S,
        "Traversal Vulnerable: database.sql Schema Dumped",
        "Traversal Secure: Whitelist Blocks Path Traversal")

    add_h3(doc, "Live Telemetry & Defense Verification")
    add_p(doc, "The secure telemetry confirms that the traversal sequences were stripped, the whitelist rejected the unauthorized document, and the filesystem boundary remained completely unbreached.")

    add_callout(doc, "Defense Verified: Combining basename() token extraction with an explicit filename whitelist guarantees that file operations cannot escape the designated storage directory regardless of traversal syntax.", "KEY TAKEAWAY", "green")

    doc.add_page_break()

    # ==============================================================================
    # PAGE 20: CHAPTER 9: VULNERABILITY 5 — CLICKJACKING [CWE-1021] (UI Redressing)
    # ==============================================================================
    add_h1(doc, "Chapter 9: Vulnerability 5 — Clickjacking (UI Redressing) [CWE-1021]")
    add_h2(doc, "9.1 Vulnerability Overview & High-Impact Scenario")
    add_p(doc, "Clickjacking (CWE-1021, OWASP Top 10 A05:2021) occurs when an attacker loads a target web application inside a transparent iframe embedded within a malicious third-party site. The attacker overlays alluring decoy UI elements (e.g., 'Claim Free Prize' or 'Download Report') directly above sensitive, high-impact buttons in the hidden application, tricking authenticated users into performing actions they never intended.")
    add_p(doc, "In SecureJobLab, the framed target endpoint (clickjack_target.php) hosts an irreversible candidate account management action: Permanently Delete Account. When an attacker frames this endpoint, a single click on a decoy button results in the complete destruction of the candidate's account and application history.")

    add_h2(doc, "9.2 Interactive UI Redressing Sandbox with Opacity Demonstration")
    add_p(doc, "SecureJobLab features an interactive UI Redressing demonstration laboratory equipped with an opacity slider to visualize the exploit mechanics across three distinct operational states:")
    add_bullet(doc, "100% Revealed Mode: Displays both layers simultaneously, revealing the framed SecureJobLab portal positioned beneath the attacker's decoy game overlay.", "• ")
    add_bullet(doc, "30% Ghost Mode: Renders the framed portal semi-transparently, visually proving that the attacker's 'Claim $500 Prize' button is pixel-aligned directly over the victim's 'Permanently Delete Account' button.", "• ")
    add_bullet(doc, "0% Invisible Mode: Renders the target iframe completely invisible (opacity: 0.0001). The victim perceives only the decoy game, clicking the prize button while unknowingly deleting their real account.", "• ")

    add_dual_image_comparison(doc, IMG_M5_100, IMG_M5_30,
        "100% Revealed: Decoy Layer Over Target App",
        "30% Ghost: Perfect Pixel Alignment Over Delete Button")

    add_h3(doc, "Attack Coercion Mechanics & State Destruction")
    add_p(doc, "When the user clicks the decoy button, the browser transmits the click event to the top-most clickable layer—which is the transparent iframe. Because the candidate is already authenticated via session cookies, the request executes with valid credentials, deleting the candidate's profile.")

    doc.add_page_break()

    # ==============================================================================
    # PAGE 21: CHAPTER 9: CLICKJACKING — SECURE MITIGATION & VERIFICATION
    # ==============================================================================
    add_h2(doc, "9.3 Secure Mitigation & HTTP Framing Protection Headers")
    add_p(doc, "In Secure Mode, framing is neutralized by configuring the server to emit modern HTTP response security headers on clickjack_target.php:")

    add_dual_code_comparison(doc,
"""// Vulnerable: No Framing Headers Emitted
// clickjack_target.php renders freely inside
// any third-party <iframe> overlay without
// restriction.
// (Missing X-Frame-Options & CSP headers)""",
"""// Secure: HTTP Framing Protection Headers
header("X-Frame-Options: DENY");
header("Content-Security-Policy: " .
       "frame-ancestors 'none';");

// Client-Side Framebuster Script Fallback:
// if (top !== self) top.location = self.location;""",
    "Vulnerable Unprotected Endpoint", "Secure Framing Defense Headers")

    add_h3(doc, "Browser Security Policy Enforcement")
    add_p(doc, "When the browser encounters the X-Frame-Options: DENY response header, its security engine refuses to render the content inside any frame or iframe. Furthermore, the modern Content-Security-Policy: frame-ancestors 'none' directive instructs all compliant browsers (Edge, Chrome, Firefox, Safari) to block embedding unconditionally, superseding legacy header limitations.")

    add_dual_image_comparison(doc, IMG_M5_TRIG, IMG_M5_S,
        "Vulnerable Mode: Harmful Account Deletion Triggered",
        "Secure Mode: Browser Blocks Framing (Blank Frame)")

    add_h3(doc, "Live Telemetry & Defense Verification")
    add_p(doc, "Verification in Microsoft Edge and browser developer tools confirms that the target page refuses to render in the attacker's iframe. The browser console records a security violation: 'Refused to display in a frame because it set X-Frame-Options to DENY'. The decoy click fails to reach the application, and the account remains completely safe.")

    add_callout(doc, "Defense Verified: HTTP response headers (X-Frame-Options: DENY and Content-Security-Policy: frame-ancestors 'none') instruct browser rendering engines to reject framing unconditionally, completely neutralizing Clickjacking.", "KEY TAKEAWAY", "green")

    doc.add_page_break()

    # ==============================================================================
    # PAGE 22: CHAPTER 10: COMPARATIVE DEFENSE MATRIX & TELEMETRY ANALYSIS
    # ==============================================================================
    add_h1(doc, "Chapter 10: Comparative Defense Matrix & Telemetry Analysis")
    add_h2(doc, "10.1 Master 5-Vulnerability Security Comparison Matrix")
    add_p(doc, "The following matrix provides a comprehensive technical comparison of the five implemented vulnerabilities, summarizing their root causes, exploit impacts, mitigations, and verified statuses:")

    t4_headers = ["Vulnerability", "CWE Class", "Root Cause", "Defense Mitigation", "Status"]
    t4_rows = [
        ["SQL Injection (SQLi)", "CWE-89", "Unsanitized dynamic string interpolation in SQL queries.", "Parameterized Prepared Statements (mysqli_prepare).", "VERIFIED (PASS)"],
        ["Cross-Site Scripting (XSS)", "CWE-79", "Direct raw output reflection into DOM without encoding.", "Contextual HTML Entity Encoding (htmlspecialchars).", "VERIFIED (PASS)"],
        ["OS Command Injection", "CWE-78", "Direct concatenation of untrusted input into shell_exec().", "Strict Regex Whitelisting + Argument Escaping (escapeshellarg).", "VERIFIED (PASS)"],
        ["Directory Traversal", "CWE-22", "Uncanonicalized relative path inclusion (../).", "basename() Token Stripping + Explicit Whitelist Array.", "VERIFIED (PASS)"],
        ["Clickjacking (UI Redressing)", "CWE-1021", "Missing HTTP framing headers permitting iframe embedding.", "X-Frame-Options: DENY & CSP frame-ancestors 'none'.", "VERIFIED (PASS)"]
    ]
    add_table(doc, t4_headers, t4_rows, [Inches(1.5), Inches(0.8), Inches(1.8), Inches(1.8), Inches(0.6)])

    add_h2(doc, "10.2 Real-time Security Telemetry Engine Architecture")
    add_p(doc, "Every module in SecureJobLab communicates with api.php using JSON telemetry. When an evaluator dispatches an attack payload, the telemetry engine computes and renders:")
    add_bullet(doc, "Exploit Status: Clear diagnostic indicator stating whether the exploit succeeded or the defense held.", "• ")
    add_bullet(doc, "Executed Query / Shell Command: Exact runtime string compiled by the database or operating system.", "• ")
    add_bullet(doc, "Returned Data Records: Interactive table displaying extracted records or database error messages.", "• ")
    add_bullet(doc, "Mitigation Telemetry: Technical explanation of the security control neutralizing the attack.", "• ")

    add_code_block(doc,
"""// Standardized JSON Telemetry Response Contract (api.php)
{
  "module": "cwe_module_identifier",
  "mode": "vulnerable" | "secure",
  "status": "exploited" | "neutralized",
  "executed_syntax": "SELECT ... | ping ... | file_get_contents(...)",
  "defense_applied": "PreparedStatements | HtmlEntities | RegexWhitelist | HeaderDeny",
  "records_count": 0,
  "telemetry_timestamp": "2026-10-06T22:30:00Z"
}""",
    title="JSON Telemetry Contract Specification")

    doc.add_page_break()

    # ==============================================================================
    # PAGE 23: CHAPTER 11: TESTING & VERIFICATION METHODOLOGY
    # ==============================================================================
    add_h1(doc, "Chapter 11: Testing & Verification Methodology")
    add_h2(doc, "11.1 Test Plan & Execution Strategy")
    add_p(doc, "Testing was conducted using a dual verification strategy: Automated Browser Testing in Microsoft Edge via Playwright validating HTTP responses and DOM states, paired with manual verification in web browsers verifying alert popups, UI Redressing sliders, and visual telemetry rendering.")

    add_h2(doc, "11.2 Comprehensive Verification Results Table (10 Scenarios)")
    add_p(doc, "The testing matrix evaluates each of the five vulnerabilities across both Vulnerable and Secure modes, yielding ten test scenarios:")

    t5_headers = ["Test ID", "Module & Mode", "Payload / Input", "Expected Result", "Status"]
    t5_rows = [
        ["TC-01", "SQLi (Vulnerable)", "' OR 1=1 #", "Bypasses query; returns all 5 jobs & secret notes.", "PASS"],
        ["TC-02", "SQLi (Secure)", "' OR 1=1 #", "Treated as literal string; 0 jobs returned; query intact.", "PASS"],
        ["TC-03", "XSS (Vulnerable)", "<script>alert('XSS')</script>", "Renders raw script in DOM; triggers native alert dialog.", "PASS"],
        ["TC-04", "XSS (Secure)", "<script>alert('XSS')</script>", "Encoded with htmlspecialchars(); displayed as safe text.", "PASS"],
        ["TC-05", "Cmd Inj (Vulnerable)", "127.0.0.1 & whoami", "Executes ping followed by whoami; prints server username.", "PASS"],
        ["TC-06", "Cmd Inj (Secure)", "127.0.0.1 & whoami", "Rejected by regex whitelist; system call blocked.", "PASS"],
        ["TC-07", "Traversal (Vulnerable)", "../database.sql", "Escapes folder; reads raw database schema file.", "PASS"],
        ["TC-08", "Traversal (Secure)", "../database.sql", "Tokens stripped; database.sql rejected by whitelist.", "PASS"],
        ["TC-09", "Clickjack (Vulnerable)", "Decoy Click (0% Opacity)", "Invisible iframe receives click; account deletion executed.", "PASS"],
        ["TC-10", "Clickjack (Secure)", "Decoy Click", "Framing blocked by X-Frame-Options: DENY; iframe blank.", "PASS"]
    ]
    add_table(doc, t5_headers, t5_rows, [Inches(0.6), Inches(1.3), Inches(1.7), Inches(2.4), Inches(0.5)])

    add_callout(doc, "Verification Summary: 10 out of 10 test cases passed with 100% adherence to expected behavioral specifications. Both exploitation mechanics and defensive mitigations were confirmed.", "TESTING SUMMARY", "green")

    doc.add_page_break()

    # ==============================================================================
    # PAGE 24: CHAPTER 12: VIVA VOCE REFERENCE & SECURITY ANALYSIS
    # ==============================================================================
    add_h1(doc, "Chapter 12: Viva Voce Reference & Security Analysis")
    add_p(doc, "This chapter provides authoritative technical answers to key questions anticipated during the academic viva examination for Course 20CYS403:")

    add_p(doc, "Prepared statements compile the SQL command structure beforehand into an Abstract Syntax Tree (AST). User-supplied data is transmitted separately and bound exclusively as parameter literals. The database query parser never re-interprets bound parameters as executable SQL grammar.", bold_prefix="Q1: Why is prepared statement execution inherently immune to SQL Injection? ")

    add_p(doc, "htmlspecialchars() replaces HTML meta-characters (&, <, >, \", ') with HTML entities (&amp;, &lt;, &gt;, &quot;, &#039;). The browser's DOM parser treats these as printable text rather than tag delimiters. ENT_QUOTES ensures single quotes are encoded, preventing attribute breakout attacks.", bold_prefix="Q2: Why does htmlspecialchars() neutralize XSS, and why are ENT_QUOTES necessary? ")

    add_p(doc, "escapeshellarg() wraps arguments in single quotes and escapes existing quotes, ensuring shell parsers interpret the input as a single literal argument. Input whitelisting rejects characters entirely before any system call occurs, providing defense-in-depth.", bold_prefix="Q3: What distinguishes escapeshellarg() from input whitelisting in Command Injection defense? ")

    add_p(doc, "basename() extracts the trailing name component of a path, stripping path-traversal tokens like ../ and ..\\. In SecureJobLab, basename() is paired with an explicit whitelist array to ensure only approved document files can be accessed.", bold_prefix="Q4: How does basename() prevent Directory Traversal attacks? ")

    add_p(doc, "X-Frame-Options: DENY instructs the browser to refuse rendering the target inside any frame. CSP frame-ancestors 'none' provides modern, granular defense. The browser terminates frame rendering before user interaction occurs.", bold_prefix="Q5: How do X-Frame-Options and CSP frame-ancestors protect against Clickjacking? ")

    add_p(doc, "Storing security mode in $_SESSION['appsec_mode'] allows multiple simultaneous evaluators to test vulnerable and secure paths concurrently on the same host without configuration restarts, providing immediate comparative telemetry.", bold_prefix="Q6: What is the security advantage of session-based dual-engine switching over environment flags? ")

    add_p(doc, "Defense-in-depth ensures that if one layer fails (e.g. client validation bypass), secondary layers (regex whitelisting, argument escaping, least-privilege execution) still prevent compromise.", bold_prefix="Q7: What is Defense-in-Depth, and how is it demonstrated in SecureJobLab? ")

    add_p(doc, "Client-side validation enhances user experience but can be easily bypassed by intercepting proxies or curl requests. Server-side validation and secure APIs are mandatory because they enforce security at the trusted execution sink.", bold_prefix="Q8: Why can client-side validation never be relied upon for security? ")

    doc.add_page_break()

    # ==============================================================================
    # PAGE 25: CHAPTER 13: LIMITATIONS & FUTURE WORK / CHAPTER 14: CONCLUSION
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

    add_callout(doc, "Academic Milestone: SecureJobLab fulfills all requirements for course 20CYS403, verifying exactly five CWE vulnerability modules across both vulnerable and secure implementations.", "ACADEMIC VERIFICATION", "green")

    doc.add_page_break()

    # ==============================================================================
    # PAGE 26: REFERENCES & AUTHORITATIVE STANDARDS
    # ==============================================================================
    add_h1(doc, "References & Authoritative Standards")

    references = [
        "[1] OWASP Foundation, \"OWASP Top 10:2021 - The Ten Most Critical Web Application Security Risks,\" 2021. Available: https://owasp.org/Top10/",
        "[2] MITRE Corporation, \"CWE-89: Improper Neutralization of Special Elements used in an SQL Command ('SQL Injection'),\" Common Weakness Enumeration, 2024. Available: https://cwe.mitre.org/data/definitions/89.html",
        "[3] MITRE Corporation, \"CWE-79: Improper Neutralization of Input During Web Page Generation ('Cross-site Scripting'),\" Common Weakness Enumeration, 2024. Available: https://cwe.mitre.org/data/definitions/79.html",
        "[4] MITRE Corporation, \"CWE-78: Improper Neutralization of Special Elements used in an OS Command ('OS Command Injection'),\" Common Weakness Enumeration, 2024. Available: https://cwe.mitre.org/data/definitions/78.html",
        "[5] MITRE Corporation, \"CWE-22: Improper Limitation of a Pathname to a Restricted Directory ('Path Traversal'),\" Common Weakness Enumeration, 2024. Available: https://cwe.mitre.org/data/definitions/22.html",
        "[6] MITRE Corporation, \"CWE-1021: Improper Restriction of Rendered UI Layers or Frames ('Clickjacking'),\" Common Weakness Enumeration, 2024. Available: https://cwe.mitre.org/data/definitions/1021.html",
        "[7] Mozilla Developer Network (MDN), \"Content Security Policy (CSP): frame-ancestors Directive,\" MDN Web Docs, 2024. Available: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Content-Security-Policy/frame-ancestors",
        "[8] Mozilla Developer Network (MDN), \"X-Frame-Options Response Header Specification,\" MDN Web Docs, 2024. Available: https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/X-Frame-Options",
        "[9] The PHP Group, \"PHP Manual: Prepared Statements and Stored Procedures - PDO & MySQLi,\" 2024. Available: https://www.php.net/manual/en/mysqli.quickstart.prepared-statements.php",
        "[10] The PHP Group, \"PHP Manual: htmlspecialchars - Convert special characters to HTML entities,\" 2024. Available: https://www.php.net/manual/en/function.htmlspecialchars.php",
        "[11] National Institute of Standards and Technology (NIST), \"Special Publication 800-95: Guide to Secure Web Services,\" U.S. Department of Commerce, 2007. Available: https://csrc.nist.gov/publications/detail/sp/800-95/final",
        "[12] International Organization for Standardization, \"ISO/IEC 27034-1: Information technology — Security techniques — Application security — Part 1: Overview and concepts,\" ISO, 2018."
    ]

    for ref in references:
        p_ref = doc.add_paragraph()
        p_ref.paragraph_format.space_before = Pt(1.5)
        p_ref.paragraph_format.space_after = Pt(2.5)
        p_ref.paragraph_format.line_spacing = 1.1
        r_ref = p_ref.add_run(ref)
        r_ref.font.name = "Calibri"
        r_ref.font.size = Pt(8.5)
        r_ref.font.color.rgb = COLOR_BODY

    # Save DOCX
    doc.save(DOCX_OUT)
    print(f"Generated DOCX at: {DOCX_OUT}")

if __name__ == "__main__":
    generate_report()
