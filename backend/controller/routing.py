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














        """
        Returns the route(list of nodes) that minimize change in elevation between start and end using the A* node, with the heuristic 
        being the distance from the end node. 
        Params:
            start_location: tuple (lat,long)
            end_location: tuple (lat,long)
         Returns:
            lat_longs: List of [lon,lat] in the route
        """
        if not self.init:
            # bbox=self.get_bounding_box(start_location,end_location)
            # self.G = ox.graph_from_bbox(bbox[0],bbox[1],bbox[2],bbox[3],network_type='walk', simplify=False)
            self.G = ox.graph_from_point(start_location, distance=10000, simplify = False, network_type='walk')
            p.dump( self.G, open( "graph.p", "wb" ) )
            self.init = True
            print("Saved Graph")
        
        G = self.G
        
        #Graph initialization
        bbox=self.get_bounding_box(start_location,end_location)
        G=self.get_graph_with_elevation(bbox)
        G=self.add_dist_from_dest(G,end_location)
        #Initialization of pre-reqs
        start_node=ox.get_nearest_node(G, point=start_location)
        end_node=ox.get_nearest_node(G, point=end_location)


        shortest_route = nx.shortest_path(G, source=start_node, target=end_node, weight='length')
        shortest_dist = sum(ox.get_route_edge_attributes(G, shortest_route, 'length'))


        def reconstruct_path(cameFrom, current):
            """
            Function to retrace the path from end node to start node. Returns in the format required by Mapbox API(for plotting)
            """
            total_path = [current]
            while current in cameFrom:
                current = cameFrom[current]
                total_path.append(current)
            ele_latlong=[[G.node[route_node]['x'],G.node[route_node]['y']] for route_node in total_path ] 
            shortest_latlong=[[G.node[route_node]['x'],G.node[route_node]['y']] for route_node in shortest_route ] 
            return (ele_latlong,shortest_latlong)        
        
        #The settotal_path of nodes already evaluated
        closedSet=set()
        # The set of currently discovered nodes that are not evaluated yet.
        # Initially, only the start node is known.        
        openSet=set()
        openSet.add(start_node)
        # For each node, which node it can most efficiently be reached from.
        # If a node can be reached from many nodes, cameFrom will eventually contain the
        # most efficient previous step.
        cameFrom={}
        #For each node, the cost of getting from the start node to that node.
        gScore={}
        for node in G.nodes():
            gScore[node]=float("inf")
        #The cost of going from start to start is zero.
        gScore[start_node] =0 
        # For each node, the total cost of getting from the start node to the goal
        # by passing by that node. That value is partly known, partly heuristic.
        fScore={}

        # For the first node, that value is completely heuristic.
        fScore[start_node] = 0#G.nodes[start_node]['dist_from_dest']

        

        while openSet!={}:
            current= min([(node,fScore[node]) for node in openSet],key=lambda t: t[1]) [0]            
            if current==end_node:
                return reconstruct_path(cameFrom, current)
            openSet.remove(current)
            closedSet.add(current)

            for neighbor in G.neighbors(current):
                if neighbor in closedSet:
                    continue # Ignore the neighbor which is already evaluated.
                #The distance from start to a neighbor
                tentative_gScore= gScore[current]+1/abs(G.nodes[current]['elevation'] - G.nodes[neighbor]['elevation'])
                if neighbor not in openSet:# Discover a new node
                    openSet.add(neighbor)
                else:
                    if tentative_gScore>=gScore[neighbor] :#Stop searching along this path if distance exceed 1.5 times shortest path
                        continue# This is not a better path.
                cameFrom[neighbor]=current
                gScore[neighbor]=tentative_gScore
                fScore[neighbor]=gScore[neighbor]# + G.nodes[neighbor]['dist_from_dest']

