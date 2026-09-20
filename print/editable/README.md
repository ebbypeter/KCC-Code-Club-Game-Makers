# Editable copies

Word versions of everything in the pack except the handouts, for filling in before you print
or send. Same design as the PDFs — same logo, palette and typefaces — so a filled-in Word file
and a printed handout still look like they came from the same club.

| File | What you need to fill in |
|---|---|
| `Parent-Information-Letter.docx` | Day, time, dates, venue, class size, registration link, your name and contact |
| `Consent-and-Photo-Permission.docx` | Term dates, venue, and **the insurance wording the committee agrees** |
| `Volunteer-Briefing.docx` | The named contact for welfare concerns |
| `Attendance-Tracker.docx` | Student names, if you'd rather type them than write them |
| `Programme-Overview.docx` | Nothing — edit if you want to reword it for a particular audience |
| `Pre-launch-Checklist.docx` | Nothing — tick boxes as you go, or print it |
| `Showcase-Run-Sheet.docx` | Times and names on the night |
| `Venue-and-Device-Checklist.docx` | Venue answers |
| `Scratch-Accounts.docx` | Nothing |

**Everything that needs filling in is highlighted in yellow.** Search for the highlight, or just
scroll — they are hard to miss. Delete the instruction box at the top once you are done.

## Save your filled-in copy somewhere else

These files are **generated**. If anyone re-runs the build, whatever you typed into them is
overwritten without warning.

So when you fill one in, use **Save As** and put your copy outside this folder — a `terms/`
folder beside the repo, or wherever the club keeps its term paperwork:

```
terms/2027-term-1/Parent-Information-Letter.docx
```

The blank template stays here; your term's version lives with that term's records. Next term you
start from the blank again rather than hunting for last term's dates in a file you have to
remember to change.

## Fonts

The Word files ask for **Fredoka** and **Nunito Sans**. Install both from
`../build/assets/fonts/` (or from Google Fonts) or Word will substitute something else — the
document still reads fine, it just isn't ours. Worth doing on whichever machine sends the parent
letter out.

## The handouts

Deliberately not here. They are print-only, have nothing to fill in, and their Scratch blocks are
drawn with CSS that Word cannot reproduce. Print those from `../handout-week-*.pdf`.

## Rebuilding

```bash
cd print/build
python3 build_editable.py ../.. ../editable
```

Needs `markdown` (pip) and `docx` (npm). See `../build/README.md`.
