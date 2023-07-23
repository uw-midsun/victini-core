# Location Service

This service acts as an entrypoint for the car to the microservices. The car will send it's coordinates and this service will map the car's coordinates to the routemodel coordinates. Then this service will send a request containing the car's raw data and routemodel coordinates to the historical car/MongoDB service.

**TODO: API request from location service to historical car/MongoDB service**

## Docker Commands

### Build image

Make sure you have docker daemon running and add your `DATABASE_URI` string as an environment variable in the Dockerfile. Make sure you're in the `location_service` directory and run:

```
docker build . -t location_service
```

### Run image

To run the service, run:

```
docker run -p 5000:5000 location_service
```

and the service will be running on [`localhost:5000`](http://localhost:5000/)

## Usage (Endpoints)

### `/all` [GET]

Get all data in the `location_service` database

### `/location` [POST]

Expected body:

```
{
    lat: <Float>,
    lon: <Float>
}
```

and returns the coordinate (row) in the `location_service` database that is closest to the coordinate given in the request body

## Other: Command Line Args

```
    arg="--create-table",
    type=bool,
    help="If you want a table to be created in the database",
    required=False,

    arg="--seed-filename",
    type=str,
    help="String of the filepath of the csv file if you want to seed the database with the csv file contents",
    required=False,
```
