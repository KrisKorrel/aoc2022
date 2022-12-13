from pathlib import Path
import string

from functools import cmp_to_key


def compare_packets(packet_a: str, packet_b: str):
    """Code is hard to read, but it works. And besides the string concatenations, it should be quite fast"""
    id_a, id_b = 0, 0
    cur_dig_a = None
    cur_dig_b = None
    cur_dig_a_start_id = None
    cur_dig_b_start_id = None
    while id_a < len(packet_a) and id_b < len(packet_b):
        # Loop until we have the entire digit
        if cur_dig_a is None and packet_a[id_a] in string.digits:
            cur_dig_a_start_id = id_a
            while packet_a[id_a] in string.digits:
                id_a += 1
            cur_dig_a = int(packet_a[cur_dig_a_start_id:id_a])
            id_a -= 1
        # Loop until we have the entire digit
        if cur_dig_b is None and packet_b[id_b] in string.digits:
            cur_dig_b_start_id = id_b
            while packet_b[id_b] in string.digits:
                id_b += 1
            cur_dig_b = int(packet_b[cur_dig_b_start_id:id_b])
            id_b -= 1

        # When both packets contain the same signal: continue
        if packet_a[id_a] in ("[", " ", ",", "]") and packet_b[id_b] == packet_a[id_a]:
            id_a += 1
            id_b += 1
        # Convert a single digit to a list containing a single digit
        elif packet_a[id_a] == "[" and cur_dig_b is not None:
            packet_b = (
                packet_b[:cur_dig_b_start_id]
                + "["
                + str(cur_dig_b)
                + "]"
                + packet_b[id_b + 1 :]
            )
            id_b = cur_dig_b_start_id
            cur_dig_b = None
        # Convert a single digit to a list containing a single digit
        elif packet_b[id_b] == "[" and cur_dig_a is not None:
            packet_a = (
                packet_a[:cur_dig_a_start_id]
                + "["
                + str(cur_dig_a)
                + "]"
                + packet_a[id_a + 1 :]
            )
            id_a = cur_dig_a_start_id
            cur_dig_a = None
        # Compare two digits
        elif cur_dig_a is not None and cur_dig_b is not None:
            if cur_dig_b < cur_dig_a:
                return -1
            if cur_dig_b > cur_dig_a:
                return 1
            id_a += 1
            id_b += 1
            cur_dig_a, cur_dig_b = None, None
        # Check whether one of the two arrays runs out
        elif packet_a[id_a] in (",", "[", *string.digits) and packet_b[id_b] == "]":
            return -1
        # Check whether one of the two arrays runs out
        elif packet_b[id_b] in (",", "[", *string.digits) and packet_a[id_a] == "]":
            return 1
        else:
            raise Exception("Unexpected state")

    return 0


def main_1():
    data_path = Path("./data/13.txt")

    packets = []
    sum_of_ordered_package_pair_ids = 0
    pair_id = 1

    with data_path.open("r") as f:
        while line := f.readline():
            line = line.strip("\n")
            if not line:
                if compare_packets(packets[0], packets[1]) == 1:
                    sum_of_ordered_package_pair_ids += pair_id
                packets = []
                pair_id += 1
            else:
                packets.append(line)

    print(sum_of_ordered_package_pair_ids)


def main_2():
    data_path = Path("./data/13.txt")

    divider_packets = [
        "[[2]]",
        "[[6]]",
    ]
    packets = []

    with data_path.open("r") as f:
        while line := f.readline():
            line = line.strip("\n")
            if not line:
                continue
            packets.append(line)

    packets.extend(divider_packets)

    packets = sorted(packets, key=cmp_to_key(compare_packets), reverse=True)

    prod = 1
    for packet_id, packet in enumerate(packets):
        if packet in divider_packets:
            prod *= packet_id + 1
    print(prod)


if __name__ == "__main__":
    main_1()
    main_2()
