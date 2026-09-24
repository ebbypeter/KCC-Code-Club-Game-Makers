# -*- coding: utf-8 -*-
"""Build the editable Word copies of the pack's non-handout documents.

    python3 build_editable.py <repo-root> <out-dir>

The handouts are print-only and stay PDF. Everything else has details a
volunteer has to fill in before it goes out — dates, venue, contact, the
agreed insurance wording — so each one is also produced as a .docx with those
placeholders highlighted.
"""
import io, json, os, re, subprocess, sys, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import md_ast
from build_print import strip_front, read

DOCS = [
    ("admin/parent-info-letter.md", "Parent-Information-Letter.docx",
     "Parent Information", "",
     "Everything highlighted in yellow needs filling in before this goes out. Delete this box when you are done."),
    ("admin/consent-and-photo-permission.md", "Consent-and-Photo-Permission.docx",
     "Consent and Photo Permission", "Return before the first session",
     "Fill in the highlighted placeholders — especially the insurance wording, which the committee has to agree — then delete this box."),
    ("admin/attendance-tracker.md", "Attendance-Tracker.docx",
     "Attendance Tracker", "Keep this in the room", "",
     ),
    ("course/program-overview.md", "Programme-Overview.docx",
     "Programme Overview", "How the club runs, and why", ""),
    ("admin/pre-launch-checklist.md", "Pre-launch-Checklist.docx",
     "Pre-launch Checklist", "Start six weeks out", ""),
    ("admin/volunteer-briefing.md", "Volunteer-Briefing.docx",
     "Volunteer Briefing", "Read before week one",
     "One thing highlighted in yellow: the named contact for welfare concerns. Fill it in before you hand this out, then delete this box."),
    ("admin/showcase-run-sheet.md", "Showcase-Run-Sheet.docx",
     "Showcase Run Sheet", "Week eight", ""),
    ("admin/venue-device-checklist.md", "Venue-and-Device-Checklist.docx",
     "Venue and Device Checklist", "Before you commit to a room", ""),
    ("admin/scratch-accounts-setup.md", "Scratch-Accounts.docx",
     "Scratch Accounts", "Set up six weeks out", ""),
]

NEWPAGE = {"Attendance-Tracker.docx": ["The sheet", "Catch-up log"]}
LANDSCAPE = {"Attendance-Tracker.docx"}

REDUNDANT_H2 = re.compile(r'^##\s*KCC Code Club:\s*Game Makers\s*$', re.M)
# The markdown carries its own "Template" note for the reader of the .md; the
# Word copy gets a clearer instruction box instead, so drop the original.
TEMPLATE_NOTE = re.compile(r'^>\s*\*\*Template\.\*\*[^\n]*(?:\n>[^\n]*)*\n?', re.M)


def main(root, outdir):
    os.makedirs(outdir, exist_ok=True)
    tmp = tempfile.mkdtemp(prefix="kcc-ast-")
    docs = []
    for entry in DOCS:
        src, out, title, sub, note = (list(entry) + [""])[:5]
        md = REDUNDANT_H2.sub("", read(os.path.join(root, src)))
        if note:
            md = TEMPLATE_NOTE.sub("", md)
        blocks = md_ast.convert(strip_front(md))
        ast = os.path.join(tmp, out + ".json")
        io.open(ast, "w", encoding="utf-8").write(json.dumps(blocks, ensure_ascii=False))
        docs.append({
            "ast": ast, "out": os.path.join(outdir, out), "title": title,
            "sub": sub, "note": note, "landscape": out in LANDSCAPE,
            "newpage": NEWPAGE.get(out, []),
        })
    man = os.path.join(tmp, "manifest.json")
    io.open(man, "w", encoding="utf-8").write(json.dumps({"docs": docs}, ensure_ascii=False))
    subprocess.run(["node", os.path.join(HERE, "make_editable.js"), man], check=True)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else ".",
         sys.argv[2] if len(sys.argv) > 2 else os.path.join("outputs", "Admin", "Editable"))
