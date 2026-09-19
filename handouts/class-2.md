# Game Makers — Week 2
## Events and Movement

**Name:** ______________________

---

### Today's big idea

Code doesn't only run when you click the green flag. It runs when **things happen** — a key
press, a click, anything. Those triggers are called **events**.

And position is just two numbers: **x** goes across, **y** goes up and down. The middle of the
stage is `x: 0  y: 0`.

```
        y: 180
          |
x: -240 --+-- x: 240
          |
       y: -180
```

---

### Words to know

| Word | What it means |
|---|---|
| **event** | Something happening that makes code run |
| **hat block** | The curved block at the top of a script. It says *when* to run |
| **coordinates** | The two numbers that say where something is |
| **change vs set** | `change` adds to what's there. `set` replaces it |

---

### Class activity A — Treasure Hunt

Three or four sprites. One is hiding treasure.

- On each empty one: `when this sprite clicked` → `say [Nothing here!] for 2 seconds`
- On the winner: `when this sprite clicked` → `say [You found it!]` → `change size by 50`

### Class activity B — Drive the Car

Make a sprite you can drive with all four arrow keys.

```
when [right arrow] key pressed  →  change x by 10
when [left arrow] key pressed   →  change x by -10
when [up arrow] key pressed     →  change y by 10
when [down arrow] key pressed   →  change y by -10
```

Now change the `10` to `50`. Too fast? Try `2`. Too slow? **Find the number that feels right.**
That's called tuning, and it's a real part of making games.

---

### Your project — the player moves

- [ ] Arrow keys move your player left and right
- [ ] The player stays near the bottom of the stage
- [ ] `go to x: 0 y: -140` under the green flag so it always starts in the same place
- [ ] Tune the speed until it feels good
- [ ] **Save it**

---

## Homework

**1. Add another dimension.** Either let your player move up and down too, or make it wrap
around — go off one side, come back on the other.

**2. Face the right way.** Use `point in direction` so your player faces where it's going.
*(If your sprite ends up upside down, look at the rotation style in the sprite panel — the
fix isn't in the code!)*

---

## Bonus challenges

1. Add WASD keys as well as the arrows, so two people could play at once.
2. Make an "H for home" key that sends the player back to the start.
3. Add the **Pen** extension. Make your sprite draw a trail. Add a key that clears it.
4. Make the sprite move faster while you hold shift. *(Tricky! Come back to this in two weeks.)*

---

### If something breaks

- **Moves once then stops?** You used `set x to` instead of `change x by`.
- **Nothing happens?** Wrong sprite selected when you wrote the code.
- **Gone off the screen?** Add `go to x: 0 y: -140` and click the green flag.
