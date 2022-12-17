import itertools
from pathlib import Path
import re
import numpy as np

from progressbar import progressbar


def main(data_path, max_steps: int, train_elephant: bool):
    valves = {}

    with data_path.open("r") as f:
        while line := f.readline():
            line = line.strip("\n")
            valve, flow_rate, next_valves = re.findall(
                r"Valve (.*) has flow rate=(.*); tunnels? leads? to valves? (.*)",
                line,
            )[0]
            next_valves = next_valves.split(", ")
            valves[valve] = (int(flow_rate), next_valves)

    # Inefficiently calculate shortest path from all valves to all valves
    dists = {}
    for start_valve in valves:
        unvisited = set([valve for valve in valves])
        tentative_distances = {valve: np.inf for valve in valves}
        tentative_distances[start_valve] = 0

        while unvisited:
            min_dist, min_dist_valve = np.inf, None
            for valve in unvisited:
                if tentative_distances[valve] < min_dist:
                    min_dist = tentative_distances[valve]
                    min_dist_valve = valve
            unvisited.remove(min_dist_valve)

            for next_valve in valves[min_dist_valve][1]:
                tentative_distances[next_valve] = min(
                    tentative_distances[next_valve],
                    tentative_distances[min_dist_valve] + 1,
                )
        dists[start_valve] = tentative_distances

    # We can condense the graph as most nodes have zero flow
    non_zero_flow_valves = set([valve for valve in valves if valves[valve][0]])

    cache = {}

    def get_max_flow(
        cur_valve: str,
        step: int,
        valves_open: set,
        elephant_still_has_to_go: bool,
    ):
        if step > max_steps:
            # Ashamed to admit that I had to steal this idea
            # (https://www.youtube.com/watch?v=DgqkVDr1WX8)
            if elephant_still_has_to_go:
                return get_max_flow(
                    cur_valve="AA",
                    step=1,
                    valves_open=valves_open,
                    elephant_still_has_to_go=False,
                )
            return 0

        cache_key = (
            cur_valve,
            step,
            tuple(sorted(list(valves_open))),
            elephant_still_has_to_go,
        )
        if cache_key in cache:
            return cache[cache_key]

        max_flow = 0
        if cur_valve in non_zero_flow_valves:
            valves_open = valves_open.union(set([cur_valve]))
            max_flow += valves[cur_valve][0] * (max_steps - step)
            step += 1

        sub_max_flow = 0
        for next_valve in non_zero_flow_valves - valves_open:
            dist = dists[cur_valve][next_valve]
            sub_max_flow = max(
                sub_max_flow,
                get_max_flow(
                    cur_valve=next_valve,
                    step=step + dist,
                    valves_open=valves_open,
                    elephant_still_has_to_go=elephant_still_has_to_go,
                ),
            )
        max_flow += sub_max_flow

        cache[cache_key] = max_flow

        return max_flow

    max_flow = get_max_flow(
        cur_valve="AA",
        step=1,
        valves_open=set(),
        elephant_still_has_to_go=train_elephant,
    )

    print(max_flow)


if __name__ == "__main__":
    main(data_path=Path("./data/16.txt"), max_steps=30, train_elephant=False)
    main(data_path=Path("./data/16.txt"), max_steps=26, train_elephant=True)
