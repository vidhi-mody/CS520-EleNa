import sys, os

sys.path.append('../')
from index import validate_params, get_route_details
from flask import Flask
import pytest
import index

import osmnx

from controller.routing import get_dijkstra_route, elevation_based_dijkstra
from model.gather_data import store_node_elevations

def test_validate_params_sucess():
    source = ['42.349056', '-72.528877']
    destination = ['42.3869382', '-72.52991477067445']
    percent = 150
    route_type = 'min'
    actual_output = validate_params(source, destination,  percent ,route_type)
    assert actual_output == (False, "No Error")

    source = ['42.349056']
    actual_output = validate_params(source, destination,  percent ,route_type)
    assert actual_output == (True, "Source not correct.")

    source = ['42.349056', '-72.528877']
    destination = ['42.3869382']
    actual_output = validate_params(source, destination,  percent ,route_type)
    assert actual_output == (True, "Destination not correct.")

    destination = ['42.3869382', '-72.52991477067445']
    percent = 250
    actual_output = validate_params(source, destination,  percent ,route_type)
    assert actual_output == (True, "Percent increase not between 100 and 200")

    percent = 150
    route_type = 'minimum'
    actual_output = validate_params(source, destination,  percent ,route_type)
    assert actual_output == (True, "Route type not between min or max")

def test_validate_params_fail():
    source = ['42.349056', '-72.528877']
    destination = ['42.3869382', '-72.52991477067445']
    percent = 150
    route_type = 'min'
    actual_output = validate_params(source, destination,  percent ,route_type)
    assert not actual_output == (True, "No Error")

    source = ['42.349056']
    actual_output = validate_params(source, destination,  percent ,route_type)
    assert not actual_output == (False, "Source not correct.")

    source = ['42.349056', '-72.528877']
    destination = ['42.3869382']
    actual_output = validate_params(source, destination,  percent ,route_type)
    assert not actual_output == (False, "Destination not correct.")

    destination = ['42.3869382', '-72.52991477067445']
    percent = 250
    actual_output = validate_params(source, destination,  percent ,route_type)
    assert not actual_output == (False, "Percent increase not between 100 and 200")

    percent = 150
    route_type = 'minimum'
    actual_output = validate_params(source, destination,  percent ,route_type)
    assert not actual_output == (False, "Route type not between min or max")



def test_get_route_details_sucess():
    source = ['42.349056', '-72.528877']
    destination = ['42.3869382', '-72.52991477067445']
    place = 'Amherst, Massachusetts'
    percent = 125
    route_type = 'max'

    temp = get_route_details(source, destination, place, percent, route_type)

    result = [{'y': 42.348773, 'x': -72.528881, 'street_count': 3, 'elevation': 54, 'dist_from_start': 0.0}, {'y': 42.349435, 'x': -72.52854, 'street_count': 3, 'elevation': 54, 'dist_from_start': 80.64699999999999}, {'y': 42.3496438, 'x': -72.5281623, 'street_count': 3, 'elevation': 54, 'dist_from_start': 119.66799999999999}, {'y': 42.3497246, 'x': -72.5279153, 'street_count': 3, 'elevation': 54, 'dist_from_start': 141.875}, {'y': 42.349854, 'x': -72.527639, 'street_count': 4, 'elevation': 54, 'dist_from_start': 168.949}, {'y': 42.35076, 'x': -72.527387, 'street_count': 4, 'elevation': 54, 'dist_from_start': 275.173}, {'y': 42.351494, 'x': -72.5273814, 'street_count': 4, 'elevation': 54, 'dist_from_start': 356.79200000000003}, {'y': 42.3515266, 'x': -72.52603, 'street_count': 3, 'elevation': 51, 'dist_from_start': 468.01200000000006}, {'y': 42.351536, 'x': -72.5258529, 'street_count': 4, 'elevation': 51, 'dist_from_start': 482.60300000000007}, {'y': 42.3515388, 'x': -72.5257925, 'street_count': 3, 'elevation': 51, 'dist_from_start': 487.5760000000001}, {'y': 42.3515681, 'x': -72.5257371, 'street_count': 3, 'elevation': 51, 'dist_from_start': 493.2240000000001}, {'y': 42.3516113, 'x': -72.5257443, 'street_count': 4, 'elevation': 51, 'dist_from_start': 498.0640000000001}, {'y': 42.351708, 'x': -72.525012, 'street_count': 3, 'elevation': 51, 'dist_from_start': 559.2110000000001}, {'y': 42.351839, 'x': -72.524353, 'street_count': 3, 'elevation': 51, 'dist_from_start': 615.3250000000002}, {'y': 42.3541171, 'x': -72.5221039, 'street_count': 4, 'elevation': 53, 'dist_from_start': 935.7540000000001}, {'y': 42.354221, 'x': -72.522022, 'street_count': 3, 'elevation': 53, 'dist_from_start': 949.1240000000001}, {'y': 42.3545731, 'x': -72.521744, 'street_count': 4, 'elevation': 53, 'dist_from_start': 994.4530000000001}, {'y': 42.3556561, 'x': -72.5210113, 'street_count': 4, 'elevation': 53, 'dist_from_start': 1134.983}, {'y': 42.3557675, 'x': -72.5210566, 'street_count': 3, 'elevation': 53, 'dist_from_start': 1148.161}, {'y': 42.3558147, 'x': -72.5210408, 'street_count': 3, 'elevation': 53, 'dist_from_start': 1153.646}, {'y': 42.3574905, 'x': -72.5210161, 'street_count': 4, 'elevation': 60, 'dist_from_start': 1340.3249999999998}, {'y': 42.3577576, 'x': -72.5210083, 'street_count': 4, 'elevation': 60, 'dist_from_start': 1370.032}, {'y': 42.3581485, 'x': -72.5209888, 'street_count': 4, 'elevation': 60, 'dist_from_start': 1413.528}, {'y': 42.3587168, 'x': -72.5209751, 'street_count': 4, 'elevation': 73, 'dist_from_start': 1476.731}, {'y': 42.3590687, 'x': -72.5209753, 'highway': 'crossing', 'street_count': 4, 'elevation': 73, 'dist_from_start': 1515.868}, {'y': 42.3595563, 'x': -72.5209708, 'highway': 'crossing', 'street_count': 4, 'elevation': 73, 'dist_from_start': 1570.0929999999998}, {'y': 42.3596156, 'x': -72.5209696, 'highway': 'crossing', 'street_count': 4, 'elevation': 73, 'dist_from_start': 1576.6879999999999}, {'y': 42.3601334, 'x': -72.520963, 'street_count': 4, 'elevation': 73, 'dist_from_start': 1634.2669999999998}, {'y': 42.3606794, 'x': -72.5209524, 'street_count': 4, 'elevation': 83, 'dist_from_start': 1694.9889999999998}, {'y': 42.3619662, 'x': -72.5208856, 'street_count': 4, 'elevation': 83, 'dist_from_start': 1838.1939999999997}, {'y': 42.36264, 'x': -72.520866, 'street_count': 3, 'elevation': 90, 'dist_from_start': 1913.1759999999997}, {'y': 42.3628323, 'x': -72.5209103, 'street_count': 4, 'elevation': 90, 'dist_from_start': 1935.3059999999998}, {'y': 42.3632934, 'x': -72.5208976, 'street_count': 4, 'elevation': 90, 'dist_from_start': 1986.5889999999997}, {'y': 42.3646983, 'x': -72.5207342, 'street_count': 4, 'elevation': 78, 'dist_from_start': 2143.3909999999996}, {'y': 42.3653703, 'x': -72.5206533, 'street_count': 4, 'elevation': 78, 'dist_from_start': 2218.4089999999997}, {'y': 42.365734, 'x': -72.520612, 'street_count': 4, 'elevation': 78, 'dist_from_start': 2258.9929999999995}, {'y': 42.367325, 'x': -72.520423, 'street_count': 4, 'elevation': 86, 'dist_from_start': 2436.5839999999994}, {'y': 42.3673798, 'x': -72.5204199, 'street_count': 3, 'elevation': 86, 'dist_from_start': 2442.6829999999995}, {'y': 42.368261, 'x': -72.5203196, 'street_count': 4, 'elevation': 86, 'dist_from_start': 2546.0009999999997}, {'y': 42.3682938, 'x': -72.5207866, 'street_count': 3, 'elevation': 86, 'dist_from_start': 2584.54}, {'y': 42.368434, 'x': -72.522787, 'highway': 'turning_circle', 'street_count': 5, 'elevation': 90, 'dist_from_start': 2749.62}, {'y': 42.369805, 'x': -72.523506, 'street_count': 3, 'elevation': 90, 'dist_from_start': 2913.114}, {'y': 42.37101, 'x': -72.524327, 'street_count': 3, 'elevation': 99, 'dist_from_start': 3063.552}, {'y': 42.3716005, 'x': -72.5231617, 'street_count': 3, 'elevation': 99, 'dist_from_start': 3179.636}, {'y': 42.3721915, 'x': -72.5232875, 'street_count': 3, 'elevation': 99, 'dist_from_start': 3246.16}, {'y': 42.3724717, 'x': -72.5233471, 'street_count': 3, 'elevation': 99, 'dist_from_start': 3277.699}, {'y': 42.3726797, 'x': -72.5233914, 'street_count': 3, 'elevation': 99, 'dist_from_start': 3301.112}, {'y': 42.3728659, 'x': -72.5234311, 'street_count': 3, 'elevation': 99, 'dist_from_start': 3322.072}, {'y': 42.373018, 'x': -72.5234635, 'street_count': 3, 'elevation': 98, 'dist_from_start': 3339.193}, {'y': 42.3736818, 'x': -72.5236048, 'street_count': 3, 'elevation': 98, 'dist_from_start': 3413.911}, {'y': 42.374218, 'x': -72.523719, 'street_count': 3, 'elevation': 98, 'dist_from_start': 3474.2670000000003}, {'y': 42.3747063, 'x': -72.5238232, 'street_count': 3, 'elevation': 98, 'dist_from_start': 3529.2340000000004}, {'y': 42.3754923, 'x': -72.5240061, 'street_count': 4, 'elevation': 100, 'dist_from_start': 3617.954}, {'y': 42.3756115, 'x': -72.5240445, 'highway': 'priority', 'street_count': 4, 'elevation': 100, 'dist_from_start': 3631.579}, {'y': 42.3757133, 'x': -72.5240821, 'street_count': 4, 'elevation': 100, 'dist_from_start': 3643.3120000000004}, {'y': 42.3770041, 'x': -72.5245234, 'street_count': 3, 'elevation': 100, 'dist_from_start': 3791.3940000000002}, {'y': 42.3772539, 'x': -72.5245971, 'street_count': 3, 'elevation': 100, 'dist_from_start': 3819.8230000000003}, {'y': 42.378361, 'x': -72.524935, 'street_count': 3, 'elevation': 100, 'dist_from_start': 3946.0170000000003}, {'y': 42.378797, 'x': -72.525064, 'street_count': 3, 'elevation': 88, 'dist_from_start': 3995.6420000000003}, {'y': 42.3797, 'x': -72.525331, 'street_count': 3, 'elevation': 91, 'dist_from_start': 4098.418000000001}, {'y': 42.380582, 'x': -72.525604, 'street_count': 3, 'elevation': 91, 'dist_from_start': 4199.023}, {'y': 42.381885, 'x': -72.525996, 'highway': 'stop', 'street_count': 4, 'elevation': 89, 'dist_from_start': 4347.444}, {'y': 42.3819395, 'x': -72.5260145, 'street_count': 4, 'elevation': 89, 'dist_from_start': 4353.692}, {'y': 42.383347, 'x': -72.526476, 'street_count': 3, 'elevation': 74, 'dist_from_start': 4514.727}, {'y': 42.383749, 'x': -72.52661, 'street_count': 3, 'elevation': 74, 'dist_from_start': 4560.763}, {'y': 42.3840081, 'x': -72.5267029, 'street_count': 4, 'elevation': 74, 'dist_from_start': 4590.568}, {'y': 42.3840772, 'x': -72.5267302, 'street_count': 4, 'elevation': 74, 'dist_from_start': 4598.572}, {'y': 42.3848588, 'x': -72.5270667, 'highway': 'crossing', 'street_count': 4, 'elevation': 74, 'dist_from_start': 4689.771}, {'y': 42.3849387, 'x': -72.527095, 'street_count': 4, 'elevation': 74, 'dist_from_start': 4698.955}, {'y': 42.3851632, 'x': -72.5271854, 'street_count': 4, 'elevation': 74, 'dist_from_start': 4725.0}, {'y': 42.3852478, 'x': -72.5272171, 'highway': 'crossing', 'street_count': 4, 'elevation': 74, 'dist_from_start': 4734.761}, {'y': 42.385564, 'x': -72.5273844, 'street_count': 4, 'elevation': 75, 'dist_from_start': 4772.8550000000005}, {'y': 42.3858522, 'x': -72.5275085, 'street_count': 4, 'elevation': 75, 'dist_from_start': 4806.485000000001}, {'y': 42.3861387, 'x': -72.5276419, 'street_count': 4, 'elevation': 75, 'dist_from_start': 4840.179000000001}, {'y': 42.386207, 'x': -72.5276688, 'street_count': 3, 'elevation': 75, 'dist_from_start': 4848.088000000001}, {'y': 42.386181, 'x': -72.5277209, 'street_count': 3, 'elevation': 75, 'dist_from_start': 4853.252}, {'y': 42.3860189, 'x': -72.5283609, 'street_count': 4, 'elevation': 75, 'dist_from_start': 4908.8240000000005}, {'y': 42.3858516, 'x': -72.5291043, 'street_count': 3, 'elevation': 75, 'dist_from_start': 4972.651000000001}, {'y': 42.3857955, 'x': -72.5294147, 'street_count': 4, 'elevation': 64, 'dist_from_start': 4998.897000000001}, {'y': 42.3858026, 'x': -72.5295766, 'street_count': 4, 'elevation': 64, 'dist_from_start': 5012.217000000001}, {'y': 42.3863936, 'x': -72.529962, 'street_count': 4, 'elevation': 64, 'dist_from_start': 5085.793000000001}, {'y': 42.3869153, 'x': -72.53016, 'street_count': 3, 'elevation': 64, 'dist_from_start': 5146.040000000001}]

    routedist = 5146.040000000001
    routeele = 122

    assert temp[0] == result and temp[1] == routedist and temp[2] == routeele


def test_get_route_details_fail():
    source = ['42.349056', '-72.528877']
    destination = ['42.3869382', '-72.52991477067445']
    place = 'Amherst, Massachusetts'
    percent = 125
    route_type = 'max'

    temp = get_route_details(source, destination, place, percent, route_type)

    result = [{'y': 42.348773, 'x': -72.528881, 'street_count': 3, 'elevation': 54, 'dist_from_start': 0.0}, {'y': 42.349435, 'x': -72.52854, 'street_count': 3, 'elevation': 54, 'dist_from_start': 80.64699999999999}, {'y': 42.3496438, 'x': -72.5281623, 'street_count': 3, 'elevation': 54, 'dist_from_start': 119.66799999999999}, {'y': 42.3497246, 'x': -72.5279153, 'street_count': 3, 'elevation': 54, 'dist_from_start': 141.875}, {'y': 42.349854, 'x': -72.527639, 'street_count': 4, 'elevation': 54, 'dist_from_start': 168.949}, {'y': 42.35076, 'x': -72.527387, 'street_count': 4, 'elevation': 54, 'dist_from_start': 275.173}, {'y': 42.351494, 'x': -72.5273814, 'street_count': 4, 'elevation': 54, 'dist_from_start': 356.79200000000003}, {'y': 42.3515266, 'x': -72.52603, 'street_count': 3, 'elevation': 51, 'dist_from_start': 468.01200000000006}, {'y': 42.351536, 'x': -72.5258529, 'street_count': 4, 'elevation': 51, 'dist_from_start': 482.60300000000007}, {'y': 42.3515388, 'x': -72.5257925, 'street_count': 3, 'elevation': 51, 'dist_from_start': 487.5760000000001}, {'y': 42.3515681, 'x': -72.5257371, 'street_count': 3, 'elevation': 51, 'dist_from_start': 493.2240000000001}, {'y': 42.3516113, 'x': -72.5257443, 'street_count': 4, 'elevation': 51, 'dist_from_start': 498.0640000000001}, {'y': 42.351708, 'x': -72.525012, 'street_count': 3, 'elevation': 51, 'dist_from_start': 559.2110000000001}, {'y': 42.351839, 'x': -72.524353, 'street_count': 3, 'elevation': 51, 'dist_from_start': 615.3250000000002}, {'y': 42.3541171, 'x': -72.5221039, 'street_count': 4, 'elevation': 53, 'dist_from_start': 935.7540000000001}, {'y': 42.354221, 'x': -72.522022, 'street_count': 3, 'elevation': 53, 'dist_from_start': 949.1240000000001}, {'y': 42.3545731, 'x': -72.521744, 'street_count': 4, 'elevation': 53, 'dist_from_start': 994.4530000000001}, {'y': 42.3556561, 'x': -72.5210113, 'street_count': 4, 'elevation': 53, 'dist_from_start': 1134.983}, {'y': 42.3557675, 'x': -72.5210566, 'street_count': 3, 'elevation': 53, 'dist_from_start': 1148.161}, {'y': 42.3558147, 'x': -72.5210408, 'street_count': 3, 'elevation': 53, 'dist_from_start': 1153.646}, {'y': 42.3574905, 'x': -72.5210161, 'street_count': 4, 'elevation': 60, 'dist_from_start': 1340.3249999999998}, {'y': 42.3577576, 'x': -72.5210083, 'street_count': 4, 'elevation': 60, 'dist_from_start': 1370.032}, {'y': 42.3581485, 'x': -72.5209888, 'street_count': 4, 'elevation': 60, 'dist_from_start': 1413.528}, {'y': 42.3587168, 'x': -72.5209751, 'street_count': 4, 'elevation': 73, 'dist_from_start': 1476.731}, {'y': 42.3590687, 'x': -72.5209753, 'highway': 'crossing', 'street_count': 4, 'elevation': 73, 'dist_from_start': 1515.868}, {'y': 42.3595563, 'x': -72.5209708, 'highway': 'crossing', 'street_count': 4, 'elevation': 73, 'dist_from_start': 1570.0929999999998}, {'y': 42.3596156, 'x': -72.5209696, 'highway': 'crossing', 'street_count': 4, 'elevation': 73, 'dist_from_start': 1576.6879999999999}, {'y': 42.3601334, 'x': -72.520963, 'street_count': 4, 'elevation': 73, 'dist_from_start': 1634.2669999999998}, {'y': 42.3606794, 'x': -72.5209524, 'street_count': 4, 'elevation': 83, 'dist_from_start': 1694.9889999999998}, {'y': 42.3619662, 'x': -72.5208856, 'street_count': 4, 'elevation': 83, 'dist_from_start': 1838.1939999999997}, {'y': 42.36264, 'x': -72.520866, 'street_count': 3, 'elevation': 90, 'dist_from_start': 1913.1759999999997}, {'y': 42.3628323, 'x': -72.5209103, 'street_count': 4, 'elevation': 90, 'dist_from_start': 1935.3059999999998}, {'y': 42.3632934, 'x': -72.5208976, 'street_count': 4, 'elevation': 90, 'dist_from_start': 1986.5889999999997}, {'y': 42.3646983, 'x': -72.5207342, 'street_count': 4, 'elevation': 78, 'dist_from_start': 2143.3909999999996}, {'y': 42.3653703, 'x': -72.5206533, 'street_count': 4, 'elevation': 78, 'dist_from_start': 2218.4089999999997}, {'y': 42.365734, 'x': -72.520612, 'street_count': 4, 'elevation': 78, 'dist_from_start': 2258.9929999999995}, {'y': 42.367325, 'x': -72.520423, 'street_count': 4, 'elevation': 86, 'dist_from_start': 2436.5839999999994}, {'y': 42.3673798, 'x': -72.5204199, 'street_count': 3, 'elevation': 86, 'dist_from_start': 2442.6829999999995}, {'y': 42.368261, 'x': -72.5203196, 'street_count': 4, 'elevation': 86, 'dist_from_start': 2546.0009999999997}, {'y': 42.3682938, 'x': -72.5207866, 'street_count': 3, 'elevation': 86, 'dist_from_start': 2584.54}, {'y': 42.368434, 'x': -72.522787, 'highway': 'turning_circle', 'street_count': 5, 'elevation': 90, 'dist_from_start': 2749.62}, {'y': 42.369805, 'x': -72.523506, 'street_count': 3, 'elevation': 90, 'dist_from_start': 2913.114}, {'y': 42.37101, 'x': -72.524327, 'street_count': 3, 'elevation': 99, 'dist_from_start': 3063.552}, {'y': 42.3716005, 'x': -72.5231617, 'street_count': 3, 'elevation': 99, 'dist_from_start': 3179.636}, {'y': 42.3721915, 'x': -72.5232875, 'street_count': 3, 'elevation': 99, 'dist_from_start': 3246.16}, {'y': 42.3724717, 'x': -72.5233471, 'street_count': 3, 'elevation': 99, 'dist_from_start': 3277.699}, {'y': 42.3726797, 'x': -72.5233914, 'street_count': 3, 'elevation': 99, 'dist_from_start': 3301.112}, {'y': 42.3728659, 'x': -72.5234311, 'street_count': 3, 'elevation': 99, 'dist_from_start': 3322.072}, {'y': 42.373018, 'x': -72.5234635, 'street_count': 3, 'elevation': 98, 'dist_from_start': 3339.193}, {'y': 42.3736818, 'x': -72.5236048, 'street_count': 3, 'elevation': 98, 'dist_from_start': 3413.911}, {'y': 42.374218, 'x': -72.523719, 'street_count': 3, 'elevation': 98, 'dist_from_start': 3474.2670000000003}, {'y': 42.3747063, 'x': -72.5238232, 'street_count': 3, 'elevation': 98, 'dist_from_start': 3529.2340000000004}, {'y': 42.3754923, 'x': -72.5240061, 'street_count': 4, 'elevation': 100, 'dist_from_start': 3617.954}, {'y': 42.3756115, 'x': -72.5240445, 'highway': 'priority', 'street_count': 4, 'elevation': 100, 'dist_from_start': 3631.579}, {'y': 42.3757133, 'x': -72.5240821, 'street_count': 4, 'elevation': 100, 'dist_from_start': 3643.3120000000004}, {'y': 42.3770041, 'x': -72.5245234, 'street_count': 3, 'elevation': 100, 'dist_from_start': 3791.3940000000002}, {'y': 42.3772539, 'x': -72.5245971, 'street_count': 3, 'elevation': 100, 'dist_from_start': 3819.8230000000003}, {'y': 42.378361, 'x': -72.524935, 'street_count': 3, 'elevation': 100, 'dist_from_start': 3946.0170000000003}, {'y': 42.378797, 'x': -72.525064, 'street_count': 3, 'elevation': 88, 'dist_from_start': 3995.6420000000003}, {'y': 42.3797, 'x': -72.525331, 'street_count': 3, 'elevation': 91, 'dist_from_start': 4098.418000000001}, {'y': 42.380582, 'x': -72.525604, 'street_count': 3, 'elevation': 91, 'dist_from_start': 4199.023}, {'y': 42.381885, 'x': -72.525996, 'highway': 'stop', 'street_count': 4, 'elevation': 89, 'dist_from_start': 4347.444}, {'y': 42.3819395, 'x': -72.5260145, 'street_count': 4, 'elevation': 89, 'dist_from_start': 4353.692}, {'y': 42.383347, 'x': -72.526476, 'street_count': 3, 'elevation': 74, 'dist_from_start': 4514.727}, {'y': 42.383749, 'x': -72.52661, 'street_count': 3, 'elevation': 74, 'dist_from_start': 4560.763}, {'y': 42.3840081, 'x': -72.5267029, 'street_count': 4, 'elevation': 74, 'dist_from_start': 4590.568}, {'y': 42.3840772, 'x': -72.5267302, 'street_count': 4, 'elevation': 74, 'dist_from_start': 4598.572}, {'y': 42.3848588, 'x': -72.5270667, 'highway': 'crossing', 'street_count': 4, 'elevation': 74, 'dist_from_start': 4689.771}, {'y': 42.3849387, 'x': -72.527095, 'street_count': 4, 'elevation': 74, 'dist_from_start': 4698.955}, {'y': 42.3851632, 'x': -72.5271854, 'street_count': 4, 'elevation': 74, 'dist_from_start': 4725.0}, {'y': 42.3852478, 'x': -72.5272171, 'highway': 'crossing', 'street_count': 4, 'elevation': 74, 'dist_from_start': 4734.761}, {'y': 42.385564, 'x': -72.5273844, 'street_count': 4, 'elevation': 75, 'dist_from_start': 4772.8550000000005}, {'y': 42.3858522, 'x': -72.5275085, 'street_count': 4, 'elevation': 75, 'dist_from_start': 4806.485000000001}, {'y': 42.3861387, 'x': -72.5276419, 'street_count': 4, 'elevation': 75, 'dist_from_start': 4840.179000000001}, {'y': 42.386207, 'x': -72.5276688, 'street_count': 3, 'elevation': 75, 'dist_from_start': 4848.088000000001}, {'y': 42.386181, 'x': -72.5277209, 'street_count': 3, 'elevation': 75, 'dist_from_start': 4853.252}, {'y': 42.3860189, 'x': -72.5283609, 'street_count': 4, 'elevation': 75, 'dist_from_start': 4908.8240000000005}, {'y': 42.3858516, 'x': -72.5291043, 'street_count': 3, 'elevation': 75, 'dist_from_start': 4972.651000000001}, {'y': 42.3857955, 'x': -72.5294147, 'street_count': 4, 'elevation': 64, 'dist_from_start': 4998.897000000001}, {'y': 42.3858026, 'x': -72.5295766, 'street_count': 4, 'elevation': 64, 'dist_from_start': 5012.217000000001}, {'y': 42.3863936, 'x': -72.529962, 'street_count': 4, 'elevation': 64, 'dist_from_start': 5085.793000000001}, {'y': 42.3869153, 'x': -72.53016, 'street_count': 3, 'elevation': 64, 'dist_from_start': 5146.040000000001}]

    routedist = 5146.040000000001
    routeele = 122

    routedist = 100.040000000001
    assert not (temp[0] == result and temp[1] == routedist and temp[2] == routeele)

    routeele = 100
    assert not (temp[0] == result and temp[1] == routedist and temp[2] == routeele)





def test_get_dijkstra_route_success():
    place = 'Amherst, Massachusetts'
    graph = osmnx.graph.graph_from_place(place)
    graph = store_node_elevations(graph)  
    start = 66699375
    end = 6382285969
    max_length = 6432.550000000001
    route_type="max"
    expected_get_path_len_no_elev = 5146.040000000001
    expected_get_path_len_elev = 122
    expected_path=[66699375, 66634686, 7058913914, 7058913916, 66656988, 66643538, 6655624009, 6655623989, 6655624004, 6655623992, 6655623986, 6655623985, 66641424, 66667006, 6655623965, 66723660, 6655623958, 6655623931, 6655623929, 6655623928, 6655623901, 6655623902, 7148671786, 7148671806, 6655623911, 9065016058, 9065016059, 6655623908, 6655623912, 6655623916, 6655623920, 2422592971, 8320860425, 8320860421, 2422592972, 66688974, 66665076, 1626574640, 1626574656, 8320806959, 66754369, 66606413, 66713794, 66636974, 7205221704, 9053984741, 7209734573, 7209734569, 7192403508, 7192403496, 66719843, 7271232747, 6304679898, 66634064, 6304679902, 7170986657, 9078520703, 66726263, 66680540, 66700205, 66653273, 66623005, 6353520436, 66652592, 66697053, 5850031599, 6353520424, 66641415, 66699101, 66610767, 1445170510, 1443766330, 6382267451, 1445169816, 1439025035, 1439024755, 1439024844, 1439024777, 6382285966, 1439024871, 6382285964, 6382285969]
    actual_path, actual_get_path_len_no_elev, actual_get_path_len_elev= get_dijkstra_route(graph,start, end, max_length,route_type)
    assert expected_path==actual_path
    assert expected_get_path_len_no_elev==actual_get_path_len_no_elev
    assert expected_get_path_len_elev==actual_get_path_len_elev
    


def test_get_dijkstra_route_fail():
    place = 'Amherst, Massachusetts'
    graph = osmnx.graph.graph_from_place(place)
    graph = store_node_elevations(graph)  
    start = 66699375
    end = 6382285969
    max_length = 6432.550000000001
    route_type="max"
    expected_get_path_len_no_elev = 7146.040000000001
    expected_get_path_len_elev = 222
    expected_path=[6669, 66634686, 7058913914, 7058913916, 66656988, 66643538, 6655624009, 6655623989, 6655624004, 6655623992, 6655623986, 6655623985, 66641424, 66667006, 6655623965, 66723660, 6655623958, 6655623931, 6655623929, 6655623928, 6655623901, 6655623902, 7148671786, 7148671806, 6655623911, 9065016058, 9065016059, 6655623908, 6655623912, 6655623916, 6655623920, 2422592971, 8320860425, 8320860421, 2422592972, 66688974, 66665076, 1626574640, 1626574656, 8320806959, 66754369, 66606413, 66713794, 66636974, 7205221704, 9053984741, 7209734573, 7209734569, 7192403508, 7192403496, 66719843, 7271232747, 6304679898, 66634064, 6304679902, 7170986657, 9078520703, 66726263, 66680540, 66700205, 66653273, 66623005, 6353520436, 66652592, 66697053, 5850031599, 6353520424, 66641415, 66699101, 66610767, 1445170510, 1443766330, 6382267451, 1445169816, 1439025035, 1439024755, 1439024844, 1439024777, 6382285966, 1439024871, 6382285964, 6382285969]
    actual_path, actual_get_path_len_no_elev, actual_get_path_len_elev= get_dijkstra_route(graph,start, end, max_length,route_type)
    assert not expected_path==actual_path
    assert not expected_get_path_len_no_elev==actual_get_path_len_no_elev
    assert not expected_get_path_len_elev==actual_get_path_len_elev
    expected_path=[1, 66634686, 7058913914, 7058913916, 66656988, 66643538, 6655624009, 6655623989, 6655624004, 6655623992, 6655623986, 6655623985, 66641424, 66667006, 6655623965, 66723660, 6655623958, 6655623931, 6655623929, 6655623928, 6655623901, 6655623902, 7148671786, 7148671806, 6655623911, 9065016058, 9065016059, 6655623908, 6655623912, 6655623916, 6655623920, 2422592971, 8320860425, 8320860421, 2422592972, 66688974, 66665076, 1626574640, 1626574656, 8320806959, 66754369, 66606413, 66713794, 66636974, 7205221704, 9053984741, 7209734573, 7209734569, 7192403508, 7192403496, 66719843, 7271232747, 6304679898, 66634064, 6304679902, 7170986657, 9078520703, 66726263, 66680540, 66700205, 66653273, 66623005, 6353520436, 66652592, 66697053, 5850031599, 6353520424, 66641415, 66699101, 66610767, 1445170510, 1443766330, 6382267451, 1445169816, 1439025035, 1439024755, 1439024844, 1439024777, 6382285966, 1439024871, 6382285964, 6382285969]
    assert not expected_path==actual_path

def test_elevation_based_dijkstra_sucess():
    place = 'Amherst, Massachusetts'
    graph = osmnx.graph.graph_from_place(place)
    graph = store_node_elevations(graph) 
    start= 66699375
    end=6382285969
    cutoff= 6432.550000000001
    max_bool=False
    actual_op=[66699375, 66634686, 7058913914, 7058913916, 66656988, 66643538, 6655624009, 6655624015, 6655624023, 66715436, 66612469, 66622346, 5261532874, 4594476697, 5261532880, 4591925874, 5261532936, 4591927789, 4591927791, 5261540294, 319882137, 7059454290, 7059418680, 319882189, 319882190, 1166105911, 8421267287, 1266301185, 1166105905, 66617893, 7245013711, 2532976319, 66696264, 8421217514, 66700325, 3053060430, 66672344, 66737704, 3053060429, 8512412980, 8512412962, 8512412968, 8512412985, 66715579, 8512412988, 8390480450, 3053047235, 66693064, 66615522, 3614944250, 3614944251, 3614944411, 319882523, 66642126, 319882540, 319882541, 66609703, 66632137, 1445169862, 6382285950, 1439024922, 1439024940, 1439024846, 6382285964, 6382285969]
    expected_op= elevation_based_dijkstra(graph, start, end, cutoff, max_bool)
    assert expected_op==actual_op

    actual_op=[1, 66634686, 7058913914, 7058913916, 66656988, 66643538, 6655624009, 6655624015, 6655624023, 66715436, 66612469, 66622346, 5261532874, 4594476697, 5261532880, 4591925874, 5261532936, 4591927789, 4591927791, 5261540294, 319882137, 7059454290, 7059418680, 319882189, 319882190, 1166105911, 8421267287, 1266301185, 1166105905, 66617893, 7245013711, 2532976319, 66696264, 8421217514, 66700325, 3053060430, 66672344, 66737704, 3053060429, 8512412980, 8512412962, 8512412968, 8512412985, 66715579, 8512412988, 8390480450, 3053047235, 66693064, 66615522, 3614944250, 3614944251, 3614944411, 319882523, 66642126, 319882540, 319882541, 66609703, 66632137, 1445169862, 6382285950, 1439024922, 1439024940, 1439024846, 6382285964, 6382285969]
    assert not expected_op==actual_op

def test_elevation_based_dijkstra_fail():
    place = 'Amherst, Massachusetts'
    graph = osmnx.graph.graph_from_place(place)
    graph = store_node_elevations(graph) 
    start= 66699375
    end=6382285969
    cutoff= 6432.550000000001
    max_bool=False
    actual_op=[66699375, 66634686, 7058913914, 7058913916, 66656988, 66643538, 6655624009, 6655624015, 6655624023, 66715436, 66612469, 66622346, 5261532874, 4594476697, 5261532880, 4591925874, 5261532936, 4591927789, 4591927791, 5261540294, 319882137, 7059454290, 7059418680, 319882189, 319882190, 1166105911, 8421267287, 1266301185, 1166105905, 66617893, 7245013711, 2532976319, 66696264, 8421217514, 66700325, 3053060430, 66672344, 66737704, 3053060429, 8512412980, 8512412962, 8512412968, 8512412985, 66715579, 8512412988, 8390480450, 3053047235, 66693064, 66615522, 3614944250, 3614944251, 3614944411, 319882523, 66642126, 319882540, 319882541, 66609703, 66632137, 1445169862, 6382285950, 1439024922, 1439024940, 1439024846, 6382285964, 6382285969]
    expected_op= elevation_based_dijkstra(graph, start, end, cutoff, max_bool)

    actual_op=[1, 66634686, 7058913914, 7058913916, 66656988, 66643538, 6655624009, 6655624015, 6655624023, 66715436, 66612469, 66622346, 5261532874, 4594476697, 5261532880, 4591925874, 5261532936, 4591927789, 4591927791, 5261540294, 319882137, 7059454290, 7059418680, 319882189, 319882190, 1166105911, 8421267287, 1266301185, 1166105905, 66617893, 7245013711, 2532976319, 66696264, 8421217514, 66700325, 3053060430, 66672344, 66737704, 3053060429, 8512412980, 8512412962, 8512412968, 8512412985, 66715579, 8512412988, 8390480450, 3053047235, 66693064, 66615522, 3614944250, 3614944251, 3614944411, 319882523, 66642126, 319882540, 319882541, 66609703, 66632137, 1445169862, 6382285950, 1439024922, 1439024940, 1439024846, 6382285964, 6382285969]
    assert not expected_op==actual_op
