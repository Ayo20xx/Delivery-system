from app.database.session import get_session
from app.services.seller import SellerService
from app.services.shipment import ShipmentService
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated


SessionDep=Annotated[AsyncSession,Depends(get_session)]

async def get_shipment_service(session:SessionDep):
    return ShipmentService(session)

async def get_seller_service(session:SessionDep):
    return SellerService(session)

ShipmentServiceDep = Annotated[ShipmentService,Depends(get_shipment_service)]
ServiceSellerDep = Annotated[SellerService,Depends(get_seller_service)]