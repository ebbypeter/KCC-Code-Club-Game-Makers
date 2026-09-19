# Game Makers — Week 4
## Decisions and Sensing

**Name:** ______________________

---

### Today's big idea

The computer can ask a **yes-or-no question** about the world, and do different things
depending on the answer.

```
if <touching the player?> then
    ...do this...
else
    ...do that instead...
```

A question that can only be answered yes or no is called a **boolean**. Those blocks are
**pointy hexagons**, and they only fit in pointy hexagon slots. Shape tells you what fits where.

---

### Words to know

| Word | What it means |
|---|---|
| **condition** | The yes/no question |
| **boolean** | An answer that can only be yes or no (true or false) |
| **if / then** | Do something only if the answer is yes |
| **if / then / else** | Do one thing if yes, a different thing if no |
| **sensing** | Blocks that let a sprite notice the world |

> ⚠️ **Big one today:** an `if` block checks **once**, at the moment it runs. If you want it to
> keep checking, it has to be **inside a loop**.

---

### Class activity A — Traffic Light

```
when green flag clicked
forever
    if <touching [Red]?> then
        say [STOP!]
    else
        say [GO!]
```

Now drag your sprite in and out of the red one.

### Class activity B — Bumper Sprite

```
when green flag clicked
forever
    move 5 steps
    if <touching [edge]?> then
        turn 180 degrees
    wait 0.01 seconds
```

Add a second sprite and make them bounce off each other too.

---

### Your project — CATCHING! 🎉

**Today your project becomes a real game you can actually play.**

The new bit goes **inside the falling loop**:

```
repeat 20
    change y by -18
    wait 0.02 seconds
    if <touching [Player]?> then
        start sound [Pop]
        go to x: (pick random -220 to 220) y: 170
```

- [ ] Catching works
- [ ] A sound plays when you catch something
- [ ] Playtest it — then swap seats and play your neighbour's!
- [ ] **Save it**

---

## Homework

**1. Catch feedback.** Make catching do something noticeable — a flash, a costume change,
a different sound, a `say`.

**2. Something you shouldn't catch.** Add a bad falling object (a bomb, a coconut, a cat).
For now it just says "Ouch!" when it hits you. Next week it'll cost you points.

---

## Bonus challenges

1. A sprite that says different things depending on which half of the stage it's on.
   *(Hint: `if <(x position) > 0>`)*
2. A sprite that follows the mouse, but only while space is held down.
3. Use `if` to stop your player leaving the stage — the thing we couldn't do in week 2!
4. Use `and` to combine two conditions: only catch it if you're touching it **and** pressing space.

---

### If something breaks

- **Catching never works?** The `if` isn't inside the loop.
- **Works once, then never again?** The `if` is in the outer `forever` but not in the `repeat`.
- **Object falls straight through you?** You need the `go to` inside the `if` to send it back up.
- **Catching is really fussy?** Your object moves too far between checks. Make `change y by`
  smaller and the `repeat` number bigger.
