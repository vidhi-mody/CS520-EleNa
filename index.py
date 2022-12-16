'''
This is the connecting point with the front-end. This file routes further routes to calculte optimal path with given elevation and percent increase in distance.
'''
import json
from sqlite3 import paramstyle
from flask import Flask
from flask import request
from flask import jsonify
from flask_cors import CORS
import osmnx
from networkx import single_source_dijkstra
from controller.routing import get_dijkstra_route
from model.gather_data import store_node_elevations 

app = Flask(__name__)
CORS(app)

@app.route('/route', methods=['POST'])
def routing():
    try:
        data = request.json
        source, destination, place, percent, route_type = data['start'], data['end'], data['place'], data['percent'], data['type']
    except:
        return "Some of the required parameters not present: source, destination, place, percent and route_elevation"
    param_has_error, error_message = validate_params(source, destination, place, percent ,route_type)
    if param_has_error:
        return error_message

    result = my_function(source, destination, place, percent, route_type)
    return jsonify(result)

def validate_params(source, destination, place, percent ,route_type):
    if len(source)!=2:
        return (True, "Source not correct.")

    if len(destination)!=2:
        return (True, "Destination not correct.")

    if percent<100 or percent>200:
        return (True, "Percent increase not between 100 and 200")
    
    if route_type not in ('min','max'):
        return (True, "Route type not between min or max")

    return (False, "No Error")
