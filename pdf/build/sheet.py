import sys, glob
from PIL import Image, ImageDraw
files = sys.argv[3:]
cols = int(sys.argv[2])
ims = [Image.open(f) for f in files]
w, h = ims[0].size
rows = (len(ims) + cols - 1) // cols
sheet = Image.new("RGB", (cols * (w + 8), rows * (h + 8)), "#888")
for i, im in enumerate(ims):
    sheet.paste(im, ((i % cols) * (w + 8), (i // cols) * (h + 8)))
sheet.save(sys.argv[1])
