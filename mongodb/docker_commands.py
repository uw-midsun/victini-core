import docker
from car_data import CarData

client = docker.from_env()


def on_insert(obj: CarData):
    """
    Callback function for when a new document is inserted into the database.
    Parameters:
        obj: The object that was inserted into the database.
    """
    container = client.containers.run("bfirsh/reticulate-splines", detach=True)
    print(container)
