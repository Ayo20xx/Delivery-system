from pydantic import BaseModel,Field
from datetime import datetime
from .database.model import ShipmentStatus


class Baseshipment(BaseModel):
     content : str 
     weight : float =Field(lt=25)
     destination : int 

class ShipmentRead(Baseshipment):
    status : ShipmentStatus
    estimated_delivery : datetime

class ShipmentCreate(Baseshipment):
  pass

class ShipmentUpdate(BaseModel):
    status: ShipmentStatus | None=Field( default=None)
    estimated_delivery: datetime | None = Field(default=None)