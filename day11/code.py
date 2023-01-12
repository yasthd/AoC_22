from dataclasses import dataclass
import operator
import re
import math

PRIME_GROUP = math.lcm(7, 11, 13, 3, 17, 2, 5, 19)
SAMPLE_PRIME_GROUP = math.lcm(23, 19, 13, 17)

with open("sample") as f:
    SAMPLE = f.read()

with open("input") as f:
    RAW = f.read()

@dataclass
class Monkey:
    items: list[int]
    operation: tuple[int, operator, int]
    test: int 
    next_monkey: tuple[int, int]
    inspected: int = 0

    @staticmethod
    def from_string(raw: str) -> "Monkey":
        pattern = r"Monkey (\d+):\s+" +\
                r"Starting items: ([\d, ]+)\s+" +\
                r"Operation: new = ([\w\*\+ ]+)\s+" +\
                r"Test: divisible by (\d+)\s+" +\
                r"If true: throw to monkey (\d+)\s+" +\
                r"If false: throw to monkey (\d+)"
        _, items, operation, test, next_monkey_1, next_monkey_2 = re.search(pattern, raw).groups()
        items = [int(x.strip()) for x in items.strip().split(", ")]
        operation = tuple(int(x) if x.isnumeric()
                        else x if x.isalpha()
                        else operator.mul if x == "*"
                        else operator.add
                        for x in operation.strip().split())
        test = int(test)
        next_monkey = (int(next_monkey_1), int(next_monkey_2))
        return Monkey(items, operation, test, next_monkey)

    def perform_operation(self, divisor: int) -> None:
        self.inspected += 1
        #doesnt work anymore for part 1 -> add "// 3" to make it work
        self.items[0] = self.operation[1](*[x if isinstance(x, int)
                                        else self.items[0]
                                        for x in self.operation[::2]]) % divisor

    def pass_item(self) -> tuple[int, int]:
        item = self.items.pop(0)
        return (item, self.next_monkey[0]) \
                if item % self.test == 0 \
                else (item, self.next_monkey[1])

def monkey_handler(rounds: int, monkeys: list[Monkey], divisor: int = 3) -> int:
    for _ in range(rounds):
        for i in range(len(monkeys)):
            while monkeys[i].items:
                monkeys[i].perform_operation(divisor)
                item, monkey = monkeys[i].pass_item()
                monkeys[monkey].items.append(item)
    return math.prod(sorted([m.inspected for m in monkeys])[-2:])

monkeys = [Monkey.from_string(s) for s in RAW.strip().split("\n\n")]
monkey_business = monkey_handler(10000, monkeys, PRIME_GROUP)
print(monkey_business)
