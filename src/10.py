from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import numpy as np


def main_1() -> int:
    data_path = Path("./data/10.txt")
    x = 1
    cycle = 0
    sum_of_signal_strengths = 0

    def _maybe_increase_sum_of_signal_strengths(sum_of_signal_strengths, cycle, x):
        if (cycle - 20) % 40 == 0:
            sum_of_signal_strengths += cycle * x

        return sum_of_signal_strengths

    with data_path.open("r") as f:
        while line := f.readline():
            line = line.strip("\n")

            if line == "noop":
                cycle += 1
                sum_of_signal_strengths = _maybe_increase_sum_of_signal_strengths(
                    sum_of_signal_strengths, cycle, x
                )
            else:
                addition = int(line.split(" ")[1])
                cycle += 1
                sum_of_signal_strengths = _maybe_increase_sum_of_signal_strengths(
                    sum_of_signal_strengths, cycle, x
                )
                cycle += 1
                sum_of_signal_strengths = _maybe_increase_sum_of_signal_strengths(
                    sum_of_signal_strengths, cycle, x
                )
                x += addition

    print(sum_of_signal_strengths)


def main_2() -> int:
    data_path = Path("./data/10.txt")
    x = 1
    cycle = 0
    screen = []

    def _draw(screen):
        screen_pos = len(screen) % 40
        if abs(screen_pos - x) <= 1:
            screen.append("#")
        else:
            screen.append(".")

    with data_path.open("r") as f:
        while line := f.readline():
            line = line.strip("\n")

            if line == "noop":
                cycle += 1
                _draw(screen)
            else:
                addition = int(line.split(" ")[1])
                cycle += 1
                _draw(screen)

                cycle += 1
                _draw(screen)
                x += addition

    for line in range(len(screen) // 40):
        print("".join(screen[line * 40 : (line + 1) * 40]))


if __name__ == "__main__":
    main_1()
    main_2()
"""
12460
"""
