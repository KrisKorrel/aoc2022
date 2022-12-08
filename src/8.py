from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
import numpy as np


def read_trees_data(data_path: Path) -> np.ndarray:
    trees = []

    with data_path.open("r") as f:
        while line := f.readline():
            line = line.strip("\n")
            tree_heights = [int(char) for char in line]
            trees.append(tree_heights)

    trees = np.asarray(trees)

    return trees


def get_visible_trees_in_line(tree_line: list[int]) -> list[int]:
    cur_max_height = None
    visible_trees = []
    for tree_height in tree_line:
        if cur_max_height is None or tree_height > cur_max_height:
            cur_max_height = tree_height

            visible_trees.append(1)
        else:
            visible_trees.append(0)

    return visible_trees


def get_visible_trees_in_line_optimized(tree_line: list[int]) -> list[int]:
    visible_trees = [0] * len(tree_line)
    index_a = 0
    tree_height_a = tree_line[index_a]
    visible_trees[index_a] = 1

    index_b = len(tree_line) - 1
    tree_height_b = tree_line[index_b]
    visible_trees[index_b] = 1

    while index_a < index_b:
        if tree_height_a == 9 and tree_height_b == 9:
            break

        if tree_height_a < tree_height_b:
            index_a += 1
            new_tree_height = tree_line[index_a]
            if new_tree_height > tree_height_a:
                visible_trees[index_a] = 1
                tree_height_a = new_tree_height
        else:
            index_b -= 1
            new_tree_height = tree_line[index_b]
            if new_tree_height > tree_height_b:
                visible_trees[index_b] = 1
                tree_height_b = new_tree_height

    return visible_trees


def main_1_naive() -> int:
    trees = read_trees_data(Path("./data/8.txt"))
    visible_trees = np.zeros_like(trees)

    for height in range(trees.shape[0]):
        tree_line = trees[height, :].tolist()
        visible_trees_in_line = get_visible_trees_in_line(tree_line)
        visible_trees[height, :] |= visible_trees_in_line

        tree_line = reversed(tree_line)
        visible_trees_in_line = get_visible_trees_in_line(tree_line)
        visible_trees[height, ::-1] |= visible_trees_in_line

    for width in range(trees.shape[1]):
        tree_line = trees[:, width].tolist()
        visible_trees_in_line = get_visible_trees_in_line(tree_line)
        visible_trees[:, width] |= visible_trees_in_line

        tree_line = reversed(tree_line)
        visible_trees_in_line = get_visible_trees_in_line(tree_line)
        visible_trees[::-1, width] |= visible_trees_in_line

    num_visible_trees = np.sum(visible_trees)

    print(num_visible_trees)


def main_1_optimized() -> int:
    trees = read_trees_data(Path("./data/8.txt"))
    visible_trees = np.zeros_like(trees)

    for height in range(trees.shape[0]):
        tree_line = trees[height, :]
        visible_trees_in_line = get_visible_trees_in_line_optimized(tree_line)
        visible_trees[height, :] |= visible_trees_in_line

    for width in range(trees.shape[1]):
        tree_line = trees[:, width].tolist()
        visible_trees_in_line = get_visible_trees_in_line_optimized(tree_line)
        visible_trees[:, width] |= visible_trees_in_line

    num_visible_trees = np.sum(visible_trees)

    print(num_visible_trees)


def get_scenic_score(trees: np.ndarray, start_height: int, start_width: int) -> int:
    base_tree_height = trees[start_height, start_width]
    scenic_scores = [0, 0, 0, 0]

    for height in range(start_height + 1, trees.shape[0]):
        scenic_scores[0] += 1
        if trees[height, start_width] >= base_tree_height:
            break
    for height in range(start_height - 1, -1, -1):
        scenic_scores[1] += 1
        if trees[height, start_width] >= base_tree_height:
            break
    for width in range(start_width + 1, trees.shape[1]):
        scenic_scores[2] += 1
        if trees[start_height, width] >= base_tree_height:
            break
    for width in range(start_width - 1, -1, -1):
        scenic_scores[3] += 1
        if trees[start_height, width] >= base_tree_height:
            break

    return np.prod(scenic_scores)


def main_2() -> int:
    trees = read_trees_data(Path("./data/8.txt"))
    max_scenic_score = 0

    for height in range(trees.shape[0]):
        for width in range(trees.shape[1]):
            scenic_score = get_scenic_score(
                trees=trees, start_height=height, start_width=width
            )
            max_scenic_score = max(scenic_score, max_scenic_score)

    print(max_scenic_score)


if __name__ == "__main__":
    main_1_naive()
    main_1_optimized()
    main_2()
