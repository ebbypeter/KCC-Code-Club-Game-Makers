# Class 7 — Operators, My Blocks and Levels

**Big idea:** You can do maths and ask complicated questions with operators. And when you've
written the same few blocks three times, you can give that group a name and turn it into a
block of your own.

## At a glance

| | |
|---|---|
| **New concepts** | Operators, compound conditions, abstraction via custom blocks |
| **New blocks** | `+ − × /`, `< = >`, `and`, `or`, `not`, `join`, `ask and wait`, `answer`, My Blocks (`define`) |
| **Class activity** | Quiz Sprite, then Make Your Own Block |
| **Project checkpoint** | Difficulty ramps up with score; level-up messages; a rare bonus item |
| **Homework** | A high-value rare item; tidy repeated code into a My Block |

## Before the class

- Print the Week 7 handout.
- Skeleton `Sky Catcher — end of Week 6` ready.
- Two weeks left. Start watching for anyone whose project is far enough behind that the showcase
  is at risk, and plan to spend extra floor time with them today and next week.

## 0:00–0:10 — Show & Tell

Ask for win screens and restarts. Anyone who got the countdown bonus working should definitely
present.

## 0:10–0:25 — Live demo

Frame My Blocks before you demo them. Ask the class how you make a cup of tea, take the seven steps they give you, draw a box round them on the board and write **MAKE TEA** on it. Then ask how you'd make tea for four people. Somebody will say "do MAKE TEA four times" rather than list twenty-eight steps — that's abstraction, arrived at by a nine-year-old in under a minute, and it beats any definition you could give.

### Operators (7 min)

1. Drop `(3) + (4)` into a `say` block. Then `(score) + (10)`. Variables go in operator slots.
2. `<(score) > (10)>` inside an `if`. Point at the hexagon shape again — operators that ask
   questions are hexagons and fit in `if` slots; operators that produce values are rounded and
   fit in number slots. Shape is meaning.
3. `<<(score) > (10)> and <(lives) > (1)>>` — nesting two conditions. Fiddly to drag; show them
   slowly. Building it *outside* the `if` first and then dragging the whole assembly in is much
   easier than trying to drop things into a tiny slot.
4. `join [Level ] (level)` inside a `say`. Now they can make text that includes a number.
5. `ask [What's your name?] and wait` → `say (join [Hello ] (answer))`. Sensing's `answer` block
   is new but obvious.

### My Blocks (8 min)

1. My Blocks → **Make a Block** → name it `reset object`.
2. A `define reset object` hat appears. Put `go to x: (pick random -220 to 220) y: 170` under it.
3. Now the `reset object` block is in the palette. Use it in two places in the falling script.
4. Change the definition — change 170 to 160 — and show that **both** places changed. One edit,
   two fixes. That's the payoff and they need to see it explicitly.
5. **Deliberate mistake:** call a My Block from a *different sprite* and find it isn't there.
   My Blocks belong to one sprite. Be puzzled, then explain.

## 0:25–0:55 — Class activity

### Activity A — Quiz Sprite (14 min)

```
when green flag clicked
set score to 0
ask [What is 7 x 6?] and wait
if <(answer) = 42> then
    say [Correct!] for 2 seconds
    change score by 1
else
    say (join [No, it was ] [42]) for 2 seconds
```

Then have them add two more questions. Three near-identical blocks of code — and leave it there,
deliberately ugly, because Activity B fixes it.

### Activity B — Make Your Own Block (16 min)

Go back to the quiz. Make a My Block called `celebrate` containing:

```
define celebrate
    say [Correct!] for 1 second
    change size by 25
    start sound [Cheer]
    wait 0.5 seconds
    change size by -25
```

Now replace the three copies of the celebration with three `celebrate` calls. Then change the
definition once and watch all three change.

Let them invent their own — `wobble`, `explode`, `spin around`. The naming is half the fun.

## 0:55–1:05 — Break

## 1:05–1:25 — Project build: levels and difficulty

Goal: **"By the end of today your game gets harder the better you get at it."**

### Step 1 — A speed variable

1. Make a variable `speed`, `set speed to 0.02` under the game start.
2. Replace the fixed `wait 0.02 seconds` in the falling loop with `wait (speed) seconds`.

### Step 2 — Ramp it up

On the player or stage:

```
when I receive [startgame]
set level to 1
forever
    if <(score) > ((level) * 10)> then
        change level by 1
        set speed to ((speed) * 0.85)
        say (join [Level ] (level)) for 1 seconds
    wait 0.1 seconds
```

Every ten points, the level goes up and everything gets 15% faster. Watch for `speed` going so
low it breaks — put a floor on it if they hit that: `if <(speed) < 0.005> then set speed to 0.005`.

### Step 3 — A rare bonus item

1. Duplicate a falling object. Make it look special — gold, sparkly, whatever.
2. In its falling loop, make it usually invisible:

```
if <(pick random 1 to 5) = 1> then
    show
else
    hide
```

3. Worth 5 points instead of 1 when caught.

### Step 4 — Tidy with a My Block

Every falling sprite has the same "go back to the top at a random x" code. Make it a
`reset object` My Block on each one. It's a small win, but it's the first time they refactor
working code purely to make it nicer, which is a real habit worth starting.

Save.

## 1:25–1:30 — Wrap

Save and back up. Tell them plainly: **next week is the showcase**, families are coming, and
next week is about polishing, not adding. If there's something they've been meaning to add,
this week's homework is the last chance.

## Homework

1. **A rare treasure.** If you didn't finish the bonus item in class, do it now. Make something
   that appears rarely and is worth a lot.
2. **Tidy up.** Find some code you've written more than once and turn it into a My Block.

Also: **think about what you'll say at the showcase.** One sentence about what your game is, and
one about the hardest thing you fixed.

## Bonus challenges

1. A power-up that makes your player wider for five seconds, then back to normal.
2. Use `join` to display "Level 3 — Score 42" in a single readout.
3. Use `and` or `or` for a combo condition — a bonus that only counts if you're on a high level.
4. **Advanced:** replace your duplicated falling sprites with **clones** — one sprite that copies
   itself. Look up `create clone of myself`, `when I start as a clone`, and `delete this clone`.
   This is genuinely harder than anything in the course and nobody is expected to get it.

## Common bugs this week

| Symptom | Cause |
|---|---|
| Game freezes when the level goes up | `speed` went to zero or negative. Put a floor on it |
| Level goes up hundreds of times instantly | The `if` fires repeatedly before the score changes. `change level by 1` inside the `if` fixes it, but only if the condition uses `level` |
| Can't drag an operator into the `if` slot | Build the whole condition in an empty area first, then drag the finished assembly in |
| My Block missing on another sprite | My Blocks belong to one sprite only. Rebuild it, or drag the sprite onto the other to copy |
| `answer` is always empty | `ask and wait` must run before `answer` is read |
| Rare item never appears | `pick random 1 to 5 = 1` is re-rolled each drop — it should appear one time in five. If never, check the `show`/`hide` are the right way round |

## Notes for the second volunteer

Nesting operator blocks is fiddly *motor work*, not hard thinking. Children who understand
perfectly well will still fail to drop a block into a small slot five times and conclude they
don't get it. Watch for frustration that's actually a mouse problem, and teach the trick of
assembling the condition in open space first.

## Links

- [Next customer please](https://projects.raspberrypi.org/en/pathways/more-scratch) — Raspberry Pi Foundation, heavy on operators and variables
- [Further Scratch pathway](https://projects.raspberrypi.org/en/pathways/further-scratch) — clones, My Blocks and boolean logic, for anyone racing ahead
- Skeleton: `Sky Catcher — end of Week 7` in the club studio
