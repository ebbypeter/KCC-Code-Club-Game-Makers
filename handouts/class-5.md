# Game Makers — Week 5
## Variables and Score

**Name:** ______________________

---

### Today's big idea

A **variable** is a box with a label on it. You put a number inside. You can look at what's in
it, and you can change it while the game is running.

```
   ┌─────────┐
   │  SCORE  │
   │    7    │
   └─────────┘
```

**`set` replaces what's in the box. `change` adds to what's already there.**

`set score to 5` → the box now holds 5, whatever it held before.
`change score by 1` → if it held 5, it now holds 6.

---

### Words to know

| Word | What it means |
|---|---|
| **variable** | A named box that holds a value |
| **set** | Replace what's in the box |
| **change** | Add to what's in the box (a negative number subtracts) |
| **reset** | Set your variables back to their starting values when the game begins |

> ⚠️ **Always reset.** Put `set score to 0` under the green flag, or your next game will start
> with your last score still in the box.

---

### Class activity A — Click Counter

```
when green flag clicked      →  set clicks to 0
when this sprite clicked     →  change clicks by 1
```

Then add: `if <(clicks) = 10> then say [You win!]`

### Class activity B — Countdown Timer

```
when green flag clicked
set timeleft to 30
repeat 30
    wait 1 seconds
    change timeleft by -1
say [Time's up!]
```

**Now combine them** — a click counter with a 30 second timer. That's a whole little game!

---

### Your project — keeping score

- [ ] Make a variable called `score`
- [ ] `set score to 0` under the green flag
- [ ] Good catch → `change score by 1`
- [ ] Bad catch → `change score by -1` and a different sound
- [ ] Put the score somewhere you can read it
- [ ] Playtest — then swap and try to beat your neighbour's high score
- [ ] **Save it**

---

## Homework

**1. High score.** Add a `highscore` variable that only updates when `score` beats it.

```
if <(score) > (highscore)> then
    set highscore to (score)
```

*Careful: do NOT reset `highscore` under the green flag, or it isn't a high score!*

**2. Make it look good.** Position your score display sensibly. Try right-clicking it for a
large readout. Hide any variables the player doesn't need to see.

---

## Bonus challenges

1. Make the game get faster as your score goes up — put `score` into the `wait` in the falling
   loop. *(Careful: a wait can't be negative.)*
2. Add a `lives` variable starting at 3 that goes down on a bad catch. What should happen at
   zero? See if you can make something happen. *(That's next week — nice head start!)*
3. Ask the player their name at the start and greet them. Look for `ask and wait` and `answer`
   in the **Sensing** blocks.
4. Add a `level` variable that goes up every ten points.

---

### If something breaks

- **Score jumps by 10 or 20 per catch?** You're still touching the object for several loops.
  Make sure the object jumps back to the top *immediately* inside the same `if`.
- **Score starts at last game's number?** Missing `set score to 0` under the green flag.
- **High score keeps resetting?** You put `set highscore to 0` under the green flag. Take it out.
