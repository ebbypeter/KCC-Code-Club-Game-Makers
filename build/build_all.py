# -*- coding: utf-8 -*-
"""Rebuild everything in outputs/ from the sources.

    cd build
    python3 build_all.py

1. Every PDF (lesson plans, handouts, volunteer docs, forms, certificate)
2. The editable Word copies in outputs/Admin/Editable/
3. Copies each class exercise (.sb3) into its week folder
4. Shrinks the slide decks

outputs/ is laid out exactly as it should appear in Google Drive, so
publishing is copying that folder across.
"""
import asyncio, os, re, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "outputs")
sys.path.insert(0, HERE)

import build_print, build_editable, shrink_pptx


def copy_exercises():
    """course/exercises/C03A01 - Something.sb3 -> Week 3's folder."""
    src = os.path.join(ROOT, "course", "exercises")
    copied = []
    if not os.path.isdir(src):
        return copied
    for f in sorted(os.listdir(src)):
        m = re.match(r'^C0?(\d)A\d+', f)
        if not m or not f.lower().endswith(".sb3"):
            continue
        n = int(m.group(1))
        dst = os.path.join(OUT, build_print.week_dir(n))
        os.makedirs(dst, exist_ok=True)
        shutil.copy2(os.path.join(src, f), os.path.join(dst, f))
        copied.append(f)
    return copied


if __name__ == "__main__":
    print("PDFs")
    made = asyncio.run(build_print.render(ROOT, OUT))
    with open(os.path.join(OUT, build_print.CERT_HTML), "w", encoding="utf-8") as f:
        f.write(build_print.certificate_html())
    for m in made:
        print("  ", m)

    print("Word copies")
    build_editable.main(ROOT, os.path.join(OUT, "Admin", "Editable"))

    print("Exercises")
    for f in copy_exercises():
        print("  ", f)

    print("Slides")
    for p in shrink_pptx.targets([OUT]):
        b, a, n = shrink_pptx.shrink(p)
        print("   %-50s %5d KB -> %4d KB" % (os.path.basename(p)[:50], b // 1024, a // 1024))
