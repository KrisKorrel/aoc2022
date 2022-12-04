import heapq
from pathlib import Path


def main() -> int:
    data_path = Path("./data/1.txt")

    cur_calories = 0
    top_3_calories = [0, 0, 0]

    with data_path.open("r") as f:
        while line := f.readline():
            # Remove newline
            line = line[:-1]

            if not line:
                if cur_calories > heapq.nsmallest(1, top_3_calories)[0]:
                    heapq.heapreplace(top_3_calories, cur_calories)
                cur_calories = 0
            else:
                cur_calories += int(line)

    top_3_calories = sorted(top_3_calories, reverse=True)

    print(top_3_calories[0])
    print(sum(top_3_calories))


if __name__ == "__main__":
    main()
