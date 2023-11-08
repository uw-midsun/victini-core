# Location Service

This service acts as an entrypoint for the car to the microservices. The car will send it's coordinates and this service will map the car's coordinates to the routemodel coordinates. Then this service will send a request containing the car's raw data and routemodel coordinates to the historical car/MongoDB service.

---

## Usage (Endpoints)

### `/all` [GET]

Retruns all the data in the `location_service` database
Expected body:

```
{
    auth_key: <String>
}
```

### `/location` [POST]

Expected body:

```
{
    lat: <Float>,
    lon: <Float>,
    auth_key: <String>
}
```

and returns the coordinate (row) in the `location_service` database that is closest to the coordinate given in the request body

---

## Docker Commands

### Build image

Make sure you have the docker daemon running. Make sure you're in the `location_service` directory and run:

```
docker build . -t location_service
```

### Run image

To run the service, run:

```
docker run -p 5000:5000 location_service
```

and the service will be running on [localhost:5000](http://localhost:5000/)
