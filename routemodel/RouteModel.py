import utils


class RouteModel:
    def __init__(
        self, polyline_coordinates: list[tuple] = None, interval_upper_bound: int = None
    ):
        self.coordinates = utils.interpolate_coordinates(
            polyline_coordinates, interval_upper_bound
        )

        self.latitudes, self.longitudes = utils.split_lat_long(self.coordinates)
