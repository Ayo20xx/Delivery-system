from datetime import datetime
from enum import Enum
from pydantic import EmailStr
from sqlmodel import Field, Relationship, SQLModel


class ShipmentStatus(str,Enum):
        Placed="placed"
        in_transit="in_transit"
        out_for_delivery= "out_for_delivery"
        delivered="delivered"

class Shipment (SQLModel,table=True):
    __tablename__="shipment"
    id : int =Field(default=None,primary_key=True)
    content : str
    weight : float = Field(le=25)
    destination : int
    status : ShipmentStatus
    estimated_delivery : datetime

    seller_id : int = Field(foreign_key="seller.id")

    Seller: "seller" = Relationship(back_populates="shipments",sa_relationship_kwargs={"lazy":"selectin"})




class seller (SQLModel, table = True ):
      
      id: int = Field(default=None,primary_key=True)
      name : str 

      email : EmailStr
      password_hash: str 

      shipments = list[Shipment] =Relationship(back_populates="Seller", sa_relationship_kwargs={"lazy":"selectin"})