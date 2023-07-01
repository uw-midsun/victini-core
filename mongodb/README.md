# Mongo DB Setup

## Initialization

There are two ways to initialize the database:

1. Create a MongoDB Atlas account and use the free tier to create a cluster. Then, create a database and a collection. Finally, create a user with read/write access to the database. You will need the connection string to the database to connect to it from the application. Set the `DB_NAME` and the `COLLECTION_NAME` in the env file and the The connection string should look like this:

    ```bash
    mongodb+srv://<username>:<password>@<cluster-url>/<database>?retryWrites=true&w=majority
    ```

2. Use the docker-compose file in this directory to create a local MongoDB instance. The database name is `race-data` the collection name is `car-location` and the The connection string should look like this:

    ```bash
    mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.10.0
    ```

**Note**: Currently this is not working since the inserted record does not appear and change stream works only with replica sets instead of standalone instances. So we need to create a replica set for the local instance.

## Usage

Add the connection string to the `MONGO_URL` environment variable in the .env file in this directory. Running the `test_insert.py` script will add a value to the specificied database and collection.

The `db_connect.py` script can be used to connect to the database and wait for real-time updates. The script will print the latest value in the database and will print any new values that are added to the database. The script will run until it is terminated. The script will call the `on_insert` function in the `docker_commands.py` file when a new value is added to the database.

The `docker_commands.py` file contains details on which container to run based on the newest element received by the `db_connect.py` file. The `docker_commands.py` file will be updated to include the commands to run the various microservices depending on the data received.

## References

- [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
- [MongoDB Docker Image](https://hub.docker.com/_/mongo)
- [MongoDB Python Driver](https://pypi.org/project/pymongo/)
- [MongoDB Change Streams](https://docs.mongodb.com/manual/changeStreams/)
