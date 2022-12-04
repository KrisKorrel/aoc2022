import heapq
from pathlib import Path
import string


def main_1() -> int:
    data_path = Path("./data/3.txt")

    sum_of_priorities = 0
    priorities = {}
    for i, char in enumerate(string.ascii_lowercase + string.ascii_uppercase):
        priorities[char] = i + 1

    with data_path.open("r") as f:
        while line := f.readline():
            line = line.strip("\n")

            length = len(line) // 2
            compartment_1 = line[:length]
            compartment_2 = line[length:]

            compartment_1_unique = set(list(compartment_1))
            for item in compartment_2:
                if item in compartment_1_unique:
                    sum_of_priorities += priorities[item]
                    break

    print(sum_of_priorities)


def main_2() -> int:
    data_path = Path("./data/3.txt")

    sum_of_priorities = 0
    cur_group = []
    priorities = {}
    for i, char in enumerate(string.ascii_lowercase + string.ascii_uppercase):
        priorities[char] = i + 1

    with data_path.open("r") as f:
        while line := f.readline():
            line = line.strip("\n")

            cur_group.append(line)

            if len(cur_group) == 3:
                common_items = (
                    set(list(cur_group[0]))
                    .intersection(set(list(cur_group[1])))
                    .intersection(set(list(cur_group[2])))
                )
                assert len(common_items) == 1
                badge = list(common_items)[0]
                sum_of_priorities += priorities[badge]

                cur_group = []

    print(sum_of_priorities)


if __name__ == "__main__":
    main_1()
    main_2()
