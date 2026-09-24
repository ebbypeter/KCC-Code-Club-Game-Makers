# Outputs

Everything the teachers, volunteers and support team use, laid out exactly as it should appear in
Google Drive. To publish, copy the contents of this folder into the shared Drive folder and replace
what's there.

**Everything here is generated.** Edit the markdown in `course/` or `admin/`, run
`build/build_all.py`, then copy across. Don't edit a file in here directly: the next build
overwrites it without warning.

```
Weeks/
  Week 1 - Meet Scratch/          lesson plan, handout, slides, class exercises
  …
  Week 8 - Polish, Test and Showcase/
Volunteers/                       briefing (PDF + deck), programme overview,
                                  long project guide, concept map, external resources
Admin/                            parent letter, consent form, attendance tracker,
                                  checklists, Scratch accounts guide
  Editable/                       Word copies of the above, for filling in
Showcase/                         run sheet, certificate template
```

## What to print, and when

| File | Print when | Copies |
|---|---|---|
| `Week N - Handout.pdf` | The night before each class | One per student, plus 2 spare |
| `Week N - Lesson Plan.pdf` | The night before each class | One per volunteer leading or floating |
| `Admin/Parent Information Letter.pdf` | Three weeks before week one | One per interested family |
| `Admin/Consent and Photo Permission.pdf` | Three weeks before week one | One per registered child |
| `Admin/Attendance Tracker.pdf` | Once, before week one | One, kept in the room. A4 landscape |
| `Admin/Pre-launch Checklist.pdf` | Eight weeks out | One, and work down it |
| `Admin/Venue and Device Checklist.pdf` | Before you commit to a room | One, for the venue visit |
| `Admin/Scratch Accounts Setup.pdf` | Six weeks out | One |
| `Volunteers/Programme Overview.pdf` | Before week one | One per volunteer |
| `Volunteers/Volunteer Briefing.pdf` | Before week one | One per volunteer, including backups |
| `Showcase/Showcase Run Sheet.pdf` | Week seven | Two |
| `Showcase/Certificate Template.pdf` | Week seven. **Fill in the names first** | One per student, A4 landscape |

The handouts are designed to survive a **black-and-white photocopier**, which is what community
venues have. Every Scratch block carries its category name and the fills are spread across the
greyscale range, so Motion still reads differently from Control with no colour at all.

The **certificate is the exception**: print that one in colour if you can. It's the thing that goes
on a fridge.

## Filling in the details

Most admin documents have dates, a venue, a contact or the agreed insurance wording to fill in
before they go out. The Word copies in `Admin/Editable/` have every placeholder **highlighted in
yellow**. Delete the instruction box at the top once you're done.

| File | What you need to fill in |
|---|---|
| `Parent-Information-Letter.docx` | Day, time, dates, venue, class size, registration link, your name and contact |
| `Consent-and-Photo-Permission.docx` | Term dates, venue, and **the insurance wording the committee agrees** |
| `Volunteer-Briefing.docx` | The named contact for welfare concerns |
| `Attendance-Tracker.docx` | Student names, if you'd rather type them than write them |
| `Showcase-Run-Sheet.docx` | Times and names on the night |
| `Venue-and-Device-Checklist.docx` | Venue answers |
| `Programme-Overview.docx`, `Pre-launch-Checklist.docx`, `Scratch-Accounts.docx` | Nothing, unless you want to reword them |

**Save your filled-in copy somewhere else.** In Drive, keep a term folder beside this pack and put
the filled-in copies there:

```
Terms/2027 Term 1/Parent-Information-Letter.docx
```

The blank template stays in the pack, and each term's paperwork lives with that term's records.

The Word files ask for **Fredoka** and **Nunito Sans**. Install both from Google Fonts (or from
`build/assets/fonts/` in the repo), or Word will substitute something else. The document still
reads fine, it just isn't ours.

## Certificates

`Showcase/Certificate Template.html` is the editable version. Open it in a browser, duplicate the
whole `<div class="cert">` block once per student, type each child's name into `.name` and a
specific award into the `.line` under "Special mention for", then print to PDF.

Make the mentions specific: "Most Determined Debugger", "Best Boss Battle", "Most Original Idea".
A specific line is worth ten generic ones. Everyone gets one; this is not a competition.

## Slides

Each week folder has that class's projector deck as PowerPoint. The teaching detail is in the
**speaker notes**, so present from the notes view. The editable originals are linked from
`course/slides.md`.
