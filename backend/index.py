'''
This is the connecting point with the front-end. This file routes further routes to calculte optimal path with given elevation and percent increase in distance.
'''
from http.client import NETWORK_AUTHENTICATION_REQUIRED
from flask import Flask
from flask_cors import CORS
import osmnx
import networkx
from networkx import single_source_dijkstra
from controller.routing import get_dijkstra_route, get_a_star
from model.gather_data import store_node_elevations 
from flask import request
from flask import jsonify
import pickle as p
import numpy as np

app = Flask(__name__)
CORS(app)

"""
This is the start point of the application. Parsing of data and calling the appropriate routing algorithm is done in this file.
"""


@app.route('/route', methods=['POST'])
def get_route():
    try:
        request_info = request.json
        source, destination, place, percent, route_type = request_info['start'], request_info['end'], request_info['place'], request_info['percent'], request_info['type']
    except:
        return "Some of the required parameters not present: source, destination, place, percent and route_elevation"

    param_has_error, error_message = validate_params(source, destination, percent ,route_type)

    if param_has_error:
        return error_message

    result = get_route_details(source, destination, place, percent, route_type)
    result = jsonify(result)
    return result


'''
Function to validate the parameters received: Source, destination, place, percent, min/max type
'''
def validate_params(source, destination, percent ,route_type):
    if len(source)!=2:
        return (True, "Source not correct.")

    if len(destination)!=2:
        return (True, "Destination not correct.")

    if percent<100 or percent>200:
        return (True, "Percent increase not between 100 and 200")
    
    if route_type not in ('min','max'):
        return (True, "Route type not between min or max")

    return (False, "No Error")




'''
Function to return the route that can be taken, in addition to the distance to be covered and total elevation in that route. Algorithms used for route detection are dijkstra and A star.
'''


def get_route_details(source, destination, place, percent, route_type):
    source_latitude = float(source[0])
    source_longitude = float(source[1])
    destination_latitude = float(destination[0])
    destination_longitude =  float(destination[1])

    distance = osmnx.distance.euclidean_dist_vec(destination_latitude, source_latitude,source_longitude, destination_longitude)
    
    if distance>15000:
        return ("Unable to compute the distance, Please insert nearby points")

    graph = osmnx.graph.graph_from_place(place)
    graph_with_elevations = store_node_elevations(graph)
    source_node = osmnx.nearest_nodes(graph_with_elevations, X=source_longitude, Y=source_latitude)
    destination_node = osmnx.nearest_nodes(graph_with_elevations, X=destination_longitude, Y=destination_latitude)
    dijkstra_distance = single_source_dijkstra(graph_with_elevations, source_node, destination_node, weight='length')
    path_nodes = get_a_star(graph_with_elevations, source_node, destination_node, dijkstra_distance[0] * percent/100, route_type)
    path_nodes, path_distance, path_elevation = get_dijkstra_route(graph_with_elevations, source_node, destination_node, dijkstra_distance[0] * percent/100, route_type)

    graph_nodes = graph_with_elevations.nodes()
    node_distances = [0.0]
    for i in range(len(path_nodes) - 1):
        node_distances.append(graph_with_elevations[path_nodes[i]][path_nodes[i+1]][0]['length'])

    result = []

    for entry in path_nodes:
        result.append(graph_nodes[entry])

    for i in range(len(result)):
        if i>1:
            result[i]['dist_uptill_now'] = result[i-1]['dist_uptill_now']+node_distances[i]
        else:
            result[i]['dist_from_start'] = node_distances[i]
    return result, path_distance, path_elevation



'''
Running on port 8080
'''


if __name__ == "__main__":
    app.run(port=8080)
    
    
 
