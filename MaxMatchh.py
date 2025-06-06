import networkx as nx
import time
import tracemalloc
import gzip
from collections import defaultdict

def load_graph_networkx(path, directed=False):
    G = nx.DiGraph() if directed else nx.Graph()
    open_func = gzip.open if path.endswith(".gz") else open
    with open_func(path, 'rt') as f:
        G = nx.parse_edgelist(f, nodetype=int, create_using=G, comments='#')
    return G

def benchmark_memory_and_time(func, *args, label=""):
    tracemalloc.start()
    t_start = time.time()
    result = func(*args)
    t_end = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"{label} - Time: {t_end - t_start:.2f} sec, Peak Memory: {peak / 1024 / 1024:.2f} MB")
    return result

# Greedy approximation for custom maximum matching
def custom_maximum_matching(G):
    matching = set()
    visited = set()
    for u in G:
        if u not in visited:
            for v in G[u]:
                if v not in visited:
                    matching.add((u, v))
                    visited.add(u)
                    visited.add(v)
                    break
    return matching

if __name__ == "__main__":
    path = "/Users/pranshumantina/Downloads/email-Eu-core.txt"
    
    print("Loading graph...")
    G = benchmark_memory_and_time(load_graph_networkx, path, False, label="Graph Load")

    print("\nRunning custom Max Matching...")
    _ = benchmark_memory_and_time(custom_maximum_matching, G, label="Custom Maximum Matching")

    print("\nRunning NetworkX Max Matching...")
    _ = benchmark_memory_and_time(nx.max_weight_matching, G, label="NetworkX Maximum Matching")
