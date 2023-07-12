import utils
import pandas as pd


class RouteModel:
    BING_MAPS_API_KEY = ""

    def __init__(
        self,
        polyline_coordinates: list[tuple] = None,
        interval_upper_bound: int = None,
        BING_MAPS_API_KEY="",
    ):
        # Set Bing Maps API Key
        RouteModel.BING_MAPS_API_KEY = BING_MAPS_API_KEY
        # Get polyline indecies and inperpolated coordinates
        self.polyline_point_index, self.coordinates = utils.interpolate_coordinates(
            polyline_coordinates, interval_upper_bound
        )
        # Get latitudes and longitudes
        self.latitudes, self.longitudes = utils.split_lat_long(self.coordinates)
        # Get elapsed distance, distance between adjacent coordinates, true bearing to next coordinate
        (
            self.elapsed_dist,
            self.dist_to_next_coordinate,
            self.true_bearing_to_next,
        ) = utils.coordinate_distances_bearings(self.coordinates)
        # Get travel direction (relative to earth)
        self.travel_direction = utils.travel_direction(self.true_bearing_to_next)
        # Get elevations and elevation gain between coordinates
        self.elevations, self.relative_elevation_gains = utils.elevations_bing(
            self.coordinates, BING_MAPS_API_KEY
        )

    def generate_dataframe(self):
        data = pd.DataFrame(
            {
                "id": [i for i in range(len(self.coordinates))],
                "polyline_point_index": self.polyline_point_index,
                "coordinates": self.coordinates,
                "latitude": self.latitudes,
                "longitude": self.longitudes,
                "elevation_meters": self.elevations,
                "elevation_gains_to_next_meters": self.relative_elevation_gains,
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

    def location_service_csv(self):
        data = pd.DataFrame(
            {
                "id": [i for i in range(len(self.coordinates))],
                "coordinates": self.coordinates,
                "latitude": self.latitudes,
                "longitude": self.longitudes,
            }
        ).fillna("")
        data.to_csv("location_service.csv")
