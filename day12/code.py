import networkx as nx

SAMPLE = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi"""

with open("input") as f:
    RAW = f.read()

def create_graph(raw: str) -> nx.DiGraph:
    topo = raw.strip().split("\n")
    topo_length = len(topo)
    topo_width = len(topo[0])

    g = nx.DiGraph()
    g.add_nodes_from([((x, y), {"height": topo[y][x]})
                    for y in range(topo_length)
                    for x in range(topo_width)])

    for node in g.nodes:
        height = g.nodes[node]["height"]

        if height == "S":
            height = "a"
        elif height == "E":
            height = "z"

        for neighbor in [(node[0] + 1, node[1]),
                        (node[0], node[1] + 1)]:

            if neighbor not in g.nodes:
                continue
            
            neighbor_height = g.nodes[neighbor]["height"]
            if neighbor_height == "S":
                neighbor_height = "a"
            elif neighbor_height == "E":
                neighbor_height = "z"
            
            height_diff = abs(ord(height) - ord(neighbor_height))
            if height_diff < 2:
                g.add_edge(node, neighbor, weight=1)
                g.add_edge(neighbor, node, weight=1)
            elif neighbor_height > height:
                g.add_edge(neighbor, node, weight=1)
            else:
                g.add_edge(node, neighbor, weight=1)
    return g
            
def manhattan(a: tuple[int, int], b: tuple[int, int]) -> int:
    return sum(abs(val1-val2) for val1, val2 in zip(a,b))

def find_starts(g: nx.DiGraph) -> list[tuple[int, int]]:
    return [node for node in g.nodes
            if g.nodes[node]["height"] == "a"
            and any([neighbor for neighbor in g.neighbors(node)
                    if g.nodes[neighbor]["height"] == "b"])]

def print_map(raw: str, path: list[tuple[int, int]]) -> None:
    topo = [[*line] for line in raw.strip().split("\n")]
    for x, y in path:
        topo[y][x] = topo[y][x].upper()
    print("\n".join(["".join(line) for line in topo]))

g = create_graph(RAW)

start = [x for x, y in g.nodes(data=True) if y['height'] == "S"][0]
end = [x for x, y in g.nodes(data=True) if y['height'] == "E"][0]
starts = find_starts(g)

print(min([len(nx.astar_path(g, s, end, heuristic=manhattan)) for s in starts]) - 1)
