# Hanoi Crossing

# Rules

Two players share a cross-shaped board: each has a private start pole and a private goal pole, plus one shared middle pole that both can use.
Player A starts with the odd disks, player B with the even disks, stacked largest-at-bottom on their start pole.
A turn moves the top disk from one visible pole to another; a disk may only land on an empty pole or on a strictly larger disk.
A player wins when their start pole is empty and their goal pole holds all of their disks.

# How to run

```
uv sync
uv run hanoi-crossing
uv run hanoi-crossing --order 0 1 0
uv run hanoi-crossing --replay examples/replay.txt
uv run hanoi-crossing --replay examples/replay.txt --format yaml
uv run pytest
```

`uv run hanoi-crossing` - random play mode (despite it's name - it's more interactive than 'random')
`uv run hanoi-crossing --order 0 1 0` - run with given order of moves
`uv run hanoi-crossing --replay examples/replay.txt` - run replay of pre-recorded game
`uv run hanoi-crossing --format yaml` - get results in parse-friendly yaml format


# AI use
Tasks
- basic rewrites
- bugfix

Tools
- Cursor