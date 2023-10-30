# ETL Scripts Overview

As of writing this README there are currently two ETL scripts that are used to populate the Routemodel and Weather table.
The models that represent these tables exist in models.py in db_gateway, so to update the schema, please refer to that file.

The way that the existing ETLs work, is that they first run any data collection scripts necessary and export it to a csv. This first step allows us to have
a checkpoint of sorts. The intention is that API calls won't have to be repeatedly called to populate the database in case the ETL scripts have to be changed, or if multiple
database seedings have to be done for each dev's database.

Afterwards, the ETL script will ingest any existing/newly-created csv and feed the data into the PostgreSQL via SQLAlchemy.

## Running Scripts

First, enter the etl directory from victini-core by running 
```
cd etl
```

We'll have to install the proper requirements for the scripts, so start by creating a virtual environment and activating it.
I would recommend installing Python 3.10 to ensure the requirements have the proper dependencies.

```
virtualenv venv --python=python3.10
./venv/Scripts/activate
```

Next, install the dependencies

```
pip install -r requirements.txt
```

### Run etl_routemodel.py

To run the etl_routemodel, we'll need a GPX json to provide data for populating our database. There should be a `routemodel_gpx.json` already inside data, but if not, one can be generated at https://mapstogpx.com/ with a Google Maps route.


Here's one that can be used: [Demo Route](https://www.google.ca/maps/dir/Fulton,+MO,+USA/Davenport/Great+River+Rd+%26+Gaylord+Nelson+Hwy,+Trenton,+WI+54014,+USA/@42.7215958,-91.0372306,7z/data=!3m1!4b1!4m35!4m34!1m5!1m1!1s0x87dc8e579b700d25:0xf0215f3f96f20e66!2m2!1d-91.9479586!2d38.8467082!1m20!1m1!1s0x87e234c5e012a2f1:0xe8ea1f6356581fb0!2m2!1d-90.5776367!2d41.5236437!3m4!1m2!1d-92.2319476!2d44.4238558!3s0x87f8338724908edf:0xca9b25d292ef7845!3m4!1m2!1d-92.3766828!2d44.5058247!3s0x87f82f351959945f:0x50b0245a3e723deb!3m4!1m2!1d-92.4467661!2d44.544585!3s0x87f827936d27e451:0xb48e8cc83edcbde7!1m5!1m1!1s0x87f78be36d3d1e0b:0x177144dc524ef09d!2m2!1d-92.5279297!2d44.6013121!3e0?entry=ttu)

The route is 535 miles along the Mississippi River from Fulton, MO to Trenton, WI :)


Now we'll run `etl_routemodel.py`, which will create the routemodel table and populate it with the gpx data.

```
python etl_routemodel/etl_routemodel.py
```

Note, at this point the routemodel table has a foreign key, weather_id, that is unpopulated. We will handle this along with populating the weather table in the next script.

### Run etl_routemodel.py

Pretty simple, just run
```
python etl_weather/etl_weather.py
```

If `weather.csv` already exists, no API calls will be made. Otherwise, an API call will be made to a point every `30km` in the routemodel to get a sample of what the weather looks like in that area. This value can be changed by changing `WEATHER_RANGE = 30000` in `etl_weather.py`. Just make sure to drop the existing values in the Weather table, so that they can be refilled with weather data at the appropriate intervals.