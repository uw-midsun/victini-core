import utils
import pandas as pd


class RouteModel:
    def __init__(
        self, polyline_coordinates: list[tuple] = None, interval_upper_bound: int = None
    ):
        self.polyline_point_index, self.coordinates = utils.interpolate_coordinates(
            polyline_coordinates, interval_upper_bound
        )
        self.latitudes, self.longitudes = utils.split_lat_long(self.coordinates)
        (
            self.elapsed_dist,
            self.dist_to_next_coordinate,
            self.true_bearing_to_next,
        ) = utils.coordinate_distances_bearings(self.coordinates)
        self.travel_direction = utils.travel_direction(self.true_bearing_to_next)

    def generate_dataframe(self):
        data = pd.DataFrame(
            {
                "polyline_point_index": self.polyline_point_index,
                "coordinates": self.coordinates,
                "latitude": self.latitudes,
                "longitude": self.longitudes,
                "elapsed_dist_meters": self.elapsed_dist,
                "dist_to_next_coordinate_meters": self.dist_to_next_coordinate,
                "true_bearing_to_next_coordinate": self.true_bearing_to_next,
                "travel_direction": self.travel_direction,
                # "turn_bearing": turn_bearings,
                # "turn_type": turn_type,
                # "relative_turn_angle": relative_turn_angle,
            }
        )
        return data

    def show(self):
        data = self.generate_dataframe()
        print(data)

    def save_csv(self, filename="routedata"):
        data = self.generate_dataframe()
        data = data.fillna("")
        format_filename = f"{filename}.csv" if ".csv" not in filename else filename
        data.to_csv(format_filename)
