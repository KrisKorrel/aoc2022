import heapq
from pathlib import Path


def main_1() -> int:
    data_path = Path("./data/2.txt")

    score = 0
    # rock (X) -> 1
    # paper (Y) -> 2
    # scissors (Z) -> 3
    base_score = {"X": 1, "Y": 2, "Z": 3}
    # rock-rock (A-X) -> draw (3)
    # rock-paper (A-Y) -> win (6)
    # rock-scissors (A-Z) -> draw (0)
    # etc.
    game_score = {
        ("A", "X"): 3,
        ("A", "Y"): 6,
        ("A", "Z"): 0,
        ("B", "X"): 0,
        ("B", "Y"): 3,
        ("B", "Z"): 6,
        ("C", "X"): 6,
        ("C", "Y"): 0,
        ("C", "Z"): 3,
    }

    with data_path.open("r") as f:
        while line := f.readline():
            line = line.strip("\n")

            choice_opponent, choice_self = line.split(" ")
            score += base_score[choice_self]
            score += game_score[(choice_opponent, choice_self)]

    print(score)


def main_2() -> int:
    data_path = Path("./data/2.txt")

    score = 0
    # lose (X) -> 0
    # draw (Y) -> 3
    # win (Z) -> 6
    game_score = {"X": 0, "Y": 3, "Z": 6}
    # rock-scissors (lose) -> 3
    # rock-rock (draw) -> 1
    # rock-paper (win) -> 2
    # etc.
    base_score = {
        ("A", "X"): 3,
        ("A", "Y"): 1,
        ("A", "Z"): 2,
        ("B", "X"): 1,
        ("B", "Y"): 2,
        ("B", "Z"): 3,
        ("C", "X"): 2,
        ("C", "Y"): 3,
        ("C", "Z"): 1,
    }

    with data_path.open("r") as f:
        while line := f.readline():
            line = line.strip("\n")

            choice_opponent, choice_self = line.split(" ")
            score += base_score[(choice_opponent, choice_self)]
            score += game_score[choice_self]

    print(score)


if __name__ == "__main__":
    main_1()
    main_2()
