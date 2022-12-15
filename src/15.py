from pathlib import Path
import re

from progressbar import progressbar


def main(
    data_path: Path,
    row_search_space_min: int,
    row_search_space_max: int,
    column_seach_space_min: int,
    column_search_space_max: int,
    print_locations: bool,
):
    sensor2beacon = {}
    min_x, min_y, max_x, max_y = None, None, None, None

    with data_path.open("r") as f:
        while line := f.readline():
            re_result = re.findall(
                r"Sensor at x=([-0-9]*), y=([-0-9]*): closest beacon is at x=([-0-9]*), y=([-0-9]*)",
                line,
            )
            sensor_x, sensor_y, beacon_x, beacon_y = re_result[0]
            sensor_x = int(sensor_x)
            sensor_y = int(sensor_y)
            beacon_x = int(beacon_x)
            beacon_y = int(beacon_y)

            min_x = (
                beacon_x
                if min_x is None
                else min(min_x, beacon_x - abs(beacon_y - sensor_y))
            )
            min_y = (
                beacon_y
                if min_y is None
                else min(min_y, beacon_y - abs(beacon_x - sensor_x))
            )
            max_x = (
                beacon_x
                if max_x is None
                else max(max_x, beacon_x + abs(beacon_y - sensor_y))
            )
            max_y = (
                beacon_y
                if max_y is None
                else max(max_y, beacon_y + abs(beacon_x - sensor_x))
            )

            sensor2beacon[(sensor_x, sensor_y)] = (beacon_x, beacon_y)

    for row_index in progressbar(range(row_search_space_min, row_search_space_max + 1)):
        spans = []
        for sensor, beacon in sensor2beacon.items():
            manhatten_distance = abs(sensor[0] - beacon[0]) + abs(sensor[1] - beacon[1])
            distance_to_row = abs(sensor[1] - row_index)
            leftover = manhatten_distance - distance_to_row

            if leftover < 0:
                continue

            span_min = sensor[0] - leftover
            span_max = sensor[0] + leftover

            if (
                column_seach_space_min is not None
                and column_search_space_max is not None
                and (
                    span_min > column_search_space_max
                    or span_max < column_seach_space_min
                )
            ):
                continue

            spans.append(
                (
                    max(
                        column_seach_space_min
                        if column_seach_space_min is not None
                        else span_min,
                        span_min,
                    ),
                    min(
                        column_search_space_max
                        if column_search_space_max is not None
                        else span_max,
                        span_max,
                    ),
                )
            )

        spans = sorted(spans)

        extended_spans = []
        cur_span = spans[0]

        for span in spans[1:]:
            if span[0] > cur_span[1] + 1:
                extended_spans.append(cur_span)
                cur_span = span
            else:
                cur_span = (cur_span[0], max(span[1], cur_span[1]))
        extended_spans.append(cur_span)

        if len(extended_spans) > 1 and print_locations:
            print()
            print(row_search_space_max * (extended_spans[0][1] + 1) + row_index)
            break
        elif not print_locations:
            nope = 0
            for span in extended_spans:
                nope += span[1] - span[0]
            print()
            print(nope)


if __name__ == "__main__":
    main(
        data_path=Path("./data/15.txt"),
        row_search_space_min=2000000,
        row_search_space_max=2000000,
        column_seach_space_min=None,
        column_search_space_max=None,
        print_locations=False,
    )
    main(
        data_path=Path("./data/15.txt"),
        row_search_space_min=0,
        row_search_space_max=4000000,
        column_seach_space_min=0,
        column_search_space_max=4000000,
        print_locations=True,
    )
