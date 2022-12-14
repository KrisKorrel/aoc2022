from pathlib import Path


def construct_rock_structure(data_path: Path):
    rocks = set()
    absolute_min_y = None

    with data_path.open("r") as f:
        while line := f.readline():
            line = line.strip("\n")
            vertices = line.split(" -> ")
            cur_pos = list(map(int, vertices[0].split(",")))

            for vertex in vertices:
                end_pos = list(map(int, vertex.split(",")))

                min_x = min(cur_pos[0], end_pos[0])
                max_x = max(cur_pos[0], end_pos[0])
                min_y = min(cur_pos[1], end_pos[1])
                max_y = max(cur_pos[1], end_pos[1])

                if absolute_min_y is None or min_y > absolute_min_y:
                    absolute_min_y = min_y

                for x in range(min_x, max_x + 1):
                    for y in range(min_y, max_y + 1):
                        rocks.add((x, y))
                cur_pos = end_pos

    return rocks, absolute_min_y


def main_1():
    data_path = Path("./data/14.txt")

    rocks, min_y = construct_rock_structure(data_path)

    cur_sand_pos = (500, 0)
    n_grains = 0
    while cur_sand_pos[1] < min_y:
        if (down_pos := (cur_sand_pos[0], cur_sand_pos[1] + 1)) not in rocks:
            cur_sand_pos = down_pos
        elif (down_left_pos := (cur_sand_pos[0] - 1, cur_sand_pos[1] + 1)) not in rocks:
            cur_sand_pos = down_left_pos
        elif (
            down_right_pos := (cur_sand_pos[0] + 1, cur_sand_pos[1] + 1)
        ) not in rocks:
            cur_sand_pos = down_right_pos
        else:
            rocks.add(cur_sand_pos)
            cur_sand_pos = (500, 0)
            n_grains += 1

    print(n_grains)


def main_2():
    data_path = Path("./data/14.txt")

    rocks, min_y = construct_rock_structure(data_path)

    cur_sand_pos = (500, 0)
    n_grains = 0
    while True:
        if (
            down_pos := (cur_sand_pos[0], cur_sand_pos[1] + 1)
        ) not in rocks and cur_sand_pos[1] < min_y + 1:
            cur_sand_pos = down_pos
        elif (
            down_left_pos := (cur_sand_pos[0] - 1, cur_sand_pos[1] + 1)
        ) not in rocks and cur_sand_pos[1] < min_y + 1:
            cur_sand_pos = down_left_pos
        elif (
            down_right_pos := (cur_sand_pos[0] + 1, cur_sand_pos[1] + 1)
        ) not in rocks and cur_sand_pos[1] < min_y + 1:
            cur_sand_pos = down_right_pos
        else:
            n_grains += 1
            if cur_sand_pos == (500, 0):
                break

            rocks.add(cur_sand_pos)
            cur_sand_pos = (500, 0)

    print(n_grains)


if __name__ == "__main__":
    main_1()
    main_2()
