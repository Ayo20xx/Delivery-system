from uuid import UUID

from pydantic import BaseModel, EmailStr,Field
from datetime import datetime
from ...database.model import ShipmentEvent, ShipmentStatus


class Baseshipment(BaseModel):
     content : str 
     weight : float =Field(lt=25)
     destination : int

class ShipmentRead(Baseshipment):
    id : UUID
    timeline: list[ShipmentEvent]
    estimated_delivery : datetime

class ShipmentCreate(Baseshipment):
  client_contact_email : EmailStr
  client_contact_phone : int | None

class ShipmentUpdate(BaseModel):
    location : int | None=Field( default=None)
    status: ShipmentStatus | None=Field( default=None)
    estimated_delivery: datetime | None = Field(default=None)
    description : str | None=Field( default=None)