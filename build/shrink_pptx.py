# -*- coding: utf-8 -*-
"""Shrink PowerPoint decks without changing how they look.

    python3 shrink_pptx.py <file-or-folder> [...]

Decks downloaded from Claude's Slides store a separate copy of the same logo
and background on every slide, uncompressed, so a 20-slide deck comes out at
around 3 MB. This keeps one copy of each distinct image, points every slide
at it, and recompresses the file. Slides, notes and layout are untouched.

Safe to run repeatedly: a deck that is already small is left as it is.
"""
import hashlib, io, os, re, sys, zipfile

MEDIA = re.compile(r'^ppt/media/[^/]+$')


def shrink(path):
    with zipfile.ZipFile(path) as z:
        infos = z.infolist()
        data = {i.filename: z.read(i.filename) for i in infos}

    # Keep the first file seen with each distinct content.
    canonical, alias = {}, {}
    for name in sorted(n for n in data if MEDIA.match(n)):
        h = hashlib.sha1(data[name]).hexdigest()
        if h in canonical:
            alias[name] = canonical[h]
        else:
            canonical[h] = name

    for dup, keep in alias.items():
        old, new = os.path.basename(dup), os.path.basename(keep)
        for n in list(data):
            if n.endswith(".rels"):
                s = data[n].decode("utf-8")
                t = s.replace('/media/%s"' % old, '/media/%s"' % new)
                if t != s:
                    data[n] = t.encode("utf-8")
        del data[dup]

    ct = "[Content_Types].xml"
    if alias and ct in data:
        s = data[ct].decode("utf-8")
        for dup in alias:
            s = re.sub(r'<Override[^>]*PartName="/%s"[^>]*/>' % re.escape(dup), "", s)
        data[ct] = s.encode("utf-8")

    before = os.path.getsize(path)
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as out:
        # [Content_Types].xml first, the way Office writes it.
        for n in sorted(data, key=lambda n: (n != ct, [i.filename for i in infos].index(n))):
            out.writestr(n, data[n])
    if buf.tell() < before:
        with open(path, "wb") as f:
            f.write(buf.getvalue())
    after = os.path.getsize(path)
    return before, after, len(alias)


def targets(args):
    for a in args:
        if os.path.isdir(a):
            for d, _, files in os.walk(a):
                for f in sorted(files):
                    if f.lower().endswith(".pptx") and not f.startswith("~$"):
                        yield os.path.join(d, f)
        else:
            yield a


if __name__ == "__main__":
    for p in targets(sys.argv[1:] or ["."]):
        b, a, n = shrink(p)
        print("  %-60s %6d KB -> %5d KB  (%d duplicate images)"
              % (os.path.basename(p)[:60], b // 1024, a // 1024, n))
