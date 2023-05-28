from RouteModel import RouteModel

polyline_coordinates = [
    (43.467879339595996, -80.56616840836313),
    (43.47883157462026, -80.53538493288134),
    (43.473830662244815, -80.53170344584917),
    (43.471525236984746, -80.53744468397863),
    (43.4644417537584, -80.54157837541729),
    (43.46348360838345, -80.53993555488016),
    (43.46266401802443, -80.53908339764159),
]
interval_upper_bound = 25

if __name__ == "__main__":
    route = RouteModel(
        polyline_coordinates=polyline_coordinates,
        interval_upper_bound=interval_upper_bound,
    )
    route.show()
    route.save_csv()
