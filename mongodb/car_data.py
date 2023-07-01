import uuid
from typing import Dict, Optional
from pydantic import BaseModel, Field
from bson import Binary

class Location(BaseModel):
    Lattitude: Dict[str, float]
    Longitude: Dict[str, float]

def uuid_conversion() -> str:
    return str(Binary.from_uuid(uuid.uuid4()))

class CarData(BaseModel):
    id: Optional[str] = Field(default_factory=uuid_conversion, alias='_id')
    location: Location = Field(...)
    speed: int = Field(...)
    
