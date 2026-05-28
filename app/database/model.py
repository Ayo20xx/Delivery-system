from datetime import datetime
from enum import Enum
from pydantic import EmailStr
from sqlalchemy import ARRAY, INTEGER
from sqlmodel import Column, Field, Relationship, SQLModel
from uuid import uuid4,UUID
from sqlalchemy.dialects import postgresql


class ShipmentStatus(str,Enum):
        Placed="placed"
        in_transit="in_transit"
        out_for_delivery= "out_for_delivery"
        delivered="delivered"

class Shipment (SQLModel,table=True):
    __tablename__="shipment"
    id : UUID =Field(sa_column=Column(
          postgresql.UUID,
          default= uuid4,
          primary_key= True,
          
    ))
    created_at : datetime = Field(sa_column=Column(
                postgresql.TIMESTAMP,
                default=datetime.now
         ))
    content : str
    weight : float = Field(le=25)
    destination : int
    estimated_delivery : datetime

    timeline: list["ShipmentEvent"] = Relationship(
           back_populates= "shipment",sa_relationship_kwargs={"lazy":"selectin"}
    )

    seller_id : UUID = Field(foreign_key="seller.id")

    Seller: "seller" = Relationship(back_populates="shipments",sa_relationship_kwargs={"lazy":"selectin"})

    delivery_partner_id : UUID = Field(foreign_key="delivery_partner.id")
    delivery_partner : "DeliveryPartner"= Relationship(back_populates="shipments",sa_relationship_kwargs={"lazy":"selectin"})

    @property
    def status(self):
           return self.timeline[-1].status if len(self.timeline) > 0 else None

class ShipmentEvent(SQLModel,table=True):
       __tablename__="shipment_event"
       id : UUID =Field(sa_column=Column(
          postgresql.UUID,
          default= uuid4,
          primary_key= True,
          
    ))
       created_at : datetime = Field(sa_column=Column(
                postgresql.TIMESTAMP,
                default=datetime.now
         ))
       location: int 
       status :ShipmentStatus
       description : str | None =Field(default=None)

       shipment_id : UUID = Field(foreign_key="shipment.id")
       shipment: Shipment = Relationship(back_populates="timeline ",sa_relationship_kwargs={"lazy":"selectin"})



 
class User (SQLModel):
         
         name : str 
         email : EmailStr
         password_hash: str = Field(exclude= True)
         created_at : datetime = Field(sa_column=Column(
                postgresql.TIMESTAMP,
                default=datetime.now,
         ))
        



class seller (User, table = True ):
      __tablename__ ="seller"
      
      id:  UUID =Field(sa_column=Column(
          postgresql.UUID,
          default= uuid4,
          primary_key= True,
          
    ))
      created_at : datetime = Field(sa_column=Column(
                postgresql.TIMESTAMP,
                default=datetime.now
         ))
      shipments : list[Shipment] =Relationship(back_populates="Seller", sa_relationship_kwargs={"lazy":"selectin"})
      address: str | None =Field(default=None)
      zip_code : int | None =Field(default=None)




class DeliveryPartner(SQLModel,table = True) :
      __tablename__="delivery_partner"
      id:  UUID =Field(sa_column=Column(
            postgresql.UUID,
            default= uuid4,
            primary_key= True,
            
      ))
      created_at : datetime = Field(sa_column=Column(
                postgresql.TIMESTAMP,
                default=datetime.now
         ))
      serviceable_zip_codes : list[int] = Field(sa_column=Column(ARRAY(INTEGER)))

      max_handling_capacity : int 

      shipments : list[Shipment] =Relationship(back_populates="delivery_partner",sa_relationship_kwargs={"lazy":"selectin"})


      @property
      def active_shipments(self):
             return [shipment for shipment in self.shipments if shipment.status != ShipmentStatus.delivered]
      @property
      def current_handling_capacity(self):
             return self.max_handling_capacity - len(self.active_shipments)
