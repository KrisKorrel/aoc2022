from collections import defaultdict, deque
from dataclasses import dataclass
import itertools
from pathlib import Path
import re
import numpy as np

from progressbar import progressbar
from itertools import product


def main(data_path: Path):
    cubes = {
        tuple(map(int, line.split(","))) for line in data_path.read_text().splitlines()
    }
    min_x, min_y, min_z = np.inf, np.inf, np.inf
    max_x, max_y, max_z = -np.inf, -np.inf, -np.inf

    visible_sides = 0
    for cube in cubes:
        x, y, z = cube
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        min_z = min(min_z, z)
        max_x = max(max_x, x)
        max_y = max(max_y, y)
        max_z = max(max_z, z)

        for delta in (-1, 1):
            if (x + delta, y, z) not in cubes:
                visible_sides += 1
            if (x, y + delta, z) not in cubes:
                visible_sides += 1
            if (x, y, z + delta) not in cubes:
                visible_sides += 1
    print(visible_sides)

    air_cubes = set()
    cubes_to_eval = set([(min_x - 1, min_y - 1, min_z - 1)])
    faces_on_outside = 0
    while cubes_to_eval:
        cube_to_eval = cubes_to_eval.pop()
        x, y, z = cube_to_eval
        for delta in (-1, 1):
            for neighbor in ((x + delta, y, z), (x, y + delta, z), (x, y, z + delta)):
                if neighbor in air_cubes:
                    pass
                elif neighbor in cubes:
                    faces_on_outside += 1
                elif (
                    min_x - 1 <= neighbor[0] <= max_x + 1
                    and min_y - 1 <= neighbor[1] <= max_y + 1
                    and min_z - 1 <= neighbor[2] <= max_z + 1
                ):
                    cubes_to_eval.add(neighbor)
        air_cubes.add(cube_to_eval)

    print(faces_on_outside)


if __name__ == "__main__":
    main(data_path=Path("./data/18.txt"))
