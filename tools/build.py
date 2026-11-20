#!/usr/bin/env python3
"""Build step for the Swift Recovery Service static site.

- Makes web-sized JPEG + WebP copies of the real job photos (assets/img/)
- Makes the Open Graph share image (assets/img/og.jpg, 1200x630)
- Checks index.html: every local file it references exists, and all
  call / WhatsApp / email links use the right number and address.
Run:  python3 tools/build.py
"""
import re, sys
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "swift-recovery-demo-photos"
OUT = ROOT / "assets" / "img"
WIDTHS = (480, 800, 1125)
TEL = "tel:+447471863459"
WA = "https://wa.me/447471863459"
EMAIL = "mailto:srsrecoveryliverpool@yahoo.com"

def images():
    OUT.mkdir(parents=True, exist_ok=True)
    for src in sorted(SRC.glob("*.jpg")):
        im = ImageOps.exif_transpose(Image.open(src)).convert("RGB")
        for w in WIDTHS:
            if w > im.width:
                continue
            r = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
            r.save(OUT / f"{src.stem}-{w}.jpg", "JPEG", quality=78, optimize=True, progressive=True)
            r.save(OUT / f"{src.stem}-{w}.webp", "WEBP", quality=74, method=6)
    # Open Graph image: landscape crop of the waterfront job
    im = Image.open(SRC / "job-5.jpg").convert("RGB")
    og = ImageOps.fit(im, (1200, 630), Image.LANCZOS, centering=(0.5, 0.55))
    og.save(OUT / "og.jpg", "JPEG", quality=82, optimize=True, progressive=True)

def check():
    html = (ROOT / "index.html").read_text()
    errors = []
    for ref in re.findall(r'(?:src|href|srcset)="([^"]+)"', html):
        for part in ref.split(","):
            p = part.strip().split(" ")[0]
            if not p or re.match(r"(https?:|tel:|mailto:|#|data:)", p):
                continue
            if not (ROOT / p).exists():
                errors.append(f"missing file: {p}")
    for href in re.findall(r'href="(tel:[^"]*)"', html):
        if href != TEL: errors.append(f"wrong tel link: {href}")
    for href in re.findall(r'href="(https://wa\.me[^"]*)"', html):
        if not href.startswith(WA): errors.append(f"wrong WhatsApp link: {href}")
    for href in re.findall(r'href="(mailto:[^"]*)"', html):
        if href != EMAIL: errors.append(f"wrong email link: {href}")
    if "[PHONE_NUMBER]" in html: errors.append("placeholder [PHONE_NUMBER] still present")
    return errors

if __name__ == "__main__":
    images()
    errs = check()
    total = sum(f.stat().st_size for f in OUT.iterdir())
    print(f"images: {len(list(OUT.iterdir()))} files, {total/1024:.0f} KB")
    if errs:
        print("\n".join("ERROR " + e for e in errs)); sys.exit(1)
    print("build OK")
