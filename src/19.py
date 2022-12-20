from collections import defaultdict, deque
from dataclasses import dataclass
import itertools
from pathlib import Path
from pprint import pprint
import re
import numpy as np

from progressbar import progressbar
from itertools import product


@dataclass
class RequirementsBleuprint:
    ore_robot: int
    clay_robot: int
    obsidian_robot: tuple[int, int]
    geode_robot: tuple[int, int]


def main(data_path: Path, minutes: int, max_blueprints: int):
    blueprints = []
    with data_path.open("r") as f:
        reqs = []
        while line := f.readline():
            line = line.strip("\n")

            reqs = re.findall(
                r"Each ore robot costs (\d+) ore\. Each clay robot costs (\d+) ore\. Each obsidian robot costs (\d+) ore and (\d+) clay\. Each geode robot costs (\d+) ore and (\d+) obs",
                line,
            )[0]
            reqs = list(map(int, reqs))
            blueprints.append(
                RequirementsBleuprint(
                    reqs[0], reqs[1], (reqs[2], reqs[3]), (reqs[4], reqs[5])
                )
            )

    total = 0
    total_multiply = 1
    blueprint: RequirementsBleuprint
    for i, blueprint in enumerate(blueprints[:max_blueprints]):
        seen = set()
        q = deque([])
        max_geode = 0
        max_hist = None

        minute = 1
        ore = 0
        clay = 0
        obsidian = 0
        geode = 0
        ore_rate = 1
        clay_rate = 0
        obsidian_rate = 0
        geode_rate = 0

        max_ore_cost = max(
            [
                blueprint.ore_robot,
                blueprint.clay_robot,
                blueprint.obsidian_robot[0],
                blueprint.geode_robot[0],
            ]
        )
        max_clay_cost = blueprint.obsidian_robot[1]
        max_obsidian_cost = blueprint.geode_robot[1]

        q.append(
            (
                minute,
                ore,
                clay,
                obsidian,
                geode,
                ore_rate,
                clay_rate,
                obsidian_rate,
                geode_rate,
                # [],
            )
        )
        t = 0

        while q:
            state = q.popleft()

            (
                minute,
                ore,
                clay,
                obsidian,
                geode,
                ore_rate,
                clay_rate,
                obsidian_rate,
                geode_rate,
                # hist,
            ) = state
            ore_rate = min(ore_rate, max_ore_cost)
            clay_rate = min(clay_rate, max_clay_cost)
            obsidian_rate = min(obsidian_rate, max_obsidian_cost)

            # if [h["action"] for h in hist] == [
            #     None,
            #     None,
            #     "clay",
            #     None,
            #     "clay",
            #     None,
            #     "clay",
            #     None,
            #     None,
            #     None,
            #     "obsidian",
            #     "clay",
            #     None,
            #     None,
            #     "obsidian",
            #     None,
            #     None,
            #     "geode",
            #     None,
            #     None,
            #     "geode",
            #     None,
            #     None,
            #     None,
            # ]:
            #     print()

            if (
                geode
                + geode_rate * (minutes - minute + 1)
                + ((minutes - minute) * (minutes - minute + 1) / 2)
                <= max_geode
            ):
                continue

            state = (
                minute,
                ore,
                clay,
                obsidian,
                geode,
                ore_rate,
                clay_rate,
                obsidian_rate,
                geode_rate,
            )

            if state in seen:
                continue
            seen.add(state)

            if minute == minutes:
                geode = geode + geode_rate
                if geode > max_geode:
                    # print(geode, max_geode, hist)
                    max_geode = geode
                    # max_hist = hist
                continue

            if minute > t:
                t = minute
                print(t, max_geode)

            q.appendleft(
                (
                    minute + 1,
                    ore + ore_rate,
                    clay + clay_rate,
                    obsidian + obsidian_rate,
                    geode + geode_rate,
                    ore_rate,
                    clay_rate,
                    obsidian_rate,
                    geode_rate,
                    # hist.copy()
                    # + [
                    #     {
                    #         "action": None,
                    #         "state": state,
                    #     }
                    # ],
                )
            )

            can_build_ore = ore >= blueprint.ore_robot
            can_build_clay = ore >= blueprint.clay_robot
            can_build_obsidian = (
                ore >= blueprint.obsidian_robot[0]
                and clay >= blueprint.obsidian_robot[1]
            )
            can_build_geode = (
                ore >= blueprint.geode_robot[0] and obsidian >= blueprint.geode_robot[1]
            )
            if can_build_ore:
                q.appendleft(
                    (
                        minute + 1,
                        ore + ore_rate - blueprint.ore_robot,
                        clay + clay_rate,
                        obsidian + obsidian_rate,
                        geode + geode_rate,
                        ore_rate + 1,
                        clay_rate,
                        obsidian_rate,
                        geode_rate,
                        # hist.copy()
                        # + [
                        #     {
                        #         "action": "ore",
                        #         "state": state,
                        #     }
                        # ],
                    )
                )
            if can_build_clay:
                q.appendleft(
                    (
                        minute + 1,
                        ore + ore_rate - blueprint.clay_robot,
                        clay + clay_rate,
                        obsidian + obsidian_rate,
                        geode + geode_rate,
                        ore_rate,
                        clay_rate + 1,
                        obsidian_rate,
                        geode_rate,
                        # hist.copy()
                        # + [
                        #     {
                        #         "action": "clay",
                        #         "state": state,
                        #     }
                        # ],
                    )
                )
            if can_build_obsidian:
                q.appendleft(
                    (
                        minute + 1,
                        ore + ore_rate - blueprint.obsidian_robot[0],
                        clay + clay_rate - blueprint.obsidian_robot[1],
                        obsidian + obsidian_rate,
                        geode + geode_rate,
                        ore_rate,
                        clay_rate,
                        obsidian_rate + 1,
                        geode_rate,
                        # hist.copy()
                        # + [
                        #     {
                        #         "action": "obsidian",
                        #         "state": state,
                        #     }
                        # ],
                    )
                )
            if can_build_geode:
                q.appendleft(
                    (
                        minute + 1,
                        ore + ore_rate - blueprint.geode_robot[0],
                        clay + clay_rate,
                        obsidian + obsidian_rate - blueprint.geode_robot[1],
                        geode + geode_rate,
                        ore_rate,
                        clay_rate,
                        obsidian_rate,
                        geode_rate + 1,
                        # hist.copy()
                        # + [
                        #     {
                        #         "action": "geode",
                        #         "state": state,
                        #     }
                        # ],
                    )
                )
        print(max_geode)
        pprint(max_hist)
        total += (i + 1) * max_geode
        total_multiply *= max_geode
    print(total)
    print(total_multiply)

    # max_ore_cost = max(
    #     [
    #         blueprint.ore_robot,
    #         blueprint.clay_robot,
    #         blueprint.obsidian_robot[0],
    #         blueprint.geode_robot[0],
    #     ]
    # )
    # max_clay_cost = blueprint.obsidian_robot[1]
    # max_obsidian_cost = blueprint.geode_robot[1]
    # max_geodes_so_far = 0
    #
    # def req(
    #     action: str = None,
    #     minute=1,
    #     ore=0,
    #     clay=0,
    #     obsidian=0,
    #     geode=0,
    #     ore_rate=1,
    #     clay_rate=0,
    #     obsidian_rate=0,
    #     geode_rate=0,
    #     # could_build_ore=False,
    #     # could_build_clay=False,
    #     # could_build_obsidian=False,
    #     # could_build_geode=False,
    #     hist=[],
    # ) -> int:
    #     sit = (
    #         action,
    #         minute,
    #         ore,
    #         clay,
    #         obsidian,
    #         geode,
    #         ore_rate,
    #         clay_rate,
    #         obsidian_rate,
    #         geode_rate,
    #     )

    #     path = [h["action"] for h in hist]
    #     if path == [
    #         None,
    #         None,
    #         "clay",
    #         None,
    #         "clay",
    #         None,
    #         "clay",
    #         # None,
    #         # None,
    #         # None,
    #     ]:
    #         print()

    #     if sit in seen:
    #         return seen[sit]

    #     most_optimistic_estimate = (
    #         geode + ((1 + minutes - minute) * (minutes - minute)) / 2
    #     )
    #     nonlocal max_geodes_so_far
    #     if most_optimistic_estimate < max_geodes_so_far:
    #         seen[sit] = 0
    #         return seen[sit]

    #     can_build_ore = ore >= blueprint.ore_robot
    #     can_build_clay = ore >= blueprint.clay_robot
    #     can_build_obsidian = (
    #         ore >= blueprint.obsidian_robot[0]
    #         and clay >= blueprint.obsidian_robot[1]
    #     )
    #     can_build_geode = (
    #         ore >= blueprint.geode_robot[0] and obsidian >= blueprint.geode_robot[1]
    #     )

    #     if not action:
    #         pass
    #         # if can_build_geode:
    #         # seen[sit] = 0
    #         # return seen[sit]
    #     elif action == "ore":
    #         if can_build_ore:
    #             ore -= blueprint.ore_robot
    #         else:
    #             seen[sit] = 0
    #             return seen[sit]
    #     elif action == "clay":
    #         if can_build_clay:
    #             ore -= blueprint.clay_robot
    #         else:
    #             seen[sit] = 0
    #             return seen[sit]
    #     elif action == "obsidian":
    #         if can_build_obsidian:
    #             ore -= blueprint.obsidian_robot[0]
    #             clay -= blueprint.obsidian_robot[1]
    #         else:
    #             seen[sit] = 0
    #             return seen[sit]
    #     elif action == "geode":
    #         if can_build_geode:
    #             ore -= blueprint.geode_robot[0]
    #             obsidian -= blueprint.geode_robot[1]
    #         else:
    #             seen[sit] = 0
    #             return seen[sit]
    #     else:
    #         raise Exception()

    #     ore += ore_rate
    #     clay += clay_rate
    #     obsidian += obsidian_rate
    #     geode += geode_rate

    #     if not action:
    #         pass
    #     elif action == "ore":
    #         ore_rate += 1
    #     elif action == "clay":
    #         clay_rate += 1
    #     elif action == "obsidian":
    #         obsidian_rate += 1
    #     elif action == "geode":
    #         geode_rate += 1
    #     else:
    #         raise Exception()

    #     hist.append(
    #         {
    #             "minute": minute,
    #             "action": action,
    #             "ore": ore,
    #             "ore_rate": ore_rate,
    #             "clay": clay,
    #             "clay_rate": clay_rate,
    #             "obsidian": obsidian,
    #             "obsidian_rate": obsidian_rate,
    #             "geode": geode,
    #             "geode_rate": geode_rate,
    #         }
    #     )

    #     if minute <= minutes:
    #         m = 0

    #         m = max(
    #             m,
    #             req(
    #                 action=None,
    #                 minute=minute + 1,
    #                 ore=ore,
    #                 clay=clay,
    #                 obsidian=obsidian,
    #                 geode=geode,
    #                 ore_rate=ore_rate,
    #                 clay_rate=clay_rate,
    #                 obsidian_rate=obsidian_rate,
    #                 geode_rate=geode_rate,
    #                 # could_build_ore=can_build_ore,
    #                 # could_build_clay=can_build_clay,
    #                 # could_build_obsidian=can_build_obsidian,
    #                 # could_build_geode=can_build_geode,
    #                 hist=hist.copy(),
    #             ),
    #         )
    #         if not (not action and can_build_geode):
    #             m = max(
    #                 m,
    #                 req(
    #                     action="geode",
    #                     minute=minute + 1,
    #                     ore=ore,
    #                     clay=clay,
    #                     obsidian=obsidian,
    #                     geode=geode,
    #                     ore_rate=ore_rate,
    #                     clay_rate=clay_rate,
    #                     obsidian_rate=obsidian_rate,
    #                     geode_rate=geode_rate,
    #                     # could_build_ore=can_build_ore,
    #                     # could_build_clay=can_build_clay,
    #                     # could_build_obsidian=can_build_obsidian,
    #                     # could_build_geode=can_build_geode,
    #                     # hist=hist.copy(),
    #                 ),
    #             )

    #         if ore_rate < max_ore_cost and not (not action and can_build_ore):
    #             m = max(
    #                 m,
    #                 req(
    #                     action="ore",
    #                     minute=minute + 1,
    #                     ore=ore,
    #                     clay=clay,
    #                     obsidian=obsidian,
    #                     geode=geode,
    #                     ore_rate=ore_rate,
    #                     clay_rate=clay_rate,
    #                     obsidian_rate=obsidian_rate,
    #                     geode_rate=geode_rate,
    #                     # could_build_ore=can_build_ore,
    #                     # could_build_clay=can_build_clay,
    #                     # could_build_obsidian=can_build_obsidian,
    #                     # could_build_geode=can_build_geode,
    #                     # hist=hist.copy(),
    #                 ),
    #             )
    #         if clay_rate < max_clay_cost and not (not action and can_build_clay):
    #             m = max(
    #                 m,
    #                 req(
    #                     action="clay",
    #                     minute=minute + 1,
    #                     ore=ore,
    #                     clay=clay,
    #                     obsidian=obsidian,
    #                     geode=geode,
    #                     ore_rate=ore_rate,
    #                     clay_rate=clay_rate,
    #                     obsidian_rate=obsidian_rate,
    #                     geode_rate=geode_rate,
    #                     # could_build_ore=can_build_ore,
    #                     # could_build_clay=can_build_clay,
    #                     # could_build_obsidian=can_build_obsidian,
    #                     # could_build_geode=can_build_geode,
    #                     # hist=hist.copy(),
    #                 ),
    #             )
    #         if obsidian_rate < max_obsidian_cost and not (
    #             not action and can_build_obsidian
    #         ):
    #             m = max(
    #                 m,
    #                 req(
    #                     action="obsidian",
    #                     minute=minute + 1,
    #                     ore=ore,
    #                     clay=clay,
    #                     obsidian=obsidian,
    #                     geode=geode,
    #                     ore_rate=ore_rate,
    #                     clay_rate=clay_rate,
    #                     obsidian_rate=obsidian_rate,
    #                     geode_rate=geode_rate,
    #                     # could_build_ore=can_build_ore,
    #                     # could_build_clay=can_build_clay,
    #                     # could_build_obsidian=can_build_obsidian,
    #                     # could_build_geode=can_build_geode,
    #                     # hist=hist.copy(),
    #                 ),
    #             )

    #         seen[sit] = m
    #         return seen[sit]
    #     else:
    #         # if geode == 2:
    #         #     for h in hist:
    #         #         pprint(h)
    #         #     print()

    #         max_geodes_so_far = max(max_geodes_so_far, geode)

    #         return geode

    # max_geodes = max(
    #     [
    #         req(action=action)
    #         for action in [None, "ore", "clay", "obsidian", "geode"]
    #     ]
    # )
    # print(max_geodes)

    # ore = 1
    # clay = 0
    # obsidian = 0
    # geode = 0
    # ore_rate = 1
    # clay_rate = 0
    # obsidian_rate = 0
    # geode_rate = 0

    # for minute in range(1, minutes + 1):
    #     create = None

    #     if ore >= blueprint.geode_robot[0] and obsidian >= blueprint.geode_robot[1]:
    #         create = "geode"
    #         ore -= blueprint.geode_robot[0]
    #         obsidian -= blueprint.geode_robot[1]

    #     ore += ore_rate
    #     clay += clay_rate
    #     obsidian += obsidian_rate
    #     geode += geode_rate

    #     if create == 'clay':
    #         clay_rate += 1
    #     if create == 'obsidian':
    #         obsidian_rate += 1
    #     if create == 'geode':
    #         geode_rate += 1


if __name__ == "__main__":
    main(data_path=Path("./data/19.txt"), minutes=32, max_blueprints=3)
