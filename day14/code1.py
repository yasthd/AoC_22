from itertools import chain
import time

SAMPLE = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

with open("input") as f:
    RAW = f.read()

def get_outline(raw: str) -> tuple[tuple[int, int], tuple[int, int]]:
    xs = []
    ys = []
    lines = [line.split(" -> ") for line in raw.strip().split("\n")]
    for x, y in [point.split(",") for point in chain(*lines)]:
        xs.append(int(x))
        ys.append(int(y))
    return (min(xs), 0), (max(xs), max(ys))

def parse(raw: str,
        min_point: tuple[int, int],
        max_point: tuple[int, int]
) -> list[list[str]]:
    cave = [["."] * (max_point[0]-min_point[0]+1)
            for i in range(max_point[1]-min_point[1]+1)]
    lines = [line.split(" -> ") for line in raw.strip().split("\n")]
    for line in lines:
        for i in range(len(line)-1):
            start = [int(a) for a in line[i].split(",")]
            end = [int(a) for a in line[i+1].split(",")]
            y_range = sorted([start[1]-min_point[1], end[1]-min_point[1]])
            y_range[1] += 1
            x_range = sorted([start[0]-min_point[0], end[0]-min_point[0]])
            x_range[1] += 1
            for y in range(*y_range):
                for x in range(*x_range):
                    cave[y][x] = "#"
    return cave

def simulate_one(cave: list[list[str]],
        sand: tuple[int, int],
) -> tuple[int, int]:
    sand_possible = [(sand[0], sand[1]+1), (sand[0]-1, sand[1]+1), (sand[0]+1, sand[1]+1)]
    for sand_next in sand_possible:
        if cave[sand_next[1]][sand_next[0]] == ".":
            cave[sand[1]][sand[0]] = "."
            cave[sand_next[1]][sand_next[0]] = "o"
            return sand_next
    return None

def simulate_all(cave: list[list[str]],
        sand_start: tuple[int, int],
        animate: bool = False
) -> int:
    if animate:
        print(f"\033[{len(cave[:len(cave)//2])}S", end="")
        print(f"\033[{len(cave[:len(cave)//2])}A", end="")
        print("\033[s", end="")
    for i in range(len(cave)*len(cave[0])):
        sand = sand_start
        try:
            while sand := simulate_one(cave, sand):
                if animate:
                    time.sleep(0.4)
                    print("\033[u", end="")
                    for line in cave[:len(cave)//2]:
                        print("".join(line))
        except IndexError as e:
            return i

min_point, max_point = get_outline(RAW)
sand_start = (500-min_point[0], 0)
cave = parse(RAW, min_point, max_point)

print(simulate_all(cave, sand_start, True))

