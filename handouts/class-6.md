# Game Makers — Week 6
## Broadcasts and Game Over

**Name:** ______________________

---

### Today's big idea

Sprites can't read each other's code. But one sprite can **shout a message**, and every sprite
listening for that message reacts.

```
  Wand:  when this sprite clicked  →  broadcast [zap]

  Frog:  when I receive [zap]  →  switch costume to [toad]
  Tree:  when I receive [zap]  →  change size by 25
```

The wand has no idea the frog and the tree exist. It just shouts. That's the clever part.

---

### Words to know

| Word | What it means |
|---|---|
| **broadcast** | Shout a message to every sprite |
| **when I receive** | Listen for a message and react to it |
| **state** | What "mode" the game is in — title screen, playing, game over |
| **stop all** | Stop absolutely everything |

> ⚠️ Message names are typed by hand, so **typos are today's biggest bug**. Always pick the
> message from the dropdown rather than making a new one by accident.

---

### Class activity A — Magic Wand

```
Wand:   when this sprite clicked  →  broadcast [zap]
Frog:   when I receive [zap]  →  switch costume to [toad]  →  say [ribbit] for 1 second
Tree:   when I receive [zap]  →  change size by 25
```

Now add a second message, `undo`, on a key press, that puts everything back.

### Class activity B — Two-Scene Story

Two backdrops, two sprites, one story that runs itself using broadcasts to move between scenes.

---

### Your project — lives, game over, and a start screen

**Step 1 — Lives**
- [ ] Variable `lives`, `set lives to 3` at the start
- [ ] Bad catch → `change lives by -1`
- [ ] A script that watches for `lives` running out and broadcasts `gameover`

```
forever
    if <(lives) < 1> then
        broadcast [gameover]
        stop this script
```

**Step 2 — Game over**
- [ ] A "Game Over" backdrop
- [ ] Stage: `when I receive [gameover]` → `switch backdrop to [Game Over]`
- [ ] Falling objects: `when I receive [gameover]` → `hide`

**Step 3 — Title screen** *(if there's time)*
- [ ] A "Title" backdrop with your game's name
- [ ] `when [s] key pressed` → `broadcast [startgame]`
- [ ] Move your game's start code from `when green flag clicked` to `when I receive [startgame]`

- [ ] **Save it**

---

## Homework

**1. A way to win.** Pick a target score. Broadcast a `youwin` message when the player gets
there, with its own backdrop.

**2. Restart.** Add a way to play again without clicking the green flag — a key or a clickable
button that resets your variables and broadcasts `startgame`.

---

## Bonus challenges

1. A "3 — 2 — 1 — GO!" countdown between the title screen and the game starting.
2. Different music for each backdrop, starting and stopping on the right broadcasts.
3. A boss object that only appears once your score passes 20.
4. Try `broadcast and wait` instead of `broadcast`. What's different?
   *(Hint: it doesn't carry on until every listener has finished.)*

---

### If something breaks

- **Broadcast does nothing?** Check the message name in the dropdown. There are probably two
  similar ones.
- **Sprites still visible after game over?** `stop all` ran before they could hide. Hide first,
  or add a short `wait` before stopping.
- **Sprites invisible when you restart?** They were hidden and never `show`n again.
- **Lives goes to -1, -2, -3?** Use `< 1` instead of `= 0`. Exact checks miss the moment.
