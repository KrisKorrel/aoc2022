import heapq
from pathlib import Path
import string
import re


def main_1() -> int:
    data_path = Path("./data/5.txt")

    stacks = None

    with data_path.open("r") as f:
        while line := f.readline():
            line = line.strip("\n")

            if not line:
                break
            if line[1] == "1":
                continue

            if stacks is None:
                stacks = [[] for _ in range((len(line) + 1) // 4)]

            for stack_id, stack in enumerate(stacks):
                char = line[stack_id * 4 + 1]
                if char != " ":
                    stack.append(char)

        stacks = [stack[::-1] for stack in stacks]

        while line := f.readline():
            line = line.strip("\n")

            n, move_from_idx, move_to_idx = re.findall(
                r"move ([0-9]*) from ([0-9]*) to ([0-9]*)", line
            )[0]
            n, move_from_idx, move_to_idx = (
                int(n),
                int(move_from_idx),
                int(move_to_idx),
            )

            for _ in range(n):
                top = stacks[move_from_idx - 1].pop(-1)
                stacks[move_to_idx - 1].append(top)

    res = "".join(stack[-1] for stack in stacks)
    print(res)


def main_2() -> int:
    data_path = Path("./data/5.txt")

    stacks = None

    with data_path.open("r") as f:
        while line := f.readline():
            line = line.strip("\n")

            if not line:
                break
            if line[1] == "1":
                continue

            if stacks is None:
                stacks = [[] for _ in range((len(line) + 1) // 4)]

            for stack_id, stack in enumerate(stacks):
                char = line[stack_id * 4 + 1]
                if char != " ":
                    stack.append(char)

        stacks = [stack[::-1] for stack in stacks]

        while line := f.readline():
            line = line.strip("\n")

            n, move_from_idx, move_to_idx = re.findall(
                r"move ([0-9]*) from ([0-9]*) to ([0-9]*)", line
            )[0]
            n, move_from_idx, move_to_idx = (
                int(n),
                int(move_from_idx),
                int(move_to_idx),
            )

            temp_stack = []
            for _ in range(n):
                top = stacks[move_from_idx - 1].pop(-1)
                temp_stack.append(top)
            for top in temp_stack[::-1]:
                stacks[move_to_idx - 1].append(top)

    res = "".join(stack[-1] for stack in stacks)
    print(res)


if __name__ == "__main__":
    main_1()
    main_2()
