
from uuid import UUID

from app.api.dependencies import  SellerDep
from app.database.model import DeliveryPartner, Shipment, seller
from app.api.schemas.shipment import ShipmentCreate, ShipmentUpdate, ShipmentStatus
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta
from fastapi import HTTPException, status
from app.database.redis import is_verification_code
from app.services.Delivery_partner import DeliveryPartnerService
from app.services.Shipment_event import ShipmentEventService
from app.services.base import BaseService




class ShipmentService(BaseService):
    def __init__(self,session:AsyncSession,partner_service:DeliveryPartnerService,event_service: ShipmentEventService):
        super().__init__(Shipment,session)
        self.partner_service= partner_service
        self.event_service=event_service

    async def get(self, id: UUID) -> Shipment | None:
        return await self._get(id)

    async def add(self, shipment_create: ShipmentCreate, seller: seller) -> Shipment:
        new_shipment = Shipment(
            **shipment_create.model_dump(),
            estimated_delivery=datetime.now() + timedelta(days=3),
            seller_id=seller.id,
        )
        partner = await self.partner_service.assign_shipment(new_shipment)
        new_shipment.delivery_partner_id = partner.id
        shipment = await self._add(new_shipment)
        event = await self.event_service.add(
            shipment=shipment,
            location=seller.zip_code if seller.zip_code is not None else shipment.destination,
            status=ShipmentStatus.Placed,
            description=f"assigned to {partner.name}",
        )
        shipment.timeline.append(event)
        return shipment
         

    async def update(self, id: UUID, shipment_update: ShipmentUpdate, partner: DeliveryPartner) -> Shipment:
        shipment = await self.get(id)
        if not shipment:
            raise HTTPException(status_code=404, detail="shipment not found")

        if shipment.delivery_partner_id != partner.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="not authorized",
            )
        if shipment_update.status == ShipmentStatus.delivered:
            code=await is_verification_code(shipment.id)

            if code != shipment_update.verification_code:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    details= "client not authorised",
                )


        update_data = shipment_update.model_dump(exclude_none=True,exclude="verification_code")
        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="no data was found",
            )

        if shipment_update.estimated_delivery:
            shipment.estimated_delivery = shipment_update.estimated_delivery

        if (
            shipment_update.location is not None
            or shipment_update.status is not None
            or shipment_update.description is not None
        ):
            last_event = await self.event_service.get_latest_event(shipment) if shipment.timeline else None
            await self.event_service.add(
                shipment=shipment,
                location=shipment_update.location if shipment_update.location is not None else last_event.location,
                status=shipment_update.status if shipment_update.status is not None else last_event.status,
                description=shipment_update.description,
            )

        return await self._update(shipment)
            
    async def cancel(self, id: UUID, seller: SellerDep) -> Shipment:
        shipment = await self.get(id)
        if not shipment:
            raise HTTPException(status_code=404, detail="shipment not found")

        if shipment.seller_id != seller.id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not Authorized",
            )

        event = await self.event_service.add(
            shipment=shipment,
            location=(
                shipment.timeline[-1].location
                if shipment.timeline
                else seller.zip_code if seller.zip_code is not None else shipment.destination
            ),
            status=ShipmentStatus.cancelled,
        )
        shipment.timeline.append(event)
        return await self._update(shipment)

    async def delete(self, id: UUID) -> None:
        shipment = await self.get(id)
        if not shipment:
            raise HTTPException(status_code=404, detail="shipment not found")
        await self._delete(shipment)