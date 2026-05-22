from app.database.model import Shipment,seller
from app.api.schemas.shipment import ShipmentCreate,ShipmentUpdate,ShipmentStatus
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime,timedelta
from fastapi import HTTPException

class ShipmentService:
    def __init__(self,session:AsyncSession):
        self.session = session
        

    async def get(self,id:int)-> Shipment:
        return await self.session.get(Shipment,id)

    async def add(self,shipment_create:ShipmentCreate,Seller:seller) -> Shipment:
         new_shipment=Shipment(
                **shipment_create.model_dump(),
                status=ShipmentStatus.Placed,
                estimated_delivery=datetime.now() + timedelta(days=3),
                seller_id= Seller.id
            )
         self.session.add(new_shipment)
         await self.session.commit()
         await self.session.refresh(new_shipment)
         return new_shipment

    async def update (self,id:int,shipment_update:ShipmentUpdate) -> Shipment:
        shipment=await self.get(id)
        
        if not shipment:          
            raise HTTPException(status_code=404, detail="shipment not found")

        shipment.sqlmodel_update(shipment_update)
        self.session.add(shipment)
        await self.session.commit()
        await self.session.refresh(shipment)

        return shipment

    async def delete(self,id:int ) -> int:
        shipment = await self.session.get(Shipment, id)
        if not shipment:
            raise HTTPException(
                status_code=404,
                detail="shipment not found"
            )
        shipment = await self.session.get(Shipment, id)
        await self.session.commit()