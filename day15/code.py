import re
import z3

SAMPLE = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""

with open ("input") as f:
    INPUT = f.read()

def parse(raw: str) -> list[tuple[tuple[int, int], tuple[int, int]]]:
    pattern = r"[a-zA-Z\s]+=(-?\d+), y=(-?\d+):[a-z\s]+=(-?\d+), y=(-?\d+)"
    return [((int(a), int(b)), (int(c), int(d))) for a, b, c ,d
            in [re.findall(pattern, line)[0] for line in raw.strip().split("\n")]]

def manhattan(a: tuple[int, int], b: tuple[int, int]) -> int:
    return sum(abs(val1-val2) for val1, val2 in zip(a,b))

def process_sensor(ruled_out: set[tuple[int, int]], sensor: tuple[int, int], beacon: tuple[int, int], target_row: int):
    dist_beacon = manhattan(sensor, beacon)
    if not (sensor[1]-dist_beacon <= target_row <= sensor[1]+dist_beacon):
        return
    dist_target = target_row - sensor[1]
    for x in range(-abs(abs(dist_target)-dist_beacon), abs(abs(dist_target)-dist_beacon)+1):
        point = (sensor[0]+x, sensor[1]+dist_target)
        assert point[1] == target_row
        if not point == beacon:
            ruled_out.add((sensor[0]+x, sensor[1]+dist_target))

def count_ruled_out(report: list[tuple[tuple[int, int], tuple[int, int]]], target_row: int = 2_000_000) -> int:
    ruled_out = set()
    for sensor, beacon in report:
        process_sensor(ruled_out, sensor, beacon, target_row)
    return len([(x, y) for x, y in ruled_out if y == target_row])

def find_frequency(report: list[tuple[tuple[int, int], tuple[int, int]]], bound: int = 4_000_000) -> int:
    solver = z3.Solver()
    x = z3.Int("x")
    y = z3.Int("y")
    solver.add(x >= 0, x <= bound)
    solver.add(y >= 0, y <= bound)
    for sensor, beacon in report:
        dist_beacon = manhattan(sensor, beacon)
        solver.add(z3.Abs(sensor[0]-x) + z3.Abs(sensor[1]-y) > dist_beacon)
    solver.check()
    model = solver.model()
    return model[x].as_long()*4_000_000 + model[y].as_long()

assert count_ruled_out(parse(SAMPLE), 10) == 26

report = parse(INPUT)
#print(count_ruled_out(report))
                   
assert find_frequency(parse(SAMPLE), 20) == 56_000_011

print(find_frequency(report))
