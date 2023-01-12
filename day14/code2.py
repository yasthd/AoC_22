from itertools import chain

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

def parse(raw: str, max_y: int) -> list[list[str]]:
    lines = [line.split(" -> ") for line in raw.strip().split("\n")]
    cave = [["."] * 1000 for i in range(max_y+2)]
    cave.append(["#"] * 1000)
    for line in lines:
        for i in range(len(line)-1):
            start = [int(a) for a in line[i].split(",")]
            end = [int(a) for a in line[i+1].split(",")]
            y_range = sorted([start[1], end[1]])
            y_range[1] += 1
            x_range = sorted([start[0], end[0]])
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

def simulate_all(cave: list[list[str]], sand_start: tuple[int, int]) -> int:
    for i in range(len(cave)*len(cave[0])):
        sand = sand_start
        while True:
            old_sand = sand
            sand = simulate_one(cave, sand)
            if not sand and old_sand == (500, 0):
                return i+1
            if not sand:
                break

_, max_point = get_outline(RAW)
sand_start = (500, 0)
cave = parse(RAW, max_point[1])

print(simulate_all(cave, sand_start))

