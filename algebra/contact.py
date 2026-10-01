"""Render nothing; build one stacked contact sheet (12 evenly spaced frames per video) for 480p previews.
Usage: python algebra/contact.py 6 7 8 9 10  -> prints the output path."""
import subprocess, sys, os, glob, tempfile
from PIL import Image

tmp = tempfile.gettempdir()
sheets = []
for q in sys.argv[1:]:
    n = f"{int(q):02d}"
    f = glob.glob(f"media/videos/a{n}_q{n}/480p15/Q{n}.mp4")
    if not f:
        print("missing", n); continue
    dur = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", f[0]]).decode())
    out = os.path.join(tmp, f"cs_{n}.png")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", f[0], "-vf", f"fps={12/dur:.4f},scale=320:-1,tile=6x2", "-frames:v", "1", out], check=True)
    sheets.append(Image.open(out))
    print(n, f"{dur:.0f}s")
W = max(s.width for s in sheets); H = sum(s.height for s in sheets)
m = Image.new("RGB", (W, H), "black"); y = 0
for s in sheets:
    m.paste(s, (0, y)); y += s.height
res = os.path.join(tmp, "cs_all.png"); m.save(res); print(res)
