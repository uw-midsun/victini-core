import json
import math

import pandas as pd
import requests
from geographiclib.geodesic import Geodesic
from pyproj import Geod


def interpolate_coordinates(
    polyline_coordinates: list[tuple] = None, interval_upper_bound: int = None
):
    # 1. Check params
    if polyline_coordinates is None or interval_upper_bound is None:
        raise TypeError("coordinates and interval_upper_bound cannot be None")
    if len(polyline_coordinates) < 3:
        raise TypeError("coordinates param must have at least 3 coordinates")

    # 2. Interpolate each segment into multiple coordinates
    segment_cooridnates = []
    for i, _ in enumerate(polyline_coordinates[1:], start=1):
        lat_1, long_1 = polyline_coordinates[i - 1]
        lat_2, long_2 = polyline_coordinates[i]
        # https://geographiclib.sourceforge.io/1.52/python/interface.html
        geo_data = Geodesic.WGS84.Inverse(lat_1, long_1, lat_2, long_2)
        dist = geo_data["s12"]
        intervals_num = math.ceil(dist / interval_upper_bound) - 1
        if intervals_num == 0:
            segment_cooridnates.append([(lat_1, long_1), (lat_2, long_2)])
        else:
            g = Geod(ellps="WGS84")
            # be careful here because the lat and longs order is switched
            longlats = g.npts(long_1, lat_1, long_2, lat_2, intervals_num)
            data = (
                [(lat_1, long_1)]
                + [(lat, long) for long, lat in longlats]
                + [(lat_2, long_2)]
            )
            segment_cooridnates.append(data)

    # 3. Formats segment_cooridnates into a long list of coordinates and indecies
    segment_points = {0: 0}  # {point, index}
    all_coordinates = segment_cooridnates[0].copy()
    interpolated_coordinates = []
    for i, segment_coordinate in enumerate(segment_cooridnates[1:], start=1):
        segment_points[len(all_coordinates) - 1] = i
        all_coordinates += segment_coordinate[1:]
    segment_points[len(all_coordinates) - 1] = len(segment_cooridnates)
    for _, coordinate in enumerate(all_coordinates):
        interpolated_coordinates.append((coordinate[0], coordinate[1]))
    polyline_point_index = [
        segment_points[i] if i in segment_points else None
        for i in range(len(all_coordinates))
    ]

    # 4. Return coordinate_point_index and interpolated_coordinates
    return polyline_point_index, interpolated_coordinates


def split_lat_long(coordinates: list[tuple] = None):
    if coordinates is None:
        raise TypeError("coordinates cannot be None")

    latitudes = []
    longitudes = []
    for c in coordinates:
        latitudes.append(c[0])
        longitudes.append(c[1])

    return latitudes, longitudes


def coordinate_distances_bearings(coordinates: list[tuple] = None):
    if coordinates is None:
        raise TypeError("coordinates cannot be None")

    elapsed_dist = [0]
    dist_to_next_coordinate = []
    true_bearing_to_next = []
    for i, _ in enumerate(coordinates[:-1]):
        lat_1, long_1 = coordinates[i]
        lat_2, long_2 = coordinates[i + 1]
        geo_data = Geodesic.WGS84.Inverse(
            lat_1, long_1, lat_2, long_2
        )  # return values: https://geographiclib.sourceforge.io/1.52/python/interface.html
        dist_to_next_coordinate.append(geo_data["s12"])  # dist between coordinates
        elapsed_dist.append(elapsed_dist[-1] + geo_data["s12"])  # trip dist so far
        true_bearing_to_next.append(geo_data["azi1"])  # bearing to next
    dist_to_next_coordinate.append(None)
    true_bearing_to_next.append(None)

    return elapsed_dist, dist_to_next_coordinate, true_bearing_to_next


def travel_direction(bearings: list = None):
    if bearings is None:
        raise TypeError("bearings cannot be None")

    general_travel_direction = []
    for bearing in bearings:
        if bearing is None:
            general_travel_direction.append(None)
        elif bearing == 0 or bearing == 360:
            general_travel_direction.append("N")
        elif bearing == 90:
            general_travel_direction.append("E")
        elif bearing == 180 or bearing == -180:
            general_travel_direction.append("S")
        elif bearing == -90:
            general_travel_direction.append("W")
        elif 0 < bearing < 90:
            general_travel_direction.append(f"N{bearing:.0f}{chr(176)}E")
        elif 90 < bearing < 180:
            general_travel_direction.append(f"S{bearing-90:.0f}{chr(176)}E")
        elif -90 < bearing < 0:
            general_travel_direction.append(f"N{abs(bearing):.0f}{chr(176)}W")
        elif -180 < bearing < -90:
            general_travel_direction.append(f"S{bearing+180:.0f}{chr(176)}W")

    return general_travel_direction


def turn_angles(coordinates: list[tuple] = None):
    ...


def elevations_bing(coordinates: list = None, BING_MAPS_API_KEY: str = ""):
    if coordinates is None:
        raise TypeError("coordinates cannot be None")
    if BING_MAPS_API_KEY == "":
        raise TypeError("BING_MAPS_API_KEY cannot be an empty string")

    # 1) "Chunk" coordinates into lists of length 10000. Change list_len if there's an API size issue
    # 2) Compresses each coordinate chunk into 1 compressed query string for Bing Maps API
    # - https://learn.microsoft.com/en-us/bingmaps/rest-services/elevations/point-compression-algorithm
    # - Requires: coordinates
    # - Result: compressed_coordinates_lst
    list_len = 1000  # Change list_len if there's an API size issue
    split_coordinates = [
        coordinates[i : min(i + list_len, len(coordinates))]
        for i in range(0, len(coordinates), list_len)
    ]
    compressed_coordinates_lst = []

    for coordinate_lst in split_coordinates:
        latitude = 0
        longitude = 0
        compressed_coordinates = ""

        for coordinate in coordinate_lst:
            newLatitude = round(coordinate[0] * 100000)
            newLongitude = round(coordinate[1] * 100000)

            dy = newLatitude - latitude
            dx = newLongitude - longitude
            latitude = newLatitude
            longitude = newLongitude

            dy = (dy << 1) ^ (dy >> 31)
            dx = (dx << 1) ^ (dx >> 31)

            index = int(((dy + dx) * (dy + dx + 1) / 2) + dy)
            while index > 0:
                rem = index & 31
                index = int((index - rem) / 32)
                if index > 0:
                    rem += 32
                compressed_coordinates += (
                    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_-"[
                        rem
                    ]
                )

        compressed_coordinates_lst.append(compressed_coordinates)

    # 3) Requests the elevation for all the coordinates using our compressed coordinate query string and saves it into a list
    # - Requires: compressed_coordinates_lst
    # - Result: coordinates_elevations_data
    coordinates_elevations_data = []
    for compressed_coordinates in compressed_coordinates_lst:
        API_query_string = f"http://dev.virtualearth.net/REST/v1/Elevation/List?points={compressed_coordinates}&heights=ellipsoid&key={BING_MAPS_API_KEY}"
        response = requests.post(API_query_string).json()

        if response["statusCode"] != 200:
            print("\n-> API Response\n", json.dumps(response, indent=2), "\n")
            raise ValueError(
                f"Bing Maps API request error {response['statusCode']}: {response['statusDescription']}"
            )

        elevations_data = response["resourceSets"][0]["resources"][0]["elevations"]
        coordinates_elevations_data.extend(elevations_data)

    # 4) Calculates the elevation change between the i and i+1 elevation in a list of elevations
    # - Requires: coordinates_elevations_data
    # - Result: relative_elevation_gains
    relative_elevation_gains = []
    relative_elevation_climb = []
    for i, _ in enumerate(coordinates_elevations_data[:-1]):
        elevation1 = coordinates_elevations_data[i]
        elevation2 = coordinates_elevations_data[i + 1]
        relative_elevation_gains.append(elevation2 - elevation1)
    relative_elevation_gains.append(None)
    relative_elevation_climb.append(None)

    return coordinates_elevations_data, relative_elevation_gains
