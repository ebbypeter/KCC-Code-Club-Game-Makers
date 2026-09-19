# Class 1 — Meet Scratch

**Big idea:** A program is a list of instructions, carried out in order, exactly as written.

## At a glance

| | |
|---|---|
| **New concepts** | Sequence, sprites, costumes, backdrops, the green flag |
| **New blocks** | `when green flag clicked`, `move`, `turn`, `go to x y`, `say`, `say for n secs`, `switch costume to`, `next costume`, `change size by` |
| **Class activity** | Name Dance |
| **Project checkpoint** | Player sprite and themed backdrop exist; the character says hello |
| **Homework** | The four-line joke; theme your player |

## Before the class

- Scratch accounts created in advance via a **teacher account** — see `admin/scratch-accounts-setup.md`.
  Do not spend session one on signups. It will eat forty minutes and it is the single most
  reliable way to lose a room of children on day one.
- Every machine logged in, Scratch open, one browser tab, before students arrive.
- Projector working and mirroring your screen. Test it. Test it the day before too.
- Printed handouts (`handouts/class-1.md`), name stickers, spare pencils.
- Your own reference Sky Catcher open in another tab, ready to show for thirty seconds.

## 0:00–0:10 — Welcome

No Show & Tell this week. Instead:

Names, name stickers, and one round of "what's a game you like?" Keep it to one sentence each
or it will run to twenty minutes.

Then show them where they're going: play your finished Sky Catcher on the projector for thirty
seconds. Let them react. Then say the sentence that carries the whole term — *"In eight weeks,
you'll have built one of these, and yours will be better than mine."*

Do not explain how it works. They just need to want it.

## 0:10–0:25 — Live demo: the Scratch window

Open with the idea the whole course rests on: *"computers do exactly what you say, in exactly the order you say it. Every bug you will ever have is you saying something slightly different from what you meant."* Then show them, rather than telling them again.

Share your screen and tour the four areas. Point at each and name it, and use the names all
term:

- **Stage** (top right) — where the game happens
- **Sprite list** (bottom right) — the characters
- **Block palette** (left) — the instructions available
- **Code area** (middle) — where you build the script

Then build, live, with them watching:

1. Drag `when green flag clicked` into the code area. Click the flag. Nothing happens. Say so.
2. Snap `say [Hello!]` under it. Click the flag. It works. Notice out loud that it never
   goes away — introduce `say [Hello!] for 2 seconds`.
3. Add `move 100 steps`. Run it. The cat has left. Bring it back with `go to x: 0 y: 0`.
4. **Make a deliberate mistake.** Put the `move` block *above* the `when green flag clicked`
   hat block, disconnected. Run it. Nothing. Look genuinely puzzled, say "hmm, what did I
   expect and what did it do?", then find it.

That last step is the most important fifteen seconds of the whole class. They need to see an
adult be confused, stay calm, and work it out. Do a version of it every single week.

## 0:25–0:55 — Class activity: Name Dance

The brief on their handout, in their words: *make a sprite that says your name and then dances.*

Guided at first, then let them go:

1. Choose a sprite from the library — any one they like.
2. `when green flag clicked` → `say [your name] for 2 seconds`.
3. Add a dance: `move 50 steps`, `wait 0.5 seconds`, `move -50 steps`, `turn 15 degrees`.
4. Add `next costume` between the moves, if their sprite has multiple costumes.
5. Add `change size by 10` and see what happens when it runs twice.

Circulate constantly. The floating volunteer should not sit down at any point during this
twenty-five minutes.

**If they finish early:** point them at the bonus challenges on the back of the handout. Do not
let them start the project build early — you want everyone arriving at project time together.

## 0:55–1:05 — Break

## 1:05–1:25 — Project build: start Sky Catcher

1. **New project.** Name it `Sky Catcher — [their name]` immediately, at the top of the window.
   Make everyone do this before anything else. Unnamed projects get lost.
2. **Pick a theme.** Two minutes, decide, commit. Offer the list from the project guide if
   they're stuck. Tell them clearly they cannot change it later.
3. **Delete the cat.** Small moment, weirdly satisfying for them.
4. **Choose a player sprite** that fits the theme (a basket, a person, a dog, a net).
5. **Choose a backdrop** that fits.
6. **Position the player at the bottom:** `when green flag clicked` → `go to x: 0 y: -140`.
7. **Add a greeting:** `say [Catch the mangoes!] for 2 seconds`.
8. **Save.** File → Save now. Then check the project appears in *My Stuff*.

That's the checkpoint. It isn't a game yet, and they know it, which is fine — they've seen
where it's going.

## 1:25–1:30 — Wrap

Everyone saves. Walk the room and physically confirm every screen shows a saved project with
the right name; do not take their word for it.

Brief the homework in one sentence each. Point at the bonus challenges. Remind them Show &
Tell is at the start of next class and that you'd love to see the joke.

## Homework

1. **The four-line joke.** Make a sprite tell a joke using four `say` blocks with waits, so the
   timing lands. The punchline has to wait.
2. **Theme your player.** Change your player sprite's costume, colour, or size so it looks
   properly like your game's idea.

## Bonus challenges

1. Make a sprite draw a square by moving and turning. (Hint: four moves, four turns of 90.)
2. Make two sprites have a conversation, with the waits timed so they don't talk over each other.
3. Explore the Sound blocks. Make your sprite play a sound when the flag is clicked.
4. Make your sprite grow bigger and bigger and then reset to normal size.

## Common bugs this week

| Symptom | Cause |
|---|---|
| Nothing happens on the green flag | Script isn't attached to the hat block |
| The sprite vanished | Moved off-stage. `go to x:0 y:0` brings it home |
| "Say" text never disappears | Used `say` instead of `say for n seconds` |
| Blocks won't snap together | Dragged to the wrong spot; needs to be close enough to see the drop shadow |
| Code runs on the wrong sprite | They wrote it while the wrong sprite was selected in the sprite list |

That last one causes more week-one confusion than everything else combined. Teach them to
glance at which sprite is highlighted before they start typing.

## Notes for the second volunteer

Your job this week is mouse skills and confidence, not code. Watch for the child who hasn't
managed to drag a block yet and is hiding it. Get to them before they decide they're bad at this.

## Links

- [Scratch](https://scratch.mit.edu)
- Related free project, good for a child who wants more: [Space talk](https://projects.raspberrypi.org/en/pathways/scratch-intro) (Raspberry Pi Foundation, Intro to Scratch pathway)
