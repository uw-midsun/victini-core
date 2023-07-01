import uuid
from typing import Dict, Optional
from pydantic import BaseModel, Field
from bson import Binary


class Location(BaseModel):
    """
    The location of the car.
    Lattitude: Key value pair, where key is the direction and value is the number. Eg:{ 'N': '60.15334714532838' }
    Longitude: Key value pair, where key is the direction and value is the number. Eg:{ 'E': '4.407109787976424' }
    """

    Lattitude: Dict[str, float]
    Longitude: Dict[str, float]


def uuid_conversion() -> str:
    """
    Creates a UUID and converts it to a string for use as a MongoDB _id.
    """
    return str(Binary.from_uuid(uuid.uuid4()))


class CarData(BaseModel):
    """
    Model representing the data sent from the car.
    Right now, it only contains the location and speed of the car but it can be expanded to include more data.
    """

    _id: Optional[str] = Field(default_factory=uuid_conversion, alias="_id")
    location: Location = Field(...)
    speed: int = Field(...)
