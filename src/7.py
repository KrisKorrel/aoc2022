from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path


@dataclass
class File:
    name: str
    size: int


@dataclass
class Dir:
    name: str
    parent: Dir
    files: list[File]
    sub_dirs: list[Dir]


def process_cd(line: str, cur_dir: Dir, root: Dir) -> Dir:
    new_dir_name = line[5:]
    if new_dir_name == "/":
        return root
    elif new_dir_name == "..":
        return cur_dir.parent
    for sub_dir in cur_dir.sub_dirs:
        if sub_dir.name == new_dir_name:
            return sub_dir
    else:
        raise Exception()


def process_commands(data_path: Path) -> Dir:
    root = Dir("/", parent=None, files=[], sub_dirs=[])
    cur_dir = root

    with data_path.open("r") as f:
        while line := f.readline():
            line = line.strip("\n")

            if line.startswith("$ ls"):
                continue
            elif line.startswith("$ cd"):
                cur_dir = process_cd(line=line, cur_dir=cur_dir, root=root)
            elif line.startswith("dir"):
                sub_dir = Dir(line[4:], parent=cur_dir, files=[], sub_dirs=[])
                cur_dir.sub_dirs.append(sub_dir)
            else:
                size, file_name = line.split(" ", 1)
                size = int(size)
                file = File(file_name, size)
                cur_dir.files.append(file)

    return root


def main_1() -> int:
    data_path = Path("./data/7.txt")

    root = process_commands(data_path=data_path)

    sum_of_small_dirs = 0

    def get_sum_of_small_dirs(cur_dir: Dir):
        nonlocal sum_of_small_dirs

        cur_dir_size = 0
        for file in cur_dir.files:
            cur_dir_size += file.size
        for sub_dir in cur_dir.sub_dirs:
            cur_dir_size += get_sum_of_small_dirs(sub_dir)

        if cur_dir_size < 100_000:
            sum_of_small_dirs += cur_dir_size

        return cur_dir_size

    get_sum_of_small_dirs(root)

    print(sum_of_small_dirs)


def main_2() -> int:
    data_path = Path("./data/7.txt")

    root = process_commands(data_path=data_path)

    deletion_candidate, deletion_candidate_size = None, None
    system_size = 70_000_000
    required_space = 30_000_000

    def get_used_space(cur_dir: Dir):
        cur_dir_size = 0
        for file in cur_dir.files:
            cur_dir_size += file.size
        for sub_dir in cur_dir.sub_dirs:
            cur_dir_size += get_used_space(sub_dir)

        return cur_dir_size

    used_space = get_used_space(root)

    def get_deletion_candidate(cur_dir: Dir):
        nonlocal deletion_candidate, deletion_candidate_size
        cur_dir_size = 0
        for file in cur_dir.files:
            cur_dir_size += file.size
        for sub_dir in cur_dir.sub_dirs:
            cur_dir_size += get_deletion_candidate(sub_dir)

        if system_size - used_space + cur_dir_size >= required_space and (
            deletion_candidate is None or deletion_candidate_size > cur_dir_size
        ):
            deletion_candidate = cur_dir
            deletion_candidate_size = cur_dir_size

        return cur_dir_size

    get_deletion_candidate(root)

    print(deletion_candidate_size)


if __name__ == "__main__":
    main_1()
    main_2()
