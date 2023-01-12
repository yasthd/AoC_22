import re
from dataclasses import dataclass
import networkx as nx

SAMPLE = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k"""

with open("input") as f:
    RAW = f.read()

@dataclass
class Node:
    type_: str
    name: str
    size: int

    @staticmethod
    def parse(raw):
        nodes = raw.strip().split("\n")
        if len(nodes[0].split()) == 1:
            return Node("directory", nodes[0], 0)
        else:
            return [Node("directory", name, 0)
                    if a == "dir"
                    else Node("file", name, int(a))
                    for a, name in [l.split() for l in nodes]]

def parse(raw):
    # -> list[tuple[str, list[Node]]]
    pattern = r"\$([^\$]*)"
    commands = list(map(lambda a: a.strip(), re.findall(pattern, raw)))
    return [(c[:2], Node.parse(c[2:])) for c in commands]

def to_graph(commands):
    filesystem = nx.DiGraph()
    filesystem.add_node("/", type_="directory", size=0)
    current = "/" 
    for command in commands[1:]:
        if command[0] == "ls":
            for node in command[1]:
                new_node = current + node.name if current == "/" else current + "/" + node.name
                filesystem.add_node(new_node, type_=node.type_, size=node.size)
                filesystem.add_edge(current, new_node)
        else:
            if command[1].name == "..":
                current = list(filesystem.predecessors(current))[0]
            else:
                current = current + command[1].name if current == "/" else current + "/" + command[1].name
    return filesystem 

def get_size(g, node):
    if len(list(g.successors(node))) == 0:
        return g.nodes[node]["size"]
    else:
        return sum([get_size(g, suc) for suc in list(g.successors(node))])


parsed_commands = parse(RAW)
g = to_graph(parsed_commands)
directories = [node for node in g.nodes if g.nodes[node]["type_"] == "directory"]
directory_sizes = [s for s in map(lambda x: get_size(g, x), directories)]
required_space = 30000000 - (70000000 - get_size(g, "/")) 
print(min([s for s in directory_sizes if s >= required_space]))

#import matplotlib.pyplot as plt
#nx.draw(g, with_labels=True)
#plt.show()

