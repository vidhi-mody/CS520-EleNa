from heapq import heappop
import collections
from heapq import heappush
from networkx import single_source_dijkstra
"""
This file returns the optimal path according to Dijikstra or Astar .
These algorithms considers elevation as well as distance in percentage to consider while navigation
"""



"""
Modified Dijikstra algorithm accorging to elevation gain and distance
"""

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



"""
Modified elevation_based_dijkstra algorithm accorging to elevation gain and distance
"""
def elevation_based_dijkstra(graph, start, end, max_distance, route_type):

        elevations = collections.defaultdict(int) #elevation dictionary
        distances = collections.defaultdict(int)  #distance dictionary
        G = graph
        Graph_sucessor = G._succ
        
        previous_node = {}
        max_distance = max_distance
        nodes_to_visit = [] 
        visited_elevation = {} 
        visited_elevation[start] = 0 
        first_node=(0, 0, start)
        heappush(nodes_to_visit, first_node)
 
        while len(nodes_to_visit)>0:
            temp_node=heappop(nodes_to_visit)
            elevation, distance, curr_node = temp_node
            if curr_node in elevations:
                continue
            if curr_node == end:
                break

            elevations[curr_node] = elevation
            distances[curr_node] = distance
            neighbors = Graph_sucessor[curr_node].items()
            for next_node, next_elevation in neighbors:
                next_dist = next_elevation[0]['length']
                next_elevation = abs(G.nodes()[curr_node]['elevation'] - G.nodes()[next_node] ['elevation'])
                new_distance , new_elevation = distances[curr_node] + next_dist , elevations[curr_node] + next_elevation
                if new_distance > max_distance:
                    continue

                if next_node not in visited_elevation or new_elevation<visited_elevation[next_node]:
                    visited_elevation[next_node] = new_elevation    
                    if route_type:
                        new_elevation *= -1
                    heappush(nodes_to_visit, [new_elevation, new_distance, next_node])
                    previous_node[next_node] = curr_node
        final_path = []
        current_node = end
        final_path.append(current_node)
        while current_node != start:
            current_node = previous_node[current_node]
            final_path.append(current_node)
        final_final_path=final_path[::-1]
        return list(final_final_path)
"""
Modified Astar  algorithm accorging to elevation gain and distance
"""
def get_a_star(graph, start, end, max_distance, route_type):
        elevations = collections.defaultdict(int)
        distances = collections.defaultdict(int) 
        G = graph
        Graph_sucessor = G._succ
        fScore={}
        previous_node = {}
        max_distance = max_distance
        nodes_to_visit = [] 
        visited_elevation = {} 
        visited_elevation[start] = 0 
        first_node=(0, 0, start)
        heappush(nodes_to_visit, first_node)
        GraphScore={}
        for node in G.nodes():
            GraphScore[node]=float("inf")
        GraphScore[start] = 0 
        while len(nodes_to_visit)>0:
            
            temp_node=heappop(nodes_to_visit)
            elevation, distance, curr_node = temp_node
            if curr_node in elevations:
                continue
            if curr_node == end:
                break
            nodes_to_visit = []
            elevations[curr_node] = elevation
            distances[curr_node] = distance
            neighbors = Graph_sucessor[curr_node].items()
            for next_node, next_elevation in neighbors:
                next_dist = next_elevation[0]['length']
                next_elevation = abs(G.nodes()[curr_node]['elevation'] - G.nodes()[next_node] ['elevation'])
                new_distance , new_elevation = distances[curr_node] + next_dist , elevations[curr_node] + next_elevation
                if new_distance > max_distance:
                    continue

                if next_node not in visited_elevation or new_elevation<visited_elevation[next_node]:
                    visited_elevation[next_node] = new_elevation    
                    if route_type:
                        new_elevation *= -1
                    heappush(nodes_to_visit, [new_elevation, new_distance, next_node])
                    previous_node[next_node] = curr_node

                if next_node in visited_elevation:
                    continue 
                alternat_graph_Score=0
                if next_node not in visited_elevation:
                    visited_elevation.add(next_node)
                else:
                    if alternat_graph_Score>=GraphScore[next_node] :
                        continue
                
        final_path = []
        current_node = end
        final_path.append(current_node)
        source_to_destination =final_path[::-1]
        source_to_destination = list(source_to_destination)
        return source_to_destination

