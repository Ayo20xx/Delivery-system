from uuid import UUID

from app.core.security import Oauth2_scheme
from app.database.model import seller
from app.database.redis import is_jti_blacklisted
from app.database.session import get_session
from app.services.seller import SellerService
from app.services.shipment import ShipmentService
from fastapi import Depends, HTTPException,status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from app.utils import decode_access_token


SessionDep=Annotated[AsyncSession,Depends(get_session)]

async def get_shipment_service(session:SessionDep):
    return ShipmentService(session)

async def get_seller_service(session:SessionDep):
    return SellerService(session)

ShipmentServiceDep = Annotated[ShipmentService,Depends(get_shipment_service)]
ServiceSellerDep = Annotated[SellerService,Depends(get_seller_service)]


async def get_access_token(token:Annotated[str,Depends(Oauth2_scheme)]):
        data= decode_access_token(token)

        if data is None or await is_jti_blacklisted(data["jti"]):
            raise HTTPException(
                status_code= status.HTTP_401_UNAUTHORIZED,
                detail="invalid access token"
            )
        return data

async def get_current_data(token_data: Annotated[dict,Depends(get_access_token)],session :SessionDep):
     
     return await session.get(seller,UUID(token_data["user"]["id"]))
     


SellerDep = Annotated[seller,Depends(get_current_data)]