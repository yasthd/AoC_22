import re

SAMPLE = """    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2"""

with open("input") as f:
    RAW = f.read()

def parse_layout(raw: str) -> list[list[str]]:
    raw_layout = raw.split("\n")[:-1]
    layout = [list() for i in range((len(raw_layout[0])+1)//4)]
    for line in raw_layout:
        for stack, i in enumerate(range(1, len(line), 4)):
            if line[i] != " ":
                layout[stack].insert(0,(line[i]))
    return layout 

def parse_instructions(raw: str) -> list[tuple[int]]:
    pattern = r"move (\d+) from (\d+) to (\d+)"
    return [(lambda a, b, c: (int(a), int(b)-1, int(c)-1))(*re.search(pattern, line).groups()) for line in raw.strip().split("\n")]

def parse(raw: str) -> tuple[list[list[str]], list[tuple[int]]]:
    layout = parse_layout(raw.split("\n\n")[0])
    instructions = parse_instructions(raw.split("\n\n")[1])
    return layout, instructions

def operate_crane(layout: list[list[str]], instructions: list[tuple[int]]) -> str:
    for instruction in instructions:
        for i in range(instruction[0]):
            cargo = layout[instruction[1]].pop()
            layout[instruction[2]].append(cargo)
    return "".join([stack[-1] for stack in layout])

def operate_crane_9001(layout: list[list[str]], instructions: list[tuple[int]]) -> str:
    for instruction in instructions:
        cargos = layout[instruction[1]][-instruction[0]:]
        del layout[instruction[1]][-instruction[0]:]
        layout[instruction[2]].extend(cargos)
    return "".join([stack[-1] for stack in layout])

layout, instructions = parse(RAW)
new_layout = operate_crane_9001(layout, instructions)

print(new_layout)

