import networkx as nx
import time
import tracemalloc
import gzip

def load_graph_networkx(path, directed=False):
    G = nx.DiGraph() if directed else nx.Graph()
    open_func = gzip.open if path.endswith(".gz") else open
    with open_func(path, 'rt') as f:
        G = nx.parse_edgelist(
            f,
            nodetype=int,
            data=(("weight", float),),
            create_using=G,
            comments="#"
        )
    print(f"Graph with {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")
    num_selfloops = nx.number_of_selfloops(G)
    print(f"Number of self-loops: {num_selfloops}")
    if num_selfloops > 0:
        print("Removing self-loops...")
        G.remove_edges_from(nx.selfloop_edges(G))

    # Restrict to first 2000 nodes
    first_2000_nodes = list(G.nodes())[:2000]
    G = G.subgraph(first_2000_nodes).copy()
    print(f"Reduced graph to {G.number_of_nodes()} nodes and {G.number_of_edges()} edges")

    return G

def benchmark_memory_and_time(func, *args, label="", **kwargs):
    tracemalloc.start()
    t_start = time.time()
    result = func(*args, **kwargs)
    t_end = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"{label} - Time: {t_end - t_start:.2f} sec, Peak Memory: {peak / 1024 / 1024:.2f} MB")
    return result

def custom_maximum_matching(G):
    matching = set()
    visited = set()
    for idx, u in enumerate(G):
        if idx % 100 == 0:
            print(f"Iteration {idx}: visiting node {u}")
        if u not in visited:
            for v in G[u]:
                if v not in visited and u != v:
                    matching.add((u, v))
                    visited.add(u)
                    visited.add(v)
                    break
    return matching

if __name__ == "__main__":
    path = '/Users/pranshumantina/Downloads/LARGE GRAPHS/loc-brightkite_edges.txt'

    print("Loading graph...")
    G = benchmark_memory_and_time(load_graph_networkx, path, False, label="Graph Load")

    print("\nRunning custom Maximum Matching...")
    _ = benchmark_memory_and_time(custom_maximum_matching, G, label="Custom Maximum Matching")

    print("\nRunning NetworkX Max Cardinality Matching...")
    _ = benchmark_memory_and_time(
        nx.max_weight_matching, G, maxcardinality=True, label="NetworkX Max Cardinality Matching"
    )

    print("\nRunning NetworkX Maximal Matching (Greedy)...")
    _ = benchmark_memory_and_time(nx.maximal_matching, G, label="NetworkX Maximal Matching")
