from heapq import heappop
import collections
from heapq import heappush
from networkx import single_source_dijkstra

def get_dijkstra_route(graph, source, destination, max_distance, route_type):
    if route_type == 'min':
        max_flag = False
    else:
        max_flag = True
    try:
        path = elevation_based_dijkstra(graph, source, destination, max_distance, max_flag)
    except Exception as e:
        print(e.__cause__)
        path = single_source_dijkstra(graph, source, destination, weight='length')[1]

    elevation = 0 
    for i in range(len(path) - 1):
        elevation += abs(graph.nodes()[path[i+1]]['elevation'] - graph.nodes()[path[i]] ['elevation'])

    distance = 0
    for i in range(len(path) - 1):
        distance += graph[path[i]][path[i+1]][0]['length']
    return path, distance, elevation

def elevation_based_dijkstra(graph, start, end, max_distance, max_bool):
    pass
    
