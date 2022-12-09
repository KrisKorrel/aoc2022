from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import numpy as np


def step(
    h_pos: tuple[int, int],
    t_pos: tuple[int, int],
    direction: str,
    visited: set[tuple[int, int]],
):
    match direction:
        case "U":
            h_pos = (h_pos[0] - 1, h_pos[1])
        case "D":
            h_pos = (h_pos[0] + 1, h_pos[1])
        case "L":
            h_pos = (h_pos[0], h_pos[1] - 1)
        case "R":
            h_pos = (h_pos[0], h_pos[1] + 1)

    if h_pos == t_pos:
        pass
    elif abs(t_pos[0] - h_pos[0]) <= 1 and abs(t_pos[1] - h_pos[1]) <= 1:
        pass
    elif t_pos[0] < h_pos[0] and t_pos[1] < h_pos[1]:
        t_pos = (t_pos[0] + 1, t_pos[1] + 1)
    elif t_pos[0] < h_pos[0] and t_pos[1] > h_pos[1]:
        t_pos = (t_pos[0] + 1, t_pos[1] - 1)
    elif t_pos[0] > h_pos[0] and t_pos[1] < h_pos[1]:
        t_pos = (t_pos[0] - 1, t_pos[1] + 1)
    elif t_pos[0] > h_pos[0] and t_pos[1] > h_pos[1]:
        t_pos = (t_pos[0] - 1, t_pos[1] - 1)
    elif t_pos[0] == h_pos[0] and t_pos[1] - h_pos[1] == 2:
        t_pos = (t_pos[0], t_pos[1] - 1)
    elif t_pos[0] == h_pos[0] and t_pos[1] - h_pos[1] == -2:
        t_pos = (t_pos[0], t_pos[1] + 1)
    elif t_pos[0] - h_pos[0] == 2 and t_pos[1] == h_pos[1]:
        t_pos = (t_pos[0] - 1, t_pos[1])
    elif t_pos[0] - h_pos[0] == -2 and t_pos[1] == h_pos[1]:
        t_pos = (t_pos[0] + 1, t_pos[1])

    visited.add(t_pos)

    return h_pos, t_pos


def step2(
    knots: list[tuple[int, int]],
    direction: str,
    visited: set[tuple[int, int]],
):
    head = knots[0]
    match direction:
        case "U":
            head = (head[0] - 1, head[1])
        case "D":
            head = (head[0] + 1, head[1])
        case "L":
            head = (head[0], head[1] - 1)
        case "R":
            head = (head[0], head[1] + 1)
    knots[0] = head

    for i in range(1, len(knots)):
        h_pos = knots[i - 1]
        t_pos = knots[i]

        if h_pos == t_pos:
            pass
        elif abs(t_pos[0] - h_pos[0]) <= 1 and abs(t_pos[1] - h_pos[1]) <= 1:
            pass
        elif t_pos[0] < h_pos[0] and t_pos[1] < h_pos[1]:
            t_pos = (t_pos[0] + 1, t_pos[1] + 1)
        elif t_pos[0] < h_pos[0] and t_pos[1] > h_pos[1]:
            t_pos = (t_pos[0] + 1, t_pos[1] - 1)
        elif t_pos[0] > h_pos[0] and t_pos[1] < h_pos[1]:
            t_pos = (t_pos[0] - 1, t_pos[1] + 1)
        elif t_pos[0] > h_pos[0] and t_pos[1] > h_pos[1]:
            t_pos = (t_pos[0] - 1, t_pos[1] - 1)
        elif t_pos[0] == h_pos[0] and t_pos[1] - h_pos[1] == 2:
            t_pos = (t_pos[0], t_pos[1] - 1)
        elif t_pos[0] == h_pos[0] and t_pos[1] - h_pos[1] == -2:
            t_pos = (t_pos[0], t_pos[1] + 1)
        elif t_pos[0] - h_pos[0] == 2 and t_pos[1] == h_pos[1]:
            t_pos = (t_pos[0] - 1, t_pos[1])
        elif t_pos[0] - h_pos[0] == -2 and t_pos[1] == h_pos[1]:
            t_pos = (t_pos[0] + 1, t_pos[1])

        knots[i] = t_pos

    visited.add(t_pos)

    return knots


def main_1() -> int:
    h_pos = 0, 0
    t_pos = 0, 0
    visited = set()

    data_path = Path("./data/9.txt")
    with data_path.open("r") as f:
        while line := f.readline():
            line = line.strip("\n")
            direction, steps = line.split(" ")
            steps = int(steps)

            for _ in range(steps):
                h_pos, t_pos = step(h_pos, t_pos, direction, visited)

    print(len(visited))


def main_2() -> int:
    knots = [(0, 0)] * 10
    visited = set()

    data_path = Path("./data/9.txt")
    with data_path.open("r") as f:
        while line := f.readline():
            line = line.strip("\n")
            direction, steps = line.split(" ")
            steps = int(steps)

            for _ in range(steps):
                knots = step2(knots, direction, visited)

    print(len(visited))


if __name__ == "__main__":
    main_1()
    main_2()
