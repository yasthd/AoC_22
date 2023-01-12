SAMPLE = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2"""

SAMPLE_2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20"""

with open("input") as f:
    RAW = f.read()

DIR = {"U": (0, 1), "R": (1, 0), "D": (0, -1), "L": (-1, 0)}

def parse(raw: str) -> list[tuple[int]]:
    return [tuple(map(lambda x: x*int(line[2:]), DIR[line[0]]))
            for line in raw.strip().split("\n")]

def sign(a: int) -> int:
    return max(-1, min(1, a)) 

def touching(head: tuple[int], tail: tuple[int]) -> bool:
    return abs(head[0] - tail[0]) < 2 and abs(head[1] - tail[1]) < 2

def tail_follow(head: tuple[int], tail: tuple[int]) -> tuple[int]:
    return tuple(sign(h-t) + t  for h, t in zip(head, tail))

def compute_steps(steps: list[tuple[int]]) -> int:
    steps_taken = {(0, 0)}
    head = (0, 0)
    tail = (0, 0)
    for step in steps:
        for _ in range(max([abs(x) for x in step])):
            direction = [sign(x) for x in step]
            head = tuple(h + d for h, d in zip(head, direction))
            if not touching(head, tail):
                tail = tail_follow(head, tail)
                steps_taken.add(tail)
    return len(steps_taken)

def compute_steps_2(steps: list[tuple[int]]) -> int:
    steps_taken = {(0, 0)}
    knots = [(0, 0) for _ in range(10)]
    for step in steps:
        for _ in range(max([abs(x) for x in step])):
            direction = [sign(x) for x in step]
            knots[0] = tuple(h + d for h, d in zip(knots[0], direction))
            for i in range(1, len(knots)):
                if not touching(knots[i-1], knots[i]):
                    knots[i] = tail_follow(knots[i-1], knots[i])
                    if i == 9:
                        steps_taken.add(knots[i])
    return len(steps_taken)

steps = parse(RAW)
print(compute_steps_2(steps))
