
from uuid import UUID

from app.api.dependencies import DeliveryPartnerServiceDep
from app.database.model import Shipment,seller
from app.api.schemas.shipment import ShipmentCreate,ShipmentUpdate,ShipmentStatus
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime,timedelta
from fastapi import HTTPException,status
from app.services.Delivery_partner import DeliveryPartnerService
from app.services.Shipment_event import ShipmentEventService
from app.services.base import BaseService




class ShipmentService(BaseService):
    def __init__(self,session:AsyncSession,partner_service:DeliveryPartnerService,event_service: ShipmentEventService):
        super().__init__(Shipment,session)
        self.partner_service= partner_service
        self.event_service=event_service

    async def get(self,id:UUID)-> Shipment | None:
        return await self.session._get(id)

    async def add(self,shipment_create:ShipmentCreate,Seller:seller) -> Shipment:
         new_shipment=Shipment(
                **shipment_create.model_dump(),
                status=ShipmentStatus.Placed,
                estimated_delivery=datetime.now() + timedelta(days=3),
                seller_id= Seller.id
            )
         partner=await self.partner_service.assign_shipment(new_shipment)
         new_shipment.delivery_partner_id = partner.id
         shipment= await self._add(new_shipment)
         await self.event_service.add(
             shipment = new_shipment.id,
             location=seller.zip_code,
             status=ShipmentStatus.placed,
             description=f"assigned to {partner.name}"
         )
         return shipment
         

    async def update (self,id:UUID,shipment_update:ShipmentUpdate,partner:DeliveryPartnerServiceDep) -> Shipment:

            shipment=await self.get(id)
            if shipment.delivery_partner_id != partner.id:
                raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                details="not authorized",
            )
            shipment=await self.get(id)
        
            if not shipment:          
                raise HTTPException(status_code=404, detail="shipment not found")

            shipment.sqlmodel_update(shipment_update)

            update = shipment_update.model_dump(exclude_none=True)
            if shipment_update.estimated_delivery:
                 shipment.estimated_delivery =shipment_update.estimated_delivery
            if len(update)> 1 or not shipment_update.estimated_delivery:
                self.event_service.add(
                    shipment=shipment
                    **update,
                )
            return await self._update(shipment)
            

    async def delete(self,id:int ) -> int:
        shipment = await self.get(id)
        if not shipment:
            raise HTTPException(
                status_code=404,
                detail="shipment not found"
            )
        await self._delete(shipment)