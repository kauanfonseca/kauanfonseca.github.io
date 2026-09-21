#!/usr/bin/env python3
"""Prepare field photos for the web.

Reads every image in images/originals/, writes a web-sized copy to
images/field/ and leaves the original untouched.

  - resizes so the long edge is at most MAX_PX
  - re-encodes as progressive JPEG at QUALITY
  - drops ALL EXIF metadata, GPS coordinates included

Run from the project root:  python3 tools/prep-images.py
"""
import re
from pathlib import Path
from PIL import Image, ImageOps

SRC, DST = Path("images/originals"), Path("images/field")
MAX_PX, QUALITY = 2000, 82
EXTS = {".jpg", ".jpeg", ".png", ".heic", ".tif", ".tiff", ".webp"}

DST.mkdir(parents=True, exist_ok=True)
for src in sorted(p for p in SRC.iterdir() if p.suffix.lower() in EXTS):
    out = DST / (re.sub(r"[^a-z0-9-]+", "-", src.stem.lower().replace("_", "-")).strip("-") + ".jpg")
    im = ImageOps.exif_transpose(Image.open(src))   # honour rotation, then discard EXIF
    im.thumbnail((MAX_PX, MAX_PX), Image.LANCZOS)
    clean = Image.new(im.mode if im.mode in ("RGB", "L") else "RGB", im.size)
    clean.paste(im.convert(clean.mode))
    clean.save(out, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    print(f"{src.name} -> {out.name}  {out.stat().st_size // 1024} kB  {clean.size[0]}x{clean.size[1]}")


def banner(src, out, focus=0.5, width=2200, height=760):
    """Recorta uma faixa horizontal de qualquer foto para usar como banner.

    focus: onde fica o centro vertical do recorte, 0 (topo) a 1 (base).
    Uso:  python3 -c "import tools.prep_images" -- ou no shell:
          python3 -c "exec(open('tools/prep-images.py').read()); \
                      banner('images/web/img-1234.jpg',
                             'images/field/banner-research.jpg', focus=0.35)"
    """
    from PIL import Image, ImageOps
    im = ImageOps.exif_transpose(Image.open(src))
    w, h = im.size
    target = width / height
    crop_h = min(h, int(w / target))
    crop_w = int(crop_h * target)
    top = max(0, min(h - crop_h, int(h * focus) - crop_h // 2))
    left = max(0, (w - crop_w) // 2)
    im.crop((left, top, left + crop_w, top + crop_h)) \
      .resize((width, height), Image.LANCZOS) \
      .save(out, "JPEG", quality=85, optimize=True, progressive=True)
    print(f"{out}  {width}x{height}  focus={focus}")


def logo(src, out, height=220):
    """Redimensiona um logo mantendo transparência (PNG -> PNG).

        python3 -c "src=open('tools/prep-images.py').read(); ns={};
        exec(src[src.index('def logo('):], ns);
        ns['logo']('~/Downloads/uerj.png', 'images/logos/uerj.png')"
    """
    from PIL import Image
    im = Image.open(src)
    if im.mode not in ("RGBA", "LA", "P"):
        im = im.convert("RGBA")
    w, h = im.size
    im = im.resize((max(1, round(w * height / h)), height), Image.LANCZOS)
    im.save(out, "PNG", optimize=True)
    print(f"{out}  {im.size[0]}x{im.size[1]}")


def portrait(src, out, side=600, focus=0.38):
    """Recorta uma foto de pessoa em quadrado e grava JPEG."""
    from PIL import Image, ImageOps
    im = ImageOps.exif_transpose(Image.open(src))
    w, h = im.size
    s = min(w, h)
    top = max(0, min(h - s, int(h * focus) - s // 2))
    left = max(0, (w - s) // 2)
    im.crop((left, top, left + s, top + s)).resize((side, side), Image.LANCZOS) \
      .convert("RGB").save(out, "JPEG", quality=88, optimize=True, progressive=True)
    print(f"{out}  {side}x{side}")
