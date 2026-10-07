# -*- coding: utf-8 -*-
"""
convert_to_pdf.py
Converts DOCX to PDF using Word COM automation (ExportAsFixedFormat in Print Quality),
and injects the high-resolution, uncompressed, crystal-clear original images directly
into the PDF object streams to eliminate any Word compression or blurriness.
"""
import os
import sys
import win32com.client
import pymupdf

BASE_DIR = r"C:\Users\Ram\Desktop\SecureWebLab"
IMAGES_DIR = os.path.join(BASE_DIR, "images")
LAB_DIR = os.path.join(BASE_DIR, "lab_5vuln_screenshots")

PAGE_IMAGE_MAPPING = {
    6: [ # Page 7: Architecture
        os.path.join(IMAGES_DIR, "diagram_architecture.png")
    ],
    8: [ # Page 9: DB Schema
        os.path.join(IMAGES_DIR, "diagram_db_schema.png")
    ],
    9: [ # Page 10: Login & Index
        os.path.join(IMAGES_DIR, "screenshot_login_verified.png"),
        os.path.join(IMAGES_DIR, "screenshot_index_verified.png")
    ],
    10: [ # Page 11: Applications Pipeline
        os.path.join(IMAGES_DIR, "screenshot_applications_verified.png")
    ],
    11: [ # Page 12: SQLi Vulnerable
        os.path.join(LAB_DIR, "mod1_vulnerable.png")
    ],
    12: [ # Page 13: SQLi Secure
        os.path.join(LAB_DIR, "mod1_secure.png")
    ],
    13: [ # Page 14: XSS Vulnerable
        os.path.join(LAB_DIR, "mod2_vulnerable.png")
    ],
    14: [ # Page 15: XSS Secure
        os.path.join(LAB_DIR, "mod2_secure.png")
    ],
    15: [ # Page 16: OS Command Injection Vulnerable
        os.path.join(LAB_DIR, "mod3_vulnerable.png")
    ],
    16: [ # Page 17: OS Command Injection Secure
        os.path.join(LAB_DIR, "mod3_secure.png")
    ],
    17: [ # Page 18: Directory Traversal Vulnerable
        os.path.join(LAB_DIR, "mod4_vulnerable.png")
    ],
    18: [ # Page 19: Directory Traversal Secure
        os.path.join(LAB_DIR, "mod4_secure.png")
    ],
    19: [ # Page 20: Clickjacking 100% & 30% Sandbox
        os.path.join(LAB_DIR, "clickjack_harmful_100pct.png"),
        os.path.join(LAB_DIR, "clickjack_harmful_30pct.png")
    ],
    20: [ # Page 21: Clickjacking Triggered vs Secure Blank Frame
        os.path.join(LAB_DIR, "clickjack_harmful_triggered.png"),
        os.path.join(LAB_DIR, "mod5_secure.png")
    ]
}

def convert_and_sharpen(docx_path, pdf_path):
    print(f"Step 1: Exporting DOCX to PDF via Word COM: {docx_path} -> {pdf_path}")
    word = win32com.client.DispatchEx("Word.Application")
    word.Visible = False
    word.DisplayAlerts = False
    try:
        doc = word.Documents.Open(os.path.abspath(docx_path))
        try:
            doc.Fields.Update()
        except Exception as e:
            print("Notice updating fields:", e)

        # ExportAsFixedFormat with OptimizeFor=0 (wdExportOptimizeForPrint)
        doc.ExportAsFixedFormat(
            OutputFileName=os.path.abspath(pdf_path),
            ExportFormat=17, # wdExportFormatPDF
            OpenAfterExport=False,
            OptimizeFor=0,   # wdExportOptimizeForPrint (Maximum print fidelity)
            Range=0,         # wdExportAllDocument
            Item=0,          # wdExportDocumentContent
            IncludeDocProps=True,
            KeepIRM=True,
            CreateBookmarks=1, # wdExportCreateHeadingBookmarks
            DocStructureTags=True,
            BitmapMissingFonts=True,
            UseISO19005_1=False
        )
        doc.Close(SaveChanges=False)
        print("Initial PDF export complete.")
    finally:
        word.Quit()

    # Step 2: Inject lossless high-resolution originals into the PDF
    print("Step 2: Injecting high-resolution uncompressed original images into PDF...")
    doc_pdf = pymupdf.open(pdf_path)
    total_replaced = 0

    for page_idx, expected_images in PAGE_IMAGE_MAPPING.items():
        if page_idx >= len(doc_pdf):
            continue
        page = doc_pdf[page_idx]
        img_infos = page.get_images()

        # Sort images geometrically (top-to-bottom, left-to-right)
        img_sorted = []
        for info in img_infos:
            xref = info[0]
            rects = page.get_image_rects(xref)
            bbox = rects[0] if rects else pymupdf.Rect(0, 0, 0, 0)
            img_sorted.append((bbox.y0, bbox.x0, xref))
        img_sorted.sort()

        for i, (_, _, xref) in enumerate(img_sorted):
            if i < len(expected_images):
                src_path = expected_images[i]
                if os.path.exists(src_path):
                    page.replace_image(xref, filename=src_path)
                    print(f"  [Page {page_idx+1}] Replaced xref {xref} with crystal-clear {os.path.basename(src_path)}")
                    total_replaced += 1
                else:
                    print(f"  [Page {page_idx+1}] Source image not found: {src_path}")

    # Step 3: Inject interactive hyperlinks into Table of Contents (Page 4) and Figures/Tables (Page 5)
    print("Step 3: Injecting interactive document hyperlinks into Table of Contents and Lists...")
    import re

    # Page 4: Table of Contents (0-indexed page 3)
    if len(doc_pdf) >= 4:
        toc_page = doc_pdf[3]
        toc_words = toc_page.get_text('words')
        lines_dict = {}
        for w in toc_words:
            y = round(w[1], 1)
            matched_y = None
            for ky in lines_dict:
                if abs(ky - y) < 4:
                    matched_y = ky
                    break
            if matched_y is None:
                matched_y = y
                lines_dict[matched_y] = []
            lines_dict[matched_y].append(w)

        toc_links_added = 0
        for y in sorted(lines_dict.keys()):
            if y < 65 or y > 710:
                continue
            w_list = sorted(lines_dict[y], key=lambda x: x[0])
            line_text = ' '.join([w[4] for w in w_list])
            m = re.search(r'(\d+)\s*$', line_text)
            if m:
                target_p = int(m.group(1))
                if 1 <= target_p <= len(doc_pdf):
                    bbox = pymupdf.Rect(w_list[0][0], min(w[1] for w in w_list), max(w[2] for w in w_list), max(w[3] for w in w_list))
                    toc_page.insert_link({
                        'kind': pymupdf.LINK_GOTO,
                        'page': target_p - 1,
                        'from': bbox
                    })
                    toc_links_added += 1
        print(f"  Added {toc_links_added} interactive hyperlinks to Table of Contents (Page 4).")

    # Page 5: List of Figures & Tables (0-indexed page 4)
    if len(doc_pdf) >= 5:
        loft_page = doc_pdf[4]
        loft_words = loft_page.get_text('words')
        loft_lines = {}
        for w in loft_words:
            y = round(w[1], 1)
            matched_y = None
            for ky in loft_lines:
                if abs(ky - y) < 4:
                    matched_y = ky
                    break
            if matched_y is None:
                matched_y = y
                loft_lines[matched_y] = []
            loft_lines[matched_y].append(w)

        loft_links_added = 0
        for y in sorted(loft_lines.keys()):
            if y < 75 or y > 330:
                continue
            w_list = sorted(loft_lines[y], key=lambda x: x[0])
            line_text = ' '.join([w[4] for w in w_list])
            m = re.search(r'(\d+)\s*$', line_text)
            if m:
                target_p = int(m.group(1))
                if 1 <= target_p <= len(doc_pdf):
                    bbox = pymupdf.Rect(w_list[0][0], min(w[1] for w in w_list), max(w[2] for w in w_list), max(w[3] for w in w_list))
                    loft_page.insert_link({
                        'kind': pymupdf.LINK_GOTO,
                        'page': target_p - 1,
                        'from': bbox
                    })
                    loft_links_added += 1
        print(f"  Added {loft_links_added} interactive hyperlinks to List of Figures & Tables (Page 5).")

    temp_sharp_pdf = pdf_path + ".sharp.pdf"
    doc_pdf.save(temp_sharp_pdf, deflate=True)
    doc_pdf.close()

    # Replace original PDF with sharpened PDF
    if os.path.exists(temp_sharp_pdf):
        os.replace(temp_sharp_pdf, pdf_path)
        print(f"Step 4: Successfully finalized crystal-clear PDF with {total_replaced} high-res images and clickable TOC at: {pdf_path}")

if __name__ == "__main__":
    docx_file = os.path.join(BASE_DIR, "SecureJobLab_Web_Application_Security_Report.docx")
    pdf_file = os.path.join(BASE_DIR, "SecureJobLab_Web_Application_Security_Report.pdf")
    convert_and_sharpen(docx_file, pdf_file)
