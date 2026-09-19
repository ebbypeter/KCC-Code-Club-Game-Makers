# Class 3 — Loops and Randomness

**Big idea:** If you're about to do the same thing twenty times, don't. Tell the computer to
repeat it. And if you want the game to surprise you, ask it for a random number.

## At a glance

| | |
|---|---|
| **New concepts** | Iteration (`repeat`, `forever`), randomness, nested loops |
| **New blocks** | `repeat n`, `forever`, `repeat until`, `wait n secs`, `pick random a to b` |
| **Class activity** | Dancing Sprite, then Rain |
| **Project checkpoint** | One object falls from a random position at the top, over and over |
| **Homework** | A second falling object; random falling speed |

## Before the class

- Print `handouts/class-3.md`.
- Skeleton `Sky Catcher — end of Week 2` ready for anyone who missed a week.

## 0:00–0:10 — Show & Tell

Homework demos. By now you should get three or four hands. If someone has done a bonus
challenge, get them up — bonus work being celebrated is what makes the *next* student attempt one.

## 0:10–0:25 — Live demo: repeat, forever, random

Frame it before you touch the keyboard. Clap a pattern — *clap, clap, stomp* — four times, wearily, then write it on the board as `repeat 4 [clap, clap, stomp]` and change the 4 to a 10. Twelve actions became thirty by editing one character. Thirty seconds, and the nested loop later lands much more easily for it.

Build live:

1. `when green flag clicked` → `repeat 10 [ move 10 steps, wait 0.1 seconds ]`. Run it. It
   crawls across the stage.
2. Take out the `wait`. Run again. It teleports — too fast to see. Put it back. The point: **the
   wait is what makes it visible**, and this is why their falling object will "not work" later.
3. Swap `repeat 10` for `forever`. Note there's no bump at the bottom of a `forever` block —
   nothing can come after it, because it never ends. Ask them why.
4. Introduce `pick random 1 to 10`. Drop it inside `move [pick random 1 to 10] steps`. Run it
   several times. Different every time.
5. Show `go to x: [pick random -240 to 240] y: 180`. Run it repeatedly. It's jumping around the
   top of the stage — which is exactly the falling-object spawn they're about to build.
6. **Deliberate mistake:** put the `wait` *outside* the loop instead of inside. Run it. Be
   confused for a moment, then narrate finding it.

## 0:25–0:55 — Class activity

### Activity A — Dancing Sprite (12 min)

Take a sprite with several costumes (the library ones with walk cycles work well).

```
when green flag clicked
forever
    next costume
    wait 0.2 seconds
    move 5 steps
```

Then let them tune the `wait` until the walk looks right. Add `if on edge, bounce` so it
doesn't escape.

### Activity B — Rain (18 min)

This is the dress rehearsal for the project build, deliberately.

```
when green flag clicked
forever
    go to x: (pick random -240 to 240) y: 180
    repeat 20
        change y by -18
        wait 0.02 seconds
```

A raindrop that appears at a random point along the top and falls to the bottom, forever.
Get them to change the numbers: fewer repeats and a bigger step is a faster drop.

**Fast finishers:** ask them to make it look like rain by duplicating the sprite three or four
times. Duplicating a sprite copies its scripts, which is a nice thing for them to discover.

## 0:55–1:05 — Break

## 1:05–1:25 — Project build: things fall from the sky

Goal: **"By the end of today, something falls from the sky in your game, over and over."**

This is the week the project starts looking like a game, and they feel it.

1. Add a new sprite that matches the theme — the mango, the ball, the star.
2. Shrink it if needed (`change size by` or the size field in the sprite pane).
3. Build the falling script. Same shape as Rain:

```
when green flag clicked
forever
    go to x: (pick random -220 to 220) y: 170
    repeat 20
        change y by -18
        wait 0.02 seconds
```

4. **Tune it.** Make everyone change the numbers until the speed feels playable with their
   player. Too fast and week four's catching will be impossible; too slow and it's boring. This
   is real game design and they should spend five minutes on it.

Note that the falling object doesn't yet notice the player at all — you can "catch" it and
nothing happens. Say that out loud and promise it for next week. The anticipation is useful.

Save.

## 1:25–1:30 — Wrap

Save, back up, homework brief.

## Homework

1. **A second thing to catch.** Add another falling sprite with a different look. (Hint: right-
   click the first one and duplicate it, then change its costume — the script comes with it.)
2. **Unpredictable speed.** Use `pick random` so each drop falls at a different speed. (Hint:
   the `wait` inside the falling loop can take a random number.)

## Bonus challenges

1. Draw a shape with `repeat` and `turn`. A square is 4 and 90. What makes a triangle? A hexagon?
   What happens with `repeat 36 [ move 10, turn 10 ]`?
2. Make the falling object spin as it falls.
3. Make a starfield — five objects falling at five different speeds.
4. Use `repeat until` instead of `forever` so the object stops after ten drops. (You'll need a
   way to count, which is properly a week-five problem. See how far you get.)

## Common bugs this week

| Symptom | Cause |
|---|---|
| Object flickers at the top and nothing else | No `wait` inside the falling loop, so a whole drop happens in one frame |
| Object falls once then stops | The `go to` and the `repeat` aren't wrapped in a `forever` |
| Object falls at an angle | `change x by` in the loop as well as `change y by` |
| It falls upward | `change y by 18` instead of `-18`. Positive y is up |
| Object goes below the stage and reappears oddly | Too many repeats for the step size; the sprite is clamped at the edge |
| Scratch freezes / the browser tab hangs | A `forever` with no `wait` inside it at all. Add a `wait 0.01`, always |

That last one is worth warning about pre-emptively. A `forever` with no wait will lock the tab
and they'll lose unsaved work. Say "every forever needs a wait somewhere inside it" and repeat
it all term.

## Notes for the second volunteer

The nested loop in the falling script (a `repeat` inside a `forever`) is the first genuinely
abstract thing in the course. Some children will build it correctly and still not be able to
explain it. That's fine at this stage — ask them to predict what happens if you change a
number, and let understanding follow the doing.

## Links

- [Find the bug](https://projects.raspberrypi.org/en/pathways/scratch-intro) — Raspberry Pi Foundation
- Skeleton: `Sky Catcher — end of Week 3` in the club studio
