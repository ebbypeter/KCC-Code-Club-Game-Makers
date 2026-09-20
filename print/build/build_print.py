# -*- coding: utf-8 -*-
"""Build the KCC Game Makers print pack.

    python3 build_print.py <repo-root> <out-dir>

Renders every markdown source in the pack to an A4 PDF through one shared
stylesheet, so the handouts, forms and volunteer documents match the slide
decks. Needs playwright + chromium.
"""
import io, os, re, sys, asyncio
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import printkit as pk

WEEK_TITLES = {
    1: "Meet Scratch", 2: "Events and Movement", 3: "Loops and Randomness",
    4: "Decisions and Sensing", 5: "Variables and Score",
    6: "Broadcasts and Game Over", 7: "Operators, My Blocks and Levels",
    8: "Polish, Test and Showcase",
}

FOOT = ("KCC Code Club · Game Makers — {doc}")


def read(p):
    return io.open(p, encoding="utf-8").read()


REDUNDANT_H2 = re.compile(r'^##\s*KCC Code Club:\s*Game Makers\s*$', re.M)


def strip_front(md):
    """Drop the leading H1/H2, the Name line and the first rule."""
    md = REDUNDANT_H2.sub("", md)
    lines = md.split("\n")
    out, seen_rule = [], False
    for i, l in enumerate(lines):
        s = l.strip()
        if not out and (s.startswith("# ") or s.startswith("## ")):
            continue
        if not seen_rule and re.match(r'^\*\*Name:\*\*', s):
            continue
        if not seen_rule and s == "---" and not "".join(out).strip():
            seen_rule = True
            continue
        out.append(l)
    return "\n".join(out).strip()


def jobs(root):
    J = []
    for n in range(1, 9):
        src = os.path.join(root, "handouts", "class-%d.md" % n)
        J.append(dict(out="handout-week-%d.pdf" % n, src=src, kind="student",
                      title="Week %d" % n, sub=WEEK_TITLES[n],
                      badge="Week %d of 8" % n, nameline=True,
                      doc="Week %d handout" % n,
                      endnote="Stuck? Put your hand up — that is what we are here for. "
                              "And always save before you close the lid."))
    A = os.path.join(root, "admin")
    C = os.path.join(root, "curriculum")
    J += [
        dict(out="form-parent-letter.pdf", src=os.path.join(A, "parent-info-letter.md"),
             kind="doc", title="Parent Information", sub="",
             badge="", doc="Parent letter"),
        dict(out="form-consent.pdf", src=os.path.join(A, "consent-and-photo-permission.md"),
             kind="doc", title="Consent and Photo Permission",
             sub="Return before the first session", badge="", doc="Consent form"),
        dict(out="form-attendance-tracker.pdf", src=os.path.join(A, "attendance-tracker.md"),
             kind="doc", title="Attendance Tracker", sub="Keep this in the room",
             badge="", landscape=True, doc="Attendance tracker",
             newpage=["The sheet", "Catch-up log"]),
        dict(out="program-overview.pdf", src=os.path.join(C, "00-program-overview.md"),
             kind="doc", title="Programme Overview",
             sub="How the club runs, and why", badge="", doc="Programme overview"),
        dict(out="pre-launch-checklist.pdf", src=os.path.join(A, "pre-launch-checklist.md"),
             kind="doc", title="Pre-launch Checklist", sub="Start six weeks out",
             badge="", doc="Pre-launch checklist"),
        dict(out="volunteer-briefing.pdf", src=os.path.join(A, "volunteer-briefing.md"),
             kind="doc", title="Volunteer Briefing", sub="Read before week one",
             badge="", doc="Volunteer briefing"),
        dict(out="showcase-run-sheet.pdf", src=os.path.join(A, "showcase-run-sheet.md"),
             kind="doc", title="Showcase Run Sheet", sub="Week eight",
             badge="", doc="Showcase run sheet"),
        dict(out="venue-device-checklist.pdf", src=os.path.join(A, "venue-device-checklist.md"),
             kind="doc", title="Venue and Device Checklist", sub="Before you commit to a room",
             badge="", doc="Venue checklist"),
        dict(out="scratch-accounts-setup.pdf", src=os.path.join(A, "scratch-accounts-setup.md"),
             kind="doc", title="Scratch Accounts", sub="Set up six weeks out",
             badge="", doc="Scratch accounts guide"),
    ]
    return J


# ------------------------------------------------------------- certificate
def certificate_html():
    return """<!doctype html><html><head><meta charset="utf-8"><title>Certificates</title>
<style>
%(fonts)s
@page { size: A4 landscape; margin: 0; }
* { box-sizing: border-box; }
body { margin:0; font-family:'Nunito Sans', Carlito, Arial, sans-serif;
  -webkit-print-color-adjust:exact; print-color-adjust:exact; }
.cert { width:297mm; height:210mm; page-break-after:always; padding:12mm;
  position:relative; background:%(cream)s; }
.frame { height:100%%; border:2.2mm solid %(maroon)s; border-radius:3mm;
  padding:11mm 16mm 9mm; display:flex; flex-direction:column; align-items:center;
  text-align:center; position:relative; background:#FFFDF7; }
.frame:after { content:""; position:absolute; inset:2.6mm;
  border:0.5mm solid %(gold)s; border-radius:1.6mm; }
.logo { width:20mm; height:20mm; object-fit:contain; margin-bottom:2mm; }
.club { font-size:9.5pt; letter-spacing:0.3em; text-transform:uppercase;
  color:%(goldtx)s; font-weight:800; }
.title { font-family:'Fredoka', sans-serif; font-size:42pt; font-weight:600;
  color:%(maroon)s; margin:3mm 0 1mm; }
.subtitle { font-size:13pt; color:%(body)s; margin-bottom:7mm; }
.awarded { font-size:10.5pt; color:%(body)s; letter-spacing:0.14em;
  text-transform:uppercase; font-weight:700; }
.name { font-family:'Fredoka', sans-serif; font-size:32pt; color:%(ink)s;
  font-weight:600; border-bottom:0.6mm solid %(gold)s; min-width:170mm;
  padding:3mm 6mm 2mm; margin:3mm 0 7mm; }
.body { font-size:12pt; color:%(body)s; line-height:1.55; max-width:195mm; }
.body strong { color:%(maroon)s; }
.blocks { margin:5mm 0 0; display:flex; gap:2.5mm; justify-content:center; }
.blocks span { display:block; width:15mm; height:7mm; border-radius:1.6mm;
  border:0.3mm solid; }
.super { font-size:12pt; color:%(ink)s; margin-top:6mm; }
.super .label { color:%(goldtx)s; font-size:9.5pt; letter-spacing:0.12em;
  text-transform:uppercase; font-weight:800; display:block; margin-bottom:2mm; }
.super .line { border-bottom:0.5mm solid %(line)s; min-width:120mm;
  display:inline-block; padding-bottom:1.5mm; }
.feet { margin-top:auto; display:flex; justify-content:space-between; width:100%%;
  gap:20mm; padding:0 4mm; }
.sig { flex:1; }
.sig .line { border-top:0.5mm solid %(maroon)s; padding-top:2mm; font-size:9.5pt;
  color:%(body)s; letter-spacing:0.09em; text-transform:uppercase; font-weight:700; }
</style></head><body>

<!-- Duplicate this whole .cert block once per student. Type the child's name into
     .name and a specific award into the .line under "Special mention for". -->
<div class="cert"><div class="frame">
  <img class="logo" src="%(logo)s" alt="Kerala Cultural Club">
  <div class="club">Kerala Cultural Club</div>
  <div class="title">Game Makers</div>
  <div class="subtitle">KCC Code Club &middot; Scratch &middot; Ages 7&ndash;12</div>

  <div class="awarded">This certifies that</div>
  <div class="name">&nbsp;</div>

  <div class="body">
    completed all eight weeks of Game Makers, learned to program with
    <strong>sequences, loops, conditionals, variables and broadcasts</strong>,
    and designed, built and debugged a working game entirely from scratch.
  </div>

  <div class="blocks">%(chips)s</div>

  <div class="super">
    <span class="label">Special mention for</span>
    <span class="line">&nbsp;</span>
  </div>

  <div class="feet">
    <div class="sig"><div class="line">Instructor</div></div>
    <div class="sig"><div class="line">Date</div></div>
  </div>
</div></div>

</body></html>""" % dict(
        fonts=pk.fonts_css(), logo=pk.logo_uri(), cream=pk.CREAM, maroon=pk.MAROON,
        gold=pk.GOLD, goldtx=pk.GOLDTX, ink=pk.INK, body=pk.BODY, line=pk.LINE,
        chips="".join('<span style="background:%s;border-color:%s"></span>' % (fill, ink)
                      for fill, ink in [("#FFBF00", "#C89600"), ("#3373CC", "#24539B"),
                                        ("#774DCB", "#5A399C"), ("#389438", "#2A7029"),
                                        ("#FF8C1A", "#C96C10"), ("#CC4C7A", "#9E3A5E")]))


# ------------------------------------------------------------- render
async def render(root, outdir):
    from playwright.async_api import async_playwright
    os.makedirs(outdir, exist_ok=True)
    built = []
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        pg = await browser.new_page()

        for j in jobs(root):
            body = pk.md_to_html(strip_front(read(j["src"])))
            for h in j.get("newpage", []):
                body = body.replace("<h2>%s</h2>" % h,
                                    '<h2 class="newpage">%s</h2>' % h)
            html = pk.page(body, j["title"], j.get("sub", ""), j.get("badge", ""),
                           j["kind"], j.get("landscape", False),
                           j.get("nameline", False), j.get("endnote", ""))
            await pg.set_content(html, wait_until="load")
            await pg.emulate_media(media="print")
            foot = ('<div style="width:100%%;font-family:sans-serif;font-size:7pt;'
                    'color:#8A7A72;padding:0 14mm;display:flex;'
                    'justify-content:space-between;"><span>%s</span>'
                    '<span class="pageNumber"></span></div>' % FOOT.format(doc=j["doc"]))
            await pg.pdf(path=os.path.join(outdir, j["out"]),
                         format="A4", landscape=j.get("landscape", False),
                         print_background=True, display_header_footer=True,
                         header_template="<div></div>", footer_template=foot,
                         margin={"top": "15mm", "bottom": "16mm",
                                 "left": "14mm", "right": "14mm"})
            built.append(j["out"])

        await pg.set_content(certificate_html(), wait_until="load")
        await pg.emulate_media(media="print")
        await pg.pdf(path=os.path.join(outdir, "certificate-template.pdf"),
                     format="A4", landscape=True, print_background=True,
                     margin={"top": "0", "bottom": "0", "left": "0", "right": "0"})
        built.append("certificate-template.pdf")
        await browser.close()
    return built


if __name__ == "__main__":
    root = sys.argv[1] if len(sys.argv) > 1 else "."
    outdir = sys.argv[2] if len(sys.argv) > 2 else os.path.join(root, "print")
    made = asyncio.run(render(root, outdir))
    io.open(os.path.join(outdir, "certificate-template.html"), "w",
            encoding="utf-8").write(certificate_html())
    print("built %d files" % (len(made) + 1))
    for m in made:
        print("  ", m)
