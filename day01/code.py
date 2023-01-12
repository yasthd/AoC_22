with open("input") as f:
    print(sum(sorted([sum(map(int,foods.strip().split())) for foods in f.read().strip().split("\n\n")], reverse=True)[:3]))
