from dataclasses import dataclass

SAMPLE = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw"""

with open("input") as f:
    INPUT = f.read()

@dataclass
class Rucksack:
    first: str
    second: str

    def shared_prio(self):
        item_type = set(self.first).intersection(self.second).pop()
        return ord(item_type) - 96 \
            if 96 <= ord(item_type) <= 122 \
            else ord(item_type) - 38

@dataclass
class ElfGroup:
    first: str
    second: str
    third: str

    def shared_badge(self):
        badge = set(self.first).intersection(self.second) \
                    .intersection(self.third).pop()
        return ord(badge) - 96 \
            if 96 <= ord(badge) <= 122 \
            else ord(badge) - 38

def parse(rucksacks: str) -> list["Rucksack"]:
    return [Rucksack(line[:len(line)//2], line[len(line)//2:]) for line \
            in rucksacks.strip().split("\n")]

def parse_groups(rucksacks: str) -> list["ElfGroup"]:
    elfs = rucksacks.strip().split("\n")
    return [ElfGroup(elfs[i], elfs[i+1], elfs[i+2]) for i \
        in range(0, len(elfs), 3)]


rucksacks = parse(INPUT)
print(sum(rucksack.shared_prio() for rucksack in rucksacks))

elf_groups = parse_groups(INPUT)
print(sum(elf_group.shared_badge() for elf_group in elf_groups))
