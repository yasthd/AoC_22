from dataclasses import dataclass
import re

SAMPLE = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8"""

with open("input") as f:
    RAW_INPUT = f.read()

@dataclass
class ElfPair:
    first: tuple[int]
    second: tuple[int]
    
    def __init__(self, a1: str, a2: str, b1: str, b2: str) -> None:
        self.first = int(a1), int(a2)
        self.second = int(b1), int(b2)

    def overlap(self) -> bool:
        return self.first[0] >= self.second[0] \
                and self.first[1] <= self.second[1] \
                or self.second[0] >= self.first[0] \
                and self.second[1] <= self.first[1]

    def overlap_2(self) -> bool:
        return self.first[0] <= self.second[0] \
                and self.first[1] >= self.second[0] \
                or self.second[0] <= self.first[0] \
                and self.second[1] >= self.first[0]

def parse(pairs: str) -> list[ElfPair]:
    pattern = r"(\d+)-(\d+),(\d+)-(\d+)"
    return [ElfPair(*re.search(pattern, line).groups()) \
            for line in pairs.strip().split("\n")]

pair_list = parse(RAW_INPUT)
overlap_pairs = [pair for pair in pair_list if pair.overlap_2()]
print(len(overlap_pairs))
