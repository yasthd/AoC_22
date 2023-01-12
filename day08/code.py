import math

SAMPLE = """30373
25512
65332
33549
35390"""

with open("input") as f:
    RAW = f.read()

def tree_scenic(forest, tree, direction = None, height = None):
    if len(set(tree).intersection({0, len(forest)-1})) != 0:
        return 0
    if not height:
        height = forest[tree[1]][tree[0]]
    if direction:
        next_tree = (tree[0]+direction[0], tree[1]+direction[1])
        visible = height > forest[next_tree[1]][next_tree[0]]
        if not visible:
            return 1
        else:
            return 1 + tree_scenic(forest, next_tree, direction, height) 
    else: 
        return math.prod([tree_scenic(forest, (tree[0], tree[1]), (x, y)) for x, y in [(0, -1), (1, 0), (0, 1), (-1, 0)]])

def tree_visible(forest, tree, direction = None, height = None):
    if len(set(tree).intersection({0, len(forest)-1})) != 0:
        return True
    if not height:
        height = forest[tree[1]][tree[0]]
    if direction:
        next_tree = (tree[0]+direction[0], tree[1]+direction[1])
        visible = height > forest[next_tree[1]][next_tree[0]]
        if not visible:
            return False
        else:
            return tree_visible(forest, next_tree, direction, height) 
    else: 
        return any(tree_visible(forest, (tree[0], tree[1]), (x, y)) for x, y in [(0, -1), (1, 0), (0, 1), (-1, 0)])

def forest_scenic(forest):
    return max([tree_scenic(forest, (x, y)) for x in range(len(forest)) for y in range(len(forest))])

def forest_visibility(forest):
    return sum([tree_visible(forest, (x, y)) for x in range(len(forest)) for y in range(len(forest))])

def parse(raw):
    return raw.strip().split("\n")

forest = parse(RAW)
print(forest_scenic(forest))

