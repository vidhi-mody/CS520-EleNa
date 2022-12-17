import json
import requests, networkx
from collections import OrderedDict


"""
This function models the graph with the elevation of the points from the open-elevation api
"""

def store_node_elevations(g):
    nodes = OrderedDict(g.nodes(data=True))
    node_points = [{'latitude': nodes[key]['y'], 'longitude': nodes[key]['x']} for key in OrderedDict(g.nodes(data=True))]
    
    results = []
    for i in range(0, len(node_points), 1000):
        chunk = node_points[i: i + 1000]
        locations = {'locations': chunk}
        result_locations = requests.post(
                url="https://api.open-elevation.com/api/v1/lookup",
                headers={
                    "Accept": "application/json",
                    "Content-Type": "application/json; charset=utf-8",
                },
                data=json.dumps(locations)
            )
        result_locations = result_locations.json()['results']
        results.extend(result_locations)
    
    elevation_dict = {}
    i = 0
    items = list(nodes.items())
    while i<len(items):
        key = items[i][0]
        elevation_dict[key] = results[i]['elevation']
        i += 1
    networkx.set_node_attributes(g, elevation_dict, name='elevation')
    return g


