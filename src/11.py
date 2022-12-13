from __future__ import annotations
from dataclasses import dataclass
from pathlib import Path
from typing import Union
import numpy as np
import re
from collections import deque
from progressbar import progressbar


@dataclass
class Monkey:
    items: deque[int]
    operation: str
    operation_arg: Union[str, int]
    test_mod: int
    true_case: int
    false_case: int
    divide_worry_level: bool
    touched_items: int = 0

    @staticmethod
    def from_text(lines: list[str], divide_worry_level) -> Monkey:
        items = re.findall(r".*Starting items: ([0-9, ]*)", lines[1])[0]
        items = [int(item) for item in items.split(", ")]

        operation, operation_arg = re.findall(
            r".*Operation: new = old ([\+\*]) (.*)", lines[2]
        )[0]
        try:
            operation_arg = int(operation_arg)
        except ValueError:
            pass

        test_mod = re.findall(r".*Test: divisible by ([0-9]*)", lines[3])[0]
        test_mod = int(test_mod)

        true_case = re.findall(r".*If true: throw to monkey ([0-9]*)", lines[4])[0]
        false_case = re.findall(r".*If false: throw to monkey ([0-9]*)", lines[5])[0]
        true_case = int(true_case)
        false_case = int(false_case)

        return Monkey(
            items=deque(items),
            operation=operation,
            operation_arg=operation_arg,
            test_mod=test_mod,
            true_case=true_case,
            false_case=false_case,
            divide_worry_level=divide_worry_level,
        )

    def eval_items(self) -> list[tuple[int, int]]:
        evaluated_items = []

        for _ in range(len(self.items)):
            item = self.items.popleft()

            operation_arg = self.operation_arg
            if operation_arg == "old":
                operation_arg = item
            if self.operation == "+":
                item = item + operation_arg
            else:
                item = item * operation_arg
            if self.divide_worry_level:
                item = int(item / 3)
            item %= self.max_mod

            if item % self.test_mod == 0:
                evaluated_items.append((item, self.true_case))
            else:
                evaluated_items.append((item, self.false_case))
            self.touched_items += 1

        return evaluated_items


def main_1(rounds: int, divide_worry_level: bool) -> int:
    data_path = Path("./data/11.txt")

    cur_lines = []
    monkeys: list[Monkey] = []

    with data_path.open("r") as f:
        while line := f.readline():
            line = line.strip("\n")

            if not line:
                monkeys.append(Monkey.from_text(cur_lines, divide_worry_level))
                cur_lines = []
                continue

            cur_lines.append(line)
        monkeys.append(Monkey.from_text(cur_lines, divide_worry_level))

    max_mod = np.prod([monkey.test_mod for monkey in monkeys])
    for monkey in monkeys:
        monkey.max_mod = max_mod

    for _ in progressbar(range(rounds)):
        t = 0
        for monkey in monkeys:
            throw_items = monkey.eval_items()
            for item, monkey_idx in throw_items:
                monkeys[monkey_idx].items.append(item)
                t += 1

    touched_items = sorted([monkey.touched_items for monkey in monkeys], reverse=True)
    monkey_business = np.prod(touched_items[:2])
    print(monkey_business)


if __name__ == "__main__":
    main_1(rounds=20, divide_worry_level=True)
    main_1(rounds=10_000, divide_worry_level=False)
