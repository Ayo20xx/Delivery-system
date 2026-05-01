from pydantic import BaseModel,Field
from enum import Enum
class Baseshipment(BaseModel):
     content : str = Field(max_length=30)
     weight : float =Field(lt=25)
     destination : int | None = None 
    
class ShipmentStatus(str,Enum):
        Placed="placed"
        in_transit="in_transit"
        out_for_delivery= "out_for_delivery"
        delivered="delivered"

class ShipmentRead(Baseshipment):
    status : str

class ShipmentCreate(Baseshipment):
  pass

class ShipmentUpdate(BaseModel):
    status: ShipmentStatus