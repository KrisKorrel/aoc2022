from collections import defaultdict
import heapq
from pathlib import Path
import string
import re


def main(expected_marker_length: int) -> int:
    data_path = Path("./data/6.txt")

    with data_path.open("r") as f:
        line = f.readline()
        line.strip("\n")

    latest_chars = defaultdict(int)
    message_start_idx = None
    for i, char in enumerate(line):
        latest_chars[char] += 1
        if i < expected_marker_length:
            continue

        drop_idx = line[i - expected_marker_length]
        latest_chars[drop_idx] -= 1
        if not latest_chars[drop_idx]:
            del latest_chars[drop_idx]

        if len(latest_chars) == expected_marker_length:
            message_start_idx = i + 1
            break

    print(message_start_idx)


if __name__ == "__main__":
    main(4)
    main(14)
