import json
from functools import cmp_to_key
from copy import deepcopy

SAMPLE = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]
"""

with open("input") as f:
    RAW = f.read()

def parse(raw: str) -> list[list[int]]:
    packages = [[[2]], [[6]]]
    for pair in raw.strip().split("\n\n"):
        for package in pair.split("\n"):
            packages.append(json.loads(package))
    return packages

def parse_pairs(raw: str) -> list[tuple[list[int]]]:
    return [(json.loads(a), json.loads(b))
            for a, b in [pair.split("\n")
            for pair in raw.strip().split("\n\n")]]

def check_order(a: list[int], b: list[int]) -> int:
    a = deepcopy(a)
    b = deepcopy(b)
    a_0 = a.pop(0) if a else None
    b_0 = b.pop(0) if b else None

    match a_0, b_0:

        case int(), int():
            if a_0 < b_0:
                return -1
            elif a_0 > b_0:
                return 1
            else:
                return check_order(a, b)

        case list(), list():
            match check_order(a_0, b_0):
                case 0:
                    return check_order(a, b)
                case -1:
                    return -1
                case 1:
                    return 1

        case list(), int():
            a.insert(0, a_0)
            b.insert(0, [b_0])
            return check_order(a, b)

        case int(), list():
            a.insert(0, [a_0])
            b.insert(0, b_0)
            return check_order(a, b)

        case None, None:
            return 0

        case None, x:
            return -1

        case x, None:
            return 1

        case x:
            print(f"Unknown case: {x}")

def compute_sum(pairs: list[tuple[list[int]]]):
    return sum([i for i, (a, b) in enumerate(pairs, 1)
                if check_order(a, b) == -1])

pairs = parse_pairs(RAW)
print(compute_sum(pairs))

packets = sorted(parse(RAW), key=cmp_to_key(check_order))
print((packets.index([[2]])+1) * (packets.index([[6]])+1))
