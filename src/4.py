import heapq
from pathlib import Path
import string


def main_1() -> int:
    data_path = Path("./data/4.txt")

    contained_pairs = 0

    with data_path.open("r") as f:
        while line := f.readline():
            line = line.strip("\n")

            sections_1, sections_2 = line.split(",")
            sections_1_min, sections_1_max = sections_1.split("-")
            sections_2_min, sections_2_max = sections_2.split("-")
            sections_1_min, sections_1_max = int(sections_1_min), int(sections_1_max)
            sections_2_min, sections_2_max = int(sections_2_min), int(sections_2_max)

            if (
                sections_1_min >= sections_2_min and sections_1_max <= sections_2_max
            ) or (
                sections_2_min >= sections_1_min and sections_2_max <= sections_1_max
            ):
                contained_pairs += 1

    print(contained_pairs)


def main_2() -> int:
    data_path = Path("./data/4.txt")

    num_overlapping_sections = 0

    with data_path.open("r") as f:
        while line := f.readline():
            line = line.strip("\n")

            sections_1, sections_2 = line.split(",")
            sections_1_min, sections_1_max = sections_1.split("-")
            sections_2_min, sections_2_max = sections_2.split("-")
            sections_1_min, sections_1_max = int(sections_1_min), int(sections_1_max)
            sections_2_min, sections_2_max = int(sections_2_min), int(sections_2_max)

            if (
                sections_1_min >= sections_2_min and sections_1_min <= sections_2_max
            ) or (
                sections_2_min >= sections_1_min and sections_2_min <= sections_1_max
            ):
                num_overlapping_sections += 1

    print(num_overlapping_sections)


if __name__ == "__main__":
    main_1()
    main_2()
