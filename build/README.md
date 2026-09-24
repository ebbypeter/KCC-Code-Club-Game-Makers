# Building the pack

Everything in `outputs/` is generated from the markdown in `course/` and `admin/`.
**Edit the markdown, then rebuild. Never edit a PDF or a Word file in `outputs/`.**

```bash
pip install markdown playwright
playwright install chromium
npm install -g docx

cd build
python3 build_all.py
```

That one command:

1. renders every PDF (lesson plans, handouts, volunteer docs, forms, run sheet, certificate)
2. writes the editable Word copies to `outputs/Admin/Editable/`
3. copies each class exercise from `course/exercises/` into its week folder
   (`C03A01 - Something.sb3` lands in Week 3)
4. shrinks the slide decks (see below)

The pieces still run on their own if you only need one: `build_print.py`,
`build_editable.py`, `shrink_pptx.py`.

## What the styling does

The pack shares its design language with the projector decks: the same two typefaces
(Fredoka for headings, Nunito Sans for text, both vendored in `assets/fonts/` under the
Open Font Licence so the build needs no network), the same maroon/gold/green palette taken
from the club logo, and the same rendering of Scratch code as real blocks.

Two templates. Student handouts get the playful one — week badge, name line, big friendly
headings. Parent, consent and volunteer documents get a quieter letterhead version of the
same palette, because a consent form should not look like a games poster.

## Scratch blocks, and why they look like that

Fenced code blocks in the markdown are detected and drawn as Scratch blocks. Indentation
becomes nesting, and a C-block (`forever`, `repeat`, `if`) closes with a proper bottom arm
with the left spine running through it, the way Scratch draws one.

**They are designed for a black-and-white photocopier**, because that is what a community
venue has. Three things do the work:

1. **Category name printed on the block**, shown whenever the category changes from the
   block above. This is what actually tells Motion from Control when there is no colour.
2. **Fills spread across the greyscale range** — Events is near-white at 0.93 relative
   luminance, My Blocks is a solid mid-grey at 0.36. `printkit.CATS` holds the targets and
   `tint_for()` solves for the tint of each Scratch hue that lands on them, so the colours
   still read as Scratch in colour.
3. **A solid ink spine** down the left of every block at full saturation, giving a second
   lightness cue.

If you add a block the classifier doesn't know, it renders neutral grey with no category
tag — harmless, but add it to `RULES` in `printkit.py` to fix properly. Anchored patterns
(what a block *starts* with) beat unanchored ones, so `go to x: (pick random …)` is
correctly Motion rather than Operators.

## Gotchas

- **Emoji are stripped.** Most printers render them as a tofu box. Don't rely on one to
  carry meaning in a handout.
- **A markdown table needs a header row.** One with empty cells gets dropped rather than
  printed as a stray coloured bar.
- `- [ ]` list items become printed checkboxes.
- To force a page break before a heading, add it to that job's `newpage` list in
  `build_print.py` — that is how the attendance sheet gets a page to itself.
- The certificate is the one thing meant to be printed in colour, so its block chips use
  the vivid Scratch palette rather than the muted print tints.

## Adding a document

Add an entry to `jobs()` in `build_print.py`: the source markdown, the output path inside `outputs/`,
`kind` (`student` or `doc`), a title and subtitle for the letterhead, and `landscape=True`
if it is a wide table.

## Editable Word copies

The handouts are print-only, but every other document has details a volunteer has to fill in —
dates, venue, contact, the agreed insurance wording. Those are also produced as `.docx`:

```bash
cd build
python3 build_editable.py .. ../outputs/Admin/Editable
```

`md_ast.py` turns the markdown into a small JSON AST (headings, paragraphs, tables, bullet /
numbered / checkbox lists, quotes, rules, links — the pack uses nothing else), and
`make_editable.js` renders that with docx-js in the same palette and letterhead as the PDFs.

Placeholders are highlighted yellow so they can't be missed. A placeholder is `[LIKE THIS]`,
`[N]`, or any bracket containing `INSERT` — see `is_placeholder()` in `md_ast.py`. The `[ ]` of a
checkbox list item is explicitly not one.

Two things to know if you change this:

- **Table column widths are computed, not fixed.** `widthsFor()` scores each column by its
  longest cell and normalises to the page width, with a minimum that scales down for wide
  tables — the 14-column attendance tracker can't afford 900 twips a column, and an earlier
  version handed docx-js a negative width and crashed.
- **The generated files are disposable.** Anyone's filled-in copy must be saved elsewhere; see
  `../outputs/README.md`.

## Slide decks

The decks aren't built here. They're made in Claude's Slides and downloaded as PowerPoint, then
dropped into their week folder as `Week N - Slides.pptx` (the briefing deck goes in
`outputs/Volunteers/`). Downloaded decks store the same logo and background on every slide,
uncompressed, which makes each one about 3 MB. `shrink_pptx.py` keeps one copy of each image,
points every slide at it and recompresses, which gets a deck to about 250 KB. It changes nothing
you can see. `build_all.py` runs it for you, and it's safe to run again on a deck that is already
small.
