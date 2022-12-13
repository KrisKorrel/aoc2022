import itertools
from pathlib import Path
import numpy as np


def read_grid(data_path: Path) -> np.ndarray:
    grid = []

    with data_path.open("r") as f:
        while line := f.readline():
            line = line.strip("\n")
            row = [ord(char) for char in line]
            grid.append(row)

    grid = np.asarray(grid)

    return grid


def main_1():
    data_path = Path("./data/12.txt")
    grid = read_grid(data_path)

    # Not optimal, should be done while constructing the grid
    start_pos, end_pos = None, None
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if chr(grid[y, x]) == "S":
                start_pos = (y, x)
                grid[start_pos] = ord("a")
            if chr(grid[y, x]) == "E":
                end_pos = (y, x)
                grid[end_pos] = ord("z")

    tentative_distances = np.ones_like(grid) * np.inf
    tentative_distances[start_pos] = 0
    unvisited = set(
        itertools.product(list(range(grid.shape[0])), list(range(grid.shape[1])))
    )
    while unvisited:
        min_dist, min_v = None, None
        # Not optimal. priority queue might be a better alternative?
        for v in unvisited:
            if min_dist is None or tentative_distances[v] < min_dist:
                min_dist = tentative_distances[v]
                min_v = v

        cur_pos = min_v

        if cur_pos == end_pos:
            break

        unvisited.remove(cur_pos)
        cur_height = grid[cur_pos]

        for next_pos in (
            (cur_pos[0] - 1, cur_pos[1]),
            (cur_pos[0] + 1, cur_pos[1]),
            (cur_pos[0], cur_pos[1] - 1),
            (cur_pos[0], cur_pos[1] + 1),
        ):
            if (
                not 0 <= next_pos[0] < grid.shape[0]
                or not 0 <= next_pos[1] < grid.shape[1]
            ):
                continue

            next_height = grid[next_pos]
            if next_height - cur_height > 1:
                continue

            tentative_distances[next_pos] = min(
                tentative_distances[next_pos], tentative_distances[cur_pos] + 1
            )

    print(tentative_distances[end_pos])


def main_2():
    data_path = Path("./data/12.txt")
    grid = read_grid(data_path)

    # Not optimal, should be done while constructing the grid
    start_pos, end_pos = None, None
    for y in range(grid.shape[0]):
        for x in range(grid.shape[1]):
            if chr(grid[y, x]) == "S":
                start_pos = (y, x)
                grid[start_pos] = ord("a")
            if chr(grid[y, x]) == "E":
                end_pos = (y, x)
                grid[end_pos] = ord("z")

    tentative_distances = np.ones_like(grid) * np.inf
    tentative_distances[end_pos] = 0
    unvisited = set(
        itertools.product(list(range(grid.shape[0])), list(range(grid.shape[1])))
    )
    while unvisited:
        min_dist, min_v = None, None
        # Not optimal. priority queue might be a better alternative?
        for v in unvisited:
            if min_dist is None or tentative_distances[v] < min_dist:
                min_dist = tentative_distances[v]
                min_v = v

        cur_pos = min_v

        if grid[cur_pos] == ord("a"):
            print(tentative_distances[cur_pos])
            break

        unvisited.remove(cur_pos)
        cur_height = grid[cur_pos]

        for next_pos in (
            (cur_pos[0] - 1, cur_pos[1]),
            (cur_pos[0] + 1, cur_pos[1]),
            (cur_pos[0], cur_pos[1] - 1),
            (cur_pos[0], cur_pos[1] + 1),
        ):
            if (
                not 0 <= next_pos[0] < grid.shape[0]
                or not 0 <= next_pos[1] < grid.shape[1]
            ):
                continue

            next_height = grid[next_pos]
            if cur_height - next_height > 1:
                continue

            tentative_distances[next_pos] = min(
                tentative_distances[next_pos], tentative_distances[cur_pos] + 1
            )


if __name__ == "__main__":
    main_1()
    main_2()
