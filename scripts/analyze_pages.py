import pymupdf
import os

pdf_path = "SecureJobLab_Web_Application_Security_Report.pdf"
doc = pymupdf.open(pdf_path)

print(f"Total Pages: {len(doc)}")
for idx, page in enumerate(doc):
    text = page.get_text().strip()
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    first_few = " | ".join(lines[:3]) if lines else "EMPTY"
    last_few = " | ".join(lines[-3:]) if lines else "EMPTY"
    
    # Calculate content bounding box
    blocks = page.get_text("blocks")
    content_blocks = [b for b in blocks if not any(x in b[4] for x in ['SecureJobLab Platform', 'Course: 20CYS403', 'DEPARTMENT OF'])]
    img_rects = [page.get_image_rects(img[0]) for img in page.get_images()]
    
    top_y = min([b[1] for b in content_blocks] + [r.y0 for rlist in img_rects for r in rlist]) if (content_blocks or img_rects) else 0
    bot_y = max([b[3] for b in content_blocks] + [r.y1 for rlist in img_rects for r in rlist]) if (content_blocks or img_rects) else 0
    height = page.rect.height
    usable_h = height - 72 # 1 inch top & bottom
    occ_h = bot_y - top_y
    occ_pct = (occ_h / usable_h) * 100
    gap_pt = height - bot_y - 36
    
    print(f"=== Page {idx+1:02d} (Occupancy: {occ_pct:.1f}%, Bottom Gap: {gap_pt:.1f} pt) ===")
    print(f"  Top: {first_few[:90]}")
    print(f"  Bottom: {last_few[:90]}")
    print(f"  Images count: {len(page.get_images())}")
