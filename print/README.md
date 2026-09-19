# Print Pack

KCC Code Club: Game Makers.

Ready-to-print PDFs. All A4 unless noted.

| File | Print when | Copies |
|---|---|---|
| `handout-week-1.pdf` … `handout-week-8.pdf` | The night before each class | One per student, plus 2 spare |
| `form-parent-letter.pdf` | Three weeks before week one | One per interested family |
| `form-consent.pdf` | Three weeks before week one | One per registered child |
| `form-attendance-tracker.pdf` | Once, before week one | One, and keep it in the room |
| `program-overview.pdf` | Before week one | One per volunteer — has the staffing ratio and the class rhythm |
| `pre-launch-checklist.pdf` | Eight weeks out | One, and work down it |
| `volunteer-briefing.pdf` | Before week one | One per volunteer, including backups |
| `showcase-run-sheet.pdf` | Week seven | Two |
| `certificate-template.pdf` | Week seven — **fill in the names before printing** | One per student, A4 landscape |

## Certificates

`certificate-template.html` is the editable source. Open it in a browser, duplicate the
`<div class="cert">` block once per student, type each child's name into the `.name` div and a
specific award into the `.line` under "Special mention for", then print to PDF.

Make the special mentions specific — "Most Determined Debugger", "Best Boss Battle", "Most
Original Idea". A specific line is worth ten generic ones and it takes five minutes to write
twelve of them. Everyone gets one; this is not a competition.

## Regenerating the PDFs

The PDFs are built from the markdown in `handouts/` and `admin/`. If you edit the markdown,
rebuild rather than editing the PDFs. Any markdown-to-PDF tool will do — the originals were
made with Chromium's print-to-PDF.
