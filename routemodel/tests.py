import pytest 

from utils import interpolate_coordinates, split_lat_long, coordinate_distances_bearings, travel_direction, relative_turn_angles, elevations_bing

# coordinates from sample_data.csv
polyline_coordinates = [
    (40.8829378816515, -98.37406855532743), 
    (40.88303262290332, -98.37402201117517), 
    (40.882977131913115, -98.37374990667321),
    (40.882921640280436, -98.37347780262579),
    (40.882935175051365,-98.37321643936254)
]

# for split lat long
for coordinate in polyline_coordinates:
    latitude = coordinate[0]
    longitude = coordinate[1]

# def test_interpolate_coordinates():

def test_split_lat_long():
    function_latitudes, function_longitudes = split_lat_long(polyline_coordinates)
    assert(latitude == function_latitudes)
    assert(longitude == function_longitudes)

def test_coordinate_distances_bearings():
        assert(travel_direction(None) == "coordinates cannot be None")

# def test_travel_directions():

def test_relative_turn_angles():
    calculated_angles = [0.4472809337216388, 0.4439371077197538, 0.445318475291096]
    function_angles = relative_turn_angles(polyline_coordinates)
    assert(calculated_angles == pytest.approx(function_angles))