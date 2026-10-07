# -*- coding: utf-8 -*-
"""
SecureJobLab: Comprehensive Academic Project Report Generator
Course Code: 20CYS403 — Web Application Security
Output: SecureJobLab_Web_Application_Security_Report.docx
"""

import os
import sys
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

# --- Color Definitions ---
COLOR_NAVY = RGBColor(10, 37, 64)       # #0A2540 - Main headings
COLOR_SLATE = RGBColor(30, 41, 59)      # #1E293B - Secondary headings
COLOR_BODY = RGBColor(51, 65, 85)       # #334155 - Body text
COLOR_BLUE = RGBColor(2, 132, 199)      # #0284C7 - Accent
COLOR_RED = RGBColor(207, 19, 34)       # #CF1322 - Vulnerable / Threat
COLOR_GREEN = RGBColor(22, 163, 74)     # #16A34A - Secure / Mitigated
COLOR_MUTED = RGBColor(100, 116, 139)   # #64748B - Captions & metadata

HEX_NAVY = "0A2540"
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

def set_cell_margins(cell, top=120, bottom=120, left=160, right=160):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('w:top', top), ('w:bottom', bottom), ('w:left', left), ('w:right', right)]:
        node = OxmlElement(m)
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_cell_border(cell, **kwargs):
    """
    kwargs: top, bottom, left, right
    values: {"val": "single", "sz": "12", "color": "0A2540"}
    """
    tcPr = cell._tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for edge in ('top', 'left', 'bottom', 'right'):
        edge_data = kwargs.get(edge)
        if edge_data:
            tag = 'w:{}'.format(edge)
            element = parse_xml(f'<{tag} {nsdecls("w")} w:val="{edge_data.get("val", "single")}" w:sz="{edge_data.get("sz", "4")}" w:space="0" w:color="{edge_data.get("color", "auto")}"/>')
            tcBorders.append(element)
        else:
            tag = 'w:{}'.format(edge)
            element = parse_xml(f'<{tag} {nsdecls("w")} w:val="none"/>')
            tcBorders.append(element)
    tcPr.append(tcBorders)

def add_header_footer(doc):
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)

        # Header
        header = s.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("20CYS403: Web Application Security Laboratory | SecureJobLab Platform")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = COLOR_MUTED

        # Footer
        footer = s.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Page ")
        frun.font.name = "Calibri"
        frun.font.size = Pt(9)
        frun.font.color.rgb = COLOR_MUTED
        # Add page number XML
        fldSimple = OxmlElement('w:fldSimple')
        fldSimple.set(qn('w:instr'), 'PAGE')
        fp._p.append(fldSimple)

        frun2 = fp.add_run(" | Confidential Academic Project Report — Strictly Evaluated for 5 Core CWE Modules")
        frun2.font.name = "Calibri"
        frun2.font.size = Pt(8.5)
        frun2.font.color.rgb = COLOR_MUTED

def add_page_number_to_run(run):
    fldSimple = OxmlElement('w:fldSimple')
    fldSimple.set(qn('w:instr'), 'PAGE')
    run._r.append(fldSimple)

def main():
    print("Initializing document...")
    doc = Document()
    add_header_footer(doc)

    print("Document structure ready. Writing full report contents...")

if __name__ == "__main__":
    main()
