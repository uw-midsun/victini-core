from geographiclib.geodesic import Geodesic
from pyproj import Geod
import math
import pandas as pd


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
    coordinate_point_index = [
        segment_points[i] if i in segment_points else None
        for i in range(len(all_coordinates))
    ]

    # 4. Return coordinate_point_index and interpolated_coordinates
    return coordinate_point_index, interpolated_coordinates


def split_lat_long(coordinates: list[tuple] = None):
    latitudes = []
    longitudes = []
    for c in enumerate(coordinates):
        latitudes.append(c[0])
        longitudes.append(c[1])

    return latitudes, longitudes
