# Class 4 — Decisions and Sensing

**Big idea:** The computer can ask a yes-or-no question about the world and do different things
depending on the answer.

**This is the big week.** At the end of today their project stops being an animation and becomes
a game they can actually play. Plan for the energy in the room to go up.

## At a glance

| | |
|---|---|
| **New concepts** | Selection (`if`, `if/else`), booleans as yes/no questions, sensing |
| **New blocks** | `if ... then`, `if ... then ... else`, `touching [sprite]?`, `touching [edge]?`, `key [x] pressed?`, `start sound`, `play sound until done` |
| **Class activity** | Traffic Light, then Bumper Sprite |
| **Project checkpoint** | Catching works. The game is playable |
| **Homework** | Catch feedback (sound or flash); add a bad object |

## Before the class

- Print the Week 4 handout.
- Skeleton `Sky Catcher — end of Week 3` ready.
- This is the highest-value class in the course — if you're going to have three volunteers in
  the room on any one week, make it this one.

## 0:00–0:10 — Show & Tell

Homework demos. Ask specifically whether anyone got the random falling speed working, and get
them to explain *how*, not just show it.

## 0:10–0:25 — Live demo: if, if/else, and touching

Build live:

1. `when green flag clicked` → `forever [ if <touching [edge]?> then [ say [ouch] for 1 second ] ]`
   with the sprite draggable. Drag it into the edge. It complains.
2. Point at the **shape** of the blocks. The `touching?` block is a pointy hexagon; the slot in
   the `if` block is a pointy hexagon. Shapes tell you what fits where. This is a genuinely
   useful piece of Scratch literacy and it takes ten seconds.
3. Add an `else`: `if <touching edge?> then [say ouch] else [say fine]`.
4. Swap in `touching [Sprite2]?` and drag two sprites together.
5. **Crucially:** show what happens when the `if` is *not* inside a `forever`. It checks once,
   at the moment the flag is clicked, finds nothing, and gives up forever. Run it, look
   confused, then find it with them.

Number 5 is the bug that will consume half your floor time today. Front-load it.

## 0:25–0:55 — Class activity

### Activity A — Traffic Light (12 min)

A sprite and two coloured sprites.

```
when green flag clicked
forever
    if <touching [Red]?> then
        say [STOP!]
    else
        say [GO!]
```

Then they drag the sprite in and out. Simple, immediate, and it makes `if/else` concrete.

### Activity B — Bumper Sprite (18 min)

```
when green flag clicked
forever
    move 5 steps
    if <touching [edge]?> then
        turn 180 degrees
    wait 0.01 seconds
```

Add a second sprite and have them bounce off each other too. Kids will spend the whole fifteen
minutes on this happily — it's the first thing that behaves like it has a mind of its own.

## 0:55–1:05 — Break

## 1:05–1:25 — Project build: catching

Goal: **"By the end of today, you can catch things and the game will notice."**

Blocks on the board: `if ... then`, `touching [player]?`, `start sound`, and the ones they
already have.

The change goes **inside the falling loop**, which is the part they'll get wrong:

```
when green flag clicked
forever
    go to x: (pick random -220 to 220) y: 170
    repeat 20
        change y by -18
        wait 0.02 seconds
        if <touching [Player]?> then
            start sound [Pop]
            go to x: (pick random -220 to 220) y: 170
```

The `go to` inside the `if` is what makes the caught object jump back to the top immediately
instead of continuing to fall through the player.

Let them struggle with placement for a few minutes before you help. The two questions to ask:

- *"When does your computer check whether you've caught it?"* (Answer: only when the `if` runs.)
- *"How many times does it check as the object falls?"* (Answer: once per trip through the
  repeat loop — twenty times.)

Then **playtest**. Everyone plays their own game for two minutes and tunes the speed. Then
swap seats and play their neighbour's for two minutes. The room will be loud. That's the point.

Save.

## 1:25–1:30 — Wrap

Save and back up carefully this week; there's more to lose now than there was.

Tell them explicitly: *"You made a game. It has no score yet, so it's a bit pointless — that's
next week."*

## Homework

1. **Catch feedback.** When you catch something, make it do something noticeable first — a
   different sound, a costume flash, a `say`, or a size change.
2. **Something you shouldn't catch.** Add a bad falling object (a bomb, a coconut, a cat). For
   now, when it touches the player it just says "Ouch!" — next week it'll cost you points.

## Bonus challenges

1. Make a sprite that says something different depending on which half of the stage it's on.
   (Hint: `if <(x position) > 0>`.)
2. Make a sprite that follows the mouse pointer, but only while the space key is held down.
3. Use `if` to stop the player leaving the stage — the thing we couldn't do in week two.
4. Combine two conditions with `and`: only catch if you're touching it **and** the space key is
   pressed. Now it's a "grab" game.

## Common bugs this week

| Symptom | Cause |
|---|---|
| Catching never works | The `if` isn't inside the `forever`/`repeat` loop |
| Catching works once, then never again | The `if` is in the outer `forever` but outside the falling `repeat` |
| Object passes through the player | The `if` fires but there's no `go to` to move it away, so it keeps falling |
| Catching works but is very fussy | The falling step is too big — it jumps past the player between checks. Smaller `change y by`, more repeats |
| `touching?` is checking the wrong thing | The dropdown defaults to the first sprite alphabetically. Check it |
| Sound doesn't play | No sound added to that sprite yet — Sounds tab, choose from the library |

The "very fussy" one is subtle and worth understanding: if the object moves 18 pixels between
checks, there are gaps where it's past the player without ever having touched it. Halving the
step and doubling the repeats fixes it, and it's a lovely accidental introduction to the idea
that computers only see the world at the moments they look.

## Notes for the second volunteer

Expect the room to fragment today — some will have catching working in five minutes and some
will still be placing the `if` at the twenty-minute mark. Get the fast ones to help their
neighbours rather than racing ahead into bonus challenges. Today of all weeks, nobody should go
home without a working catch.

## Links

- [Don't fall in!](https://projects.raspberrypi.org/en/pathways/more-scratch) — Raspberry Pi Foundation, a natural next game
- Skeleton: `Sky Catcher — end of Week 4` in the club studio
