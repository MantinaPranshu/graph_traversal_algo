import heapq
from collections import defaultdict
import time
import tracemalloc
import networkx as nx
import gzip

class Graph:
    def __init__(self):
        self.adj = defaultdict(list)

    def add_edge(self, u, v, weight=1):
        self.adj[u].append((v, weight))

    def load_from_snap_edge_list(self, file_path, directed=False):
        open_func = gzip.open if file_path.endswith(".gz") else open
        with open_func(file_path, 'rt') as f:
            for i, line in enumerate(f):
                if line.startswith('#'):
                    continue
                u, v = map(int, line.strip().split())
                self.add_edge(u, v)
                if not directed:
                    self.add_edge(v, u)
                if i % 1_000_000 == 0 and i > 0:
                    print(f"Loaded {i} edges...")

    def dijkstra(self, start):
        dist = {}
        pq = [(0, start)]
        visited = set()

        while pq:
            current_dist, u = heapq.heappop(pq)
            if u in visited:
                continue
            visited.add(u)
            dist[u] = current_dist

            for v, weight in self.adj[u]:
                if v not in visited:
                    heapq.heappush(pq, (current_dist + weight, v))

        return dist


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
    time_taken = t_end - t_start
    memory_peak = peak / 1024 / 1024  # Convert to MB
    print(f"{label} - Time: {time_taken:.2f} sec, Peak Memory: {memory_peak:.2f} MB")
    return result, time_taken, memory_peak


# ========== MAIN ==========

if __name__ == "__main__":
    path_to_snap_file = "/Users/pranshumantina/Downloads/email-Eu-core.txt"  # or .txt.gz
    source_node = 1  # Update with actual node present in the graph

    # ---------- Custom Dijkstra ----------
    print("Loading custom graph...")
    custom_graph = Graph()
    _, _, _ = benchmark_memory_and_time(
        custom_graph.load_from_snap_edge_list,
        path_to_snap_file,
        False,
        label="Custom Graph Load"
    )

    custom_result, custom_time, custom_mem = benchmark_memory_and_time(
        custom_graph.dijkstra,
        source_node,
        label="Custom Dijkstra"
    )

    # Save distances to file
    with open("dijkstra_distances.txt", "w") as f:
        for node in sorted(custom_result.keys()):
            f.write(f"Node {node}: Distance = {custom_result[node]}\n")

    # ---------- NetworkX Dijkstra ----------
    print("\nLoading NetworkX graph...")
    nx_graph, _, _ = benchmark_memory_and_time(
        load_graph_networkx,
        path_to_snap_file,
        False,
        label="NetworkX Graph Load"
    )

    nx_result, nx_time, nx_mem = benchmark_memory_and_time(
        nx.single_source_dijkstra_path_length,
        nx_graph,
        source_node,
        label="NetworkX Dijkstra"
    )

    # ---------- Summary ----------
    print("\n========== Performance Summary ==========")
    print(f"Custom Dijkstra    - Time: {custom_time:.2f} sec, Memory: {custom_mem:.2f} MB")
    print(f"NetworkX Dijkstra  - Time: {nx_time:.2f} sec, Memory: {nx_mem:.2f} MB")
