"""Merge each extracted PDF image with its soft mask onto white, and build contact sheets.

usage: python3 -I flatten.py <pdf> <extract_dir> <prefix> <out_dir>
"""
import os
import subprocess
import sys

from PIL import Image, ImageDraw

pdf, src, prefix, out = sys.argv[1:5]
os.makedirs(out, exist_ok=True)

listing = subprocess.run(["pdfimages", "-list", pdf], capture_output=True, text=True).stdout.splitlines()[2:]
rows = [l.split() for l in listing if l.strip()]
by_num = {int(r[1]): r for r in rows}

kept = []
for r in rows:
    page, num, kind = int(r[0]), int(r[1]), r[2]
    if kind != "image":
        continue
    path = os.path.join(src, f"{prefix}-{page:03d}-{num:03d}.png")
    img = Image.open(path).convert("RGB")
    nxt = by_num.get(num + 1)
    if nxt and nxt[2] == "smask":
        mask = Image.open(os.path.join(src, f"{prefix}-{page:03d}-{num + 1:03d}.png")).convert("L")
        if mask.size != img.size:
            mask = mask.resize(img.size)
        bg = Image.new("RGB", img.size, "white")
        bg.paste(img, mask=mask)
        img = bg
    name = f"p{page:03d}_n{num:03d}.png"
    img.save(os.path.join(out, name))
    kept.append((name, img))

# contact sheets: 12 thumbnails per sheet, labelled
cols, rows_per, tw, th = 4, 3, 420, 420
for s in range(0, len(kept), cols * rows_per):
    sheet = Image.new("RGB", (cols * tw, rows_per * (th + 24)), "white")
    d = ImageDraw.Draw(sheet)
    for i, (name, img) in enumerate(kept[s:s + cols * rows_per]):
        t = img.copy()
        t.thumbnail((tw - 10, th - 10))
        x, y = (i % cols) * tw, (i // cols) * (th + 24)
        sheet.paste(t, (x + 5, y + 24))
        d.text((x + 5, y + 4), name, fill="red")
    sheet.save(os.path.join(out, f"_sheet_{s // (cols * rows_per):02d}.png"))
print(len(kept), "images")
