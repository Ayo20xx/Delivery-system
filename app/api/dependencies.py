from uuid import UUID

from app.core.security import Oauth2_scheme_seller, Oauth2_scheme_DeliveryPartner
from app.database.model import seller, DeliveryPartner
from app.database.redis import is_jti_blacklisted
from app.database.session import get_session
from app.services.Delivery_partner import DeliveryPartnerService
from app.services.Shipment_event import ShipmentEventService
from app.services.seller import SellerService
from app.services.shipment import ShipmentService
from fastapi import BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.utils import decode_access_token


SessionDep = Annotated[AsyncSession, Depends(get_session)]

async def get_shipment_service(session: SessionDep, tasks: BackgroundTasks):
    return ShipmentService(
        session,
        DeliveryPartnerService(session, tasks),
        ShipmentEventService(session, tasks),
    )


async def get_seller_service(session: SessionDep, tasks: BackgroundTasks):
    return SellerService(session, tasks)


ShipmentServiceDep = Annotated[ShipmentService, Depends(get_shipment_service)]
ServiceSellerDep = Annotated[SellerService, Depends(get_seller_service)]


def get_delivery_partner_service(session: SessionDep, tasks: BackgroundTasks):
    return DeliveryPartnerService(session, tasks)


async def _get_access_token(token: str):
    data = decode_access_token(token)

    if data is None or await is_jti_blacklisted(data["jti"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="invalid access token",
        )
    return data


async def get_seller_access_token(token: Annotated[str, Depends(Oauth2_scheme_seller)]):
    return await _get_access_token(token)


async def get_partner_access_token(token: Annotated[str, Depends(Oauth2_scheme_DeliveryPartner)]):
    return await _get_access_token(token)


async def get_seller_data(token_data: Annotated[dict, Depends(get_seller_access_token)], session: SessionDep):
    seller_obj = await session.get(seller, UUID(token_data["user"]["id"]))
    if seller_obj is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
        )
    return seller_obj


async def get_partner_data(token_data: Annotated[dict, Depends(get_partner_access_token)], session: SessionDep):
    partner_obj = await session.get(DeliveryPartner, UUID(token_data["user"]["id"]))
    if partner_obj is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized",
        )
    return partner_obj


SellerDep = Annotated[seller, Depends(get_seller_data)]

DeliveryDep = Annotated[DeliveryPartner, Depends(get_partner_data)]

DeliveryPartnerServiceDep = Annotated[DeliveryPartnerService, Depends(get_delivery_partner_service)]

