import networkx as nx
import time
import tracemalloc
import gzip
from collections import defaultdict, deque

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

def custom_betweenness_centrality(G):
    betweenness = dict.fromkeys(G.nodes(), 0.0)
    for s in G:
        stack = []
        pred = {w: [] for w in G}
        sigma = dict.fromkeys(G, 0.0); sigma[s] = 1.0
        dist = dict.fromkeys(G, -1); dist[s] = 0
        queue = deque([s])
        while queue:
            v = queue.popleft()
            stack.append(v)
            for w in G[v]:
                if dist[w] < 0:
                    queue.append(w)
                    dist[w] = dist[v] + 1
                if dist[w] == dist[v] + 1:
                    sigma[w] += sigma[v]
                    pred[w].append(v)
        delta = dict.fromkeys(G, 0.0)
        while stack:
            w = stack.pop()
            for v in pred[w]:
                delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
            if w != s:
                betweenness[w] += delta[w]
    return betweenness

if __name__ == "__main__":
    path = "/Users/pranshumantina/Downloads/email-Eu-core.txt"
    
    print("Loading graph...")
    G = benchmark_memory_and_time(load_graph_networkx, path, False, label="Graph Load")

    print("\nRunning custom Brandes BC...")
    _ = benchmark_memory_and_time(custom_betweenness_centrality, G, label="Custom Betweenness Centrality")

    print("\nRunning NetworkX Brandes BC...")
    _ = benchmark_memory_and_time(nx.betweenness_centrality, G, label="NetworkX Betweenness Centrality")
