with open("sample") as f:
    SAMPLE = f.read()

with open("input") as f:
    RAW = f.read()

def parse(raw: str) -> list[int]:
    instructions = []
    for line in raw.strip().split("\n"):
        cmd = line.split()[0]
        if cmd == "noop":
            instructions.append(0)
        else:
            num = int(line.split()[1])
            instructions.extend([0, num])
    return instructions

def get_signal(cycle: int, instructions: list[int]) -> int:
    return cycle * (sum(instructions[:cycle-1])+1)

def sum_of_cycles(cycles: list[int], instuctions: list[int]) -> int:
    return sum([get_signal(c, instructions) for c in cycles])

def draw_crt(instructions: list[int]) -> str:
    crt = ""
    reg = 1
    for inst in instructions:
        if len(crt) % 40 in [reg-1, reg, reg+1]:
            crt += "#"
        else:
            crt += "."
        reg += inst
    return "\n".join([crt[i:i+40] for i in [0, 40, 80, 120, 160, 200]])

instructions = parse(RAW)
print(sum_of_cycles([20, 60, 100, 140, 180, 220], instructions))
print(draw_crt(instructions))

