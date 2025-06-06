import networkx as nx
import time
import tracemalloc
import gzip
from collections import defaultdict
import community as community_louvain  # pip install python-louvain

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

# Placeholder for custom Louvain implementation
def custom_louvain(G):
    # A simplified placeholder - real implementation is complex
    return community_louvain.best_partition(G)

if __name__ == "__main__":
    path = "/Users/pranshumantina/Downloads/email-Eu-core.txt"

    print("Loading graph...")
    G = benchmark_memory_and_time(load_graph_networkx, path, False, label="Graph Load")

    print("\nRunning custom Louvain...")
    partition1 = benchmark_memory_and_time(custom_louvain, G, label="Custom Louvain")

    print("\nRunning NetworkX Louvain...")
    partition2 = benchmark_memory_and_time(community_louvain.best_partition, G, label="NetworkX Louvain")
