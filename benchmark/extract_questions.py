"""Crop every question from the practice-test PDF into benchmark/q/qNN.png (test PDF, no answers)."""
import re, sys, fitz

PDF = sys.argv[1]
doc = fitz.open(PDF)
marks = []  # (question number, page index, y_top)
for pi, page in enumerate(doc):
    for b in page.get_text("blocks"):
        m = re.match(r"Question (\d+)\s*$", b[4].strip())
        if m:
            marks.append((int(m.group(1)), pi, b[1]))
marks.sort()
for i, (q, pi, y) in enumerate(marks):
    page = doc[pi]
    y0 = max(y - 4, 0)
    if i + 1 < len(marks) and marks[i + 1][1] == pi:
        y1 = marks[i + 1][2] - 64   # stop above the next question's category header
    else:
        y1 = page.rect.height - 30
    clip = fitz.Rect(30, y0, page.rect.width - 30, y1)
    pix = page.get_pixmap(clip=clip, dpi=170)
    out = f"benchmark/q/q{q:02d}.png"
    pix.save(out)
    from PIL import Image, ImageChops
    im = Image.open(out).convert("RGB")
    bbox = ImageChops.difference(im, Image.new("RGB", im.size, "white")).getbbox()
    if bbox:
        im.crop((0, 0, im.width, min(im.height, bbox[3] + 12))).save(out)
    print(q, pi + 1, round(y0), round(y1))
