# Game Makers — Week 7
## Operators, My Blocks and Levels

**Name:** ______________________

---

### Today's big idea

**Two ideas today.**

**Operators** let you do maths and ask complicated questions.
`(score) + 10` · `(score) > 10` · `<this> and <that>` · `join [Level ] (level)`

**My Blocks** let you take a group of blocks you keep rewriting, give it a name, and use it as
one single block from then on.

> *"How do you make a cup of tea?"* — seven steps.
> Draw a box around them and call it **MAKE TEA**.
> Now "make tea for four people" is `repeat 4 [MAKE TEA]` instead of 28 steps.

That's called **abstraction**, and it's one of the most powerful ideas in all of programming.

---

### Words to know

| Word | What it means |
|---|---|
| **operator** | A block that does maths or asks a question |
| **My Block** | A block you invent yourself, made of other blocks |
| **define** | The hat block where you say what your new block does |
| **abstraction** | Naming a group of steps so you can forget the details |

> 💡 **Dragging tip:** building `<<(score) > 10> and <(lives) > 1>>` inside a tiny slot is
> horrible. Build the whole thing in an **empty space** first, then drag the finished assembly
> into the `if`.

---

### Class activity A — Quiz Sprite

```
ask [What is 7 x 6?] and wait
if <(answer) = 42> then
    say [Correct!] for 2 seconds
    change score by 1
else
    say (join [No, it was ] [42]) for 2 seconds
```

Add two more questions. Notice how much you're copying and pasting. Activity B fixes that.

### Class activity B — Make Your Own Block

```
define celebrate
    say [Correct!] for 1 second
    change size by 25
    start sound [Cheer]
    wait 0.5 seconds
    change size by -25
```

Now replace all three copies of your celebration with one `celebrate` block.
**Change the definition once → all three change.** That's the payoff.

---

### Your project — it gets harder as you get better

- [ ] A `speed` variable. Replace the fixed `wait 0.02` with `wait (speed) seconds`
- [ ] Every 10 points: level up and multiply `speed` by 0.85

```
forever
    if <(score) > ((level) * 10)> then
        change level by 1
        set speed to ((speed) * 0.85)
        say (join [Level ] (level)) for 1 seconds
    wait 0.1 seconds
```

- [ ] A **rare bonus item** worth 5 points that only shows up sometimes:

```
if <(pick random 1 to 5) = 1> then
    show
else
    hide
```

- [ ] Make a `reset object` My Block and use it on every falling sprite
- [ ] **Save it**

---

## Homework

**1. A rare treasure.** If you didn't finish the bonus item, do it now.

**2. Tidy up.** Find code you've written more than once and turn it into a My Block.

**3. Think about the showcase.** Next week your family comes to see your game. Have two
sentences ready: *what your game is*, and *the hardest bug you fixed*.

---

## Bonus challenges

1. A power-up that makes your player wider for five seconds, then back to normal.
2. Use `join` to show "Level 3 — Score 42" as one readout.
3. Use `and` or `or` for a combo condition — a bonus that only counts on a high level.
4. **Really hard:** replace your duplicated falling sprites with **clones**. Look up
   `create clone of myself`, `when I start as a clone`, `delete this clone`. Nobody is expected
   to get this one.

---

### If something breaks

- **Game freezes on level up?** `speed` hit zero or went negative. Put a floor on it.
- **Level goes up hundreds of times?** The `if` keeps firing. Make sure `level` is in the condition.
- **Can't drop an operator in?** Build it in empty space first, then drag it in.
- **My Block missing on another sprite?** My Blocks belong to one sprite only.
