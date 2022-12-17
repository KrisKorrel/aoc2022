from dataclasses import dataclass
import itertools
from pathlib import Path
import re
import numpy as np

from progressbar import progressbar


def main(data_path: Path, rocks_to_fall: int, width: int):
    blow_pattern = data_path.read_text()

    # Points relative to origin at the bottom-left extrema of the shape
    shape_patterns = [
        [[0, 0], [1, 0], [2, 0], [3, 0]],  # horizontal line
        [[1, 0], [0, 1], [1, 1], [2, 1], [1, 2]],  # cross
        [[0, 0], [1, 0], [2, 0], [2, 1], [2, 2]],  # reverse L
        [[0, 0], [0, 1], [0, 2], [0, 3]],  # revertical line
        [[0, 0], [1, 0], [0, 1], [1, 1]],  # block
    ]

    shape_idx = 0
    blow_index = 0
    mode = "fall"
    fallen_rocks = 0
    cur_stack_height = 0
    cur_stack = set()
    cur_shape = None

    seen_situations = {}

    while fallen_rocks < rocks_to_fall:
        if not cur_shape:
            cur_shape = shape_patterns[shape_idx % len(shape_patterns)]
            shape_idx += 1
            cur_shape = [(p[0] + 2, p[1] + cur_stack_height + 3) for p in cur_shape]

            # print()
            # print()
            # print(fallen_rocks)
            # lines = ["+-------+"]
            # for i in range(cur_stack_height + 10):
            #     line = ["|"]
            #     for j in range(width):
            #         if (j, i) in cur_stack:
            #             line.append("#")
            #         elif [j, i] in cur_shape:
            #             line.append("%")
            #         else:
            #             line.append(".")
            #     line.append("|")
            #     lines.append("".join(line))
            # lines = reversed(lines)
            # for line in lines:
            #     print(line)
            # print()
            # print()
            # print()
            # if fallen_rocks == 3:
            #     exit()

            mode = "push"

            continue

        if mode == "fall":
            fallen_shape = [(p[0], p[1] - 1) for p in cur_shape]
            allow_fall = True
            for p in fallen_shape:
                if p[1] < 0 or p in cur_stack:
                    allow_fall = False
                    break

            if allow_fall:
                cur_shape = fallen_shape
                mode = "push"
                continue
            else:
                for p in cur_shape:
                    cur_stack.add(p)
                    cur_stack_height = max(cur_stack_height, p[1] + 1)
                cur_shape = None
                fallen_rocks += 1

                # -10 is tricky and not guaranteed to give the same situation
                situation = (
                    shape_idx % (len(shape_patterns)),
                    blow_index % (len(blow_pattern)),
                    tuple(
                        sorted(
                            [
                                (p[0], cur_stack_height - p[1])
                                for p in cur_stack
                                if p[1] > cur_stack_height - 20
                            ]
                        )
                    ),
                )

                if situation in seen_situations:
                    prev_stack_height, prev_fallen_rocks = seen_situations[situation]
                    rocks_delta_in_cycle = fallen_rocks - prev_fallen_rocks
                    height_delta_in_cycle = cur_stack_height - prev_stack_height
                    n_cycles_to_shortcut = (
                        rocks_to_fall - fallen_rocks
                    ) // rocks_delta_in_cycle
                    cur_stack_height = cur_stack_height + (
                        n_cycles_to_shortcut * height_delta_in_cycle
                    )
                    fallen_rocks = fallen_rocks + (
                        n_cycles_to_shortcut * rocks_delta_in_cycle
                    )
                    cur_stack = {
                        (p[0], p[1] + n_cycles_to_shortcut * height_delta_in_cycle)
                        for p in cur_stack
                    }

                seen_situations[situation] = (cur_stack_height, fallen_rocks)

        elif mode == "push":
            blow = blow_pattern[blow_index % len(blow_pattern)]
            blow_index += 1
            allow_blow = True
            blown_shape = [
                (p[0] - 1, p[1]) if blow == "<" else (p[0] + 1, p[1]) for p in cur_shape
            ]

            for p in blown_shape:
                if p[0] < 0 or p[0] > width - 1 or p in cur_stack:
                    allow_blow = False
                    break

            if allow_blow:
                cur_shape = blown_shape

            mode = "fall"

    print(cur_stack_height)


if __name__ == "__main__":
    main(
        data_path=Path("./data/17.txt"),
        rocks_to_fall=2022,
        width=7,
    )
    main(
        data_path=Path("./data/17.txt"),
        rocks_to_fall=1000000000000,
        width=7,
    )
