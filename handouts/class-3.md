# Game Makers — Week 3
## Loops and Randomness

**Name:** ______________________

---

### Today's big idea

If you're about to do the same thing twenty times — **don't**. Tell the computer to repeat it.

```
repeat 4
    clap
    clap
    stomp
```

That's 12 actions written in 4 lines. Change the 4 to a 100 and you've just done 300 actions
by typing two characters.

And when you want the computer to surprise you, use `pick random`.

---

### Words to know

| Word | What it means |
|---|---|
| **loop** | Code that repeats |
| **repeat n** | Do this exactly n times |
| **forever** | Do this until the game stops. Nothing can go after it |
| **random** | A number the computer picks that you can't predict |

> ⚠️ **Golden rule:** every `forever` loop needs a `wait` inside it somewhere. Without one,
> Scratch freezes and you lose your work.

---

### Class activity A — Dancing Sprite

```
when green flag clicked
forever
    next costume
    wait 0.2 seconds
    move 5 steps
```

Change the `0.2` until the walk looks right. Add `if on edge, bounce` so it doesn't escape.

### Class activity B — Rain

```
when green flag clicked
forever
    go to x: (pick random -240 to 240) y: 180
    repeat 20
        change y by -18
        wait 0.02 seconds
```

A raindrop that appears somewhere random along the top and falls. Forever.

**Now change the numbers.** Fewer repeats + bigger step = faster. Try it.

---

### Your project — things fall from the sky!

Today your project starts looking like a real game.

- [ ] Add a falling object sprite that fits your theme
- [ ] Make it the right size
- [ ] Give it the falling script (same shape as Rain)
- [ ] **Tune the speed** so it's catchable but not boring
- [ ] **Save it**

*It doesn't notice your player yet — you can "catch" it and nothing happens. That's next week.*

---

## Homework

**1. A second thing to catch.** Add another falling sprite that looks different.
*(Shortcut: right-click your first one and duplicate it — the code comes with it!)*

**2. Unpredictable speed.** Use `pick random` so each drop falls at a different speed.
*(Hint: the `wait` can take a random number.)*

---

## Bonus challenges

1. Draw shapes with `repeat` + `turn`. A square is `repeat 4 [move 100, turn 90]`.
   What makes a triangle? A hexagon? What does `repeat 36 [move 10, turn 10]` draw?
2. Make your falling object spin as it falls.
3. Make a starfield — five objects falling at five different speeds.
4. Use `repeat until` instead of `forever` so it stops after ten drops. *(Hard! You'll need a
   way to count, which we learn in two weeks.)*

---

### If something breaks

- **Flickers at the top and nothing else?** No `wait` inside the falling loop.
- **Falls once then stops?** The whole thing needs to be inside a `forever`.
- **Falls upward?** `change y by 18` should be `change y by -18`. Up is positive.
- **Scratch froze?** A `forever` with no `wait` in it. Reload and add one.
