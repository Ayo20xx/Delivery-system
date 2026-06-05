from fastapi import HTTPException, status
from sqlalchemy import select
from sqlmodel import any_
from app.api.schemas.delivery_partner import DeliveryPartnerCreate
from app.database.model import DeliveryPartner, Shipment

from app.services.user import UserService


class DeliveryPartnerService(UserService):
    def __init__(self, session,tasks):
        super().__init__(DeliveryPartner, session,tasks)
    
    async def add(self,delivery_partner: DeliveryPartnerCreate):
        return await self._add_user(
            delivery_partner.model_dump(),"partner"
        )
    
    async def get_partner_by_zipcode(self, zipcode: int):
        result = await self.session.execute(
            select(DeliveryPartner).where(
                zipcode == any_(DeliveryPartner.serviceable_zip_codes)
            )
        )
        return result.scalars().all()

    async def assign_shipment(self, shipment: Shipment):
        eligible_partners = await self.get_partner_by_zipcode(shipment.destination)

        for partner in eligible_partners:
            if partner.current_handling_capacity > 0:
                partner.shipments.append(shipment)
                return partner
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE,detail="no delivery partner available")

    async def update(self,partner:DeliveryPartner):
        return await self._update(partner)

    async def token(self,email,password) -> str:
        return await self._generate_token(email,password)