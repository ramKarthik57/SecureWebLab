# -*- coding: utf-8 -*-
"""
inspect_layout.py
Analyzes the rendered PDF for exact chapter start pages, heading locations,
and checks for orphaned headings or near-empty pages.
"""
import pymupdf
import re

pdf_path = r"C:\Users\Ram\Desktop\SecureWebLab\SecureJobLab_Web_Application_Security_Report.pdf"
doc = pymupdf.open(pdf_path)

print(f"Total Pages: {len(doc)}")
chapter_pages = {}

for idx, page in enumerate(doc):
    page_num = idx + 1
    text = page.get_text()
    lines = [line.strip() for line in text.split("\n") if line.strip()]
    num_chars = len(text.strip())
    num_images = len(page.get_images())

    # Check for chapter titles
    for line in lines:
        if line.startswith("Chapter ") or line.startswith("References ") or line.startswith("Table of Contents") or line.startswith("Certificate ") or line.startswith("Executive Summary"):
            clean_title = line.split("\n")[0][:50]
            if clean_title not in chapter_pages:
                chapter_pages[clean_title] = page_num

    # Check for orphan headings (heading near bottom of page)
    # Get text blocks
    blocks = page.get_text("blocks")
    if blocks:
        last_block = blocks[-1]
        last_text = last_block[4].strip()
        # If last text starts with Chapter or 1. or 2. and is short, it might be an orphan heading
        if re.match(r'^(Chapter \d+|[1-9]\.[0-9]|References|Q[1-5]:)', last_text) and len(last_text) < 80:
            print(f"[POTENTIAL ORPHAN] Page {page_num}: Last block is heading '{last_text}' at y1={last_block[3]:.1f}")

    print(f"Page {page_num:02d}: {num_chars:4d} chars, {num_images} images. Top: '{lines[0] if lines else 'EMPTY'}'")

print("\n--- Identified Chapter Start Pages ---")
for k, v in chapter_pages.items():
    print(f"  {k:50s} -> Page {v}")
