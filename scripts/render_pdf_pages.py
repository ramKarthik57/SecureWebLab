# -*- coding: utf-8 -*-
"""
render_pdf_pages.py
Renders all pages of the generated PDF into PNG images for visual inspection.
"""
import os
import pymupdf

def render_pages(pdf_path, out_dir):
    os.makedirs(out_dir, exist_ok=True)
    doc = pymupdf.open(pdf_path)
    print(f"Rendering {len(doc)} pages...")
    for idx, page in enumerate(doc):
        pix = page.get_pixmap(dpi=150)
        out_file = os.path.join(out_dir, f"page_{idx+1:02d}.png")
        pix.save(out_file)
        print(f"Rendered Page {idx+1:02d}: {out_file} ({pix.width}x{pix.height})")

if __name__ == "__main__":
    pdf = r"C:\Users\Ram\Desktop\SecureWebLab\SecureJobLab_Web_Application_Security_Report.pdf"
    out = r"C:\Users\Ram\Desktop\SecureWebLab\pdf_page_inspection"
    render_pages(pdf, out)
