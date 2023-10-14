import graphs
from time import time
from random import choice
from sys import argv

def human_time(seconds):
    hours = seconds // 3600
    minutes = seconds // 60 % 60
    seconds = seconds % 60
    if hours > 0:
        return "{}h {}min {:.2f}s".format(hours, minutes, seconds)
    elif minutes > 0:
        return "{}min {:.2f}s".format(minutes, seconds)
    else:
        return "{:.2f}s".format(seconds)

def get_random_vertex(n_vertices):
    return choice(list(range(1, n_vertices + 1)))

def get_random_vertices(n_vertices, n):
    output = []
    for _ in range(n):
        output.append(get_random_vertex(n_vertices))
    return output

if len(argv) != 3:
    raise ValueError("Arguments must be graph filename and representation type (matrix or vectors)")

filename = argv[1]
repr_type = argv[2]

if repr_type not in ["matrix", "vectors"]:
    raise ValueError("Representation type must be matrix or vectors")

print(f"Graph {filename}, representation using {repr_type}")

if repr_type == "matrix":
    g = graphs.AdjacencyMatrixGraph(filename)
else:
    g = graphs.AdjacencyVectorsGraph(filename)

# Number of random vertices to select
k = 100
vertices = get_random_vertices(g.get_n_vertices(), k)
for vertex in [20, 30, 40, 50, 60]:
    print(f"--> d(10,{vertex}) = {g.get_distance(10, vertex)}")
    print(f"--> path(10, {vertex}) = {g.get_path(10, vertex)}")

# Measure the average time for the min-heap implementation
min_heap_times = []
for vertex in vertices:
    start = time()
    g.dijkstra(vertex, "")
    end = time()
    elapsed_time = end - start
    min_heap_times.append(elapsed_time)

min_heap_average_time = sum(min_heap_times) / k
print(f"--> Average time of Dijkstra (min-heap) computation: {human_time(min_heap_average_time)}")

# Measure the average time for the naive implementation
""" naive_times = []
for vertex in vertices:
    start = time()
    g.dijkstra_naive(vertex, "")
    end = time()
    elapsed_time = end - start
    naive_times.append(elapsed_time)

naive_average_time = sum(naive_times) / k """
""" print(f"--> Average time of Dijkstra (naive) computation: {human_time(naive_average_time)}") """
