
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import DeliveryDep, get_partner_access_token
from app.api.schemas.delivery_partner import DeliveryPartnerCreate ,DeliveryPartnerRead
from app.database.redis import add_jti_to_blacklist

router = APIRouter (prefix="/partner")


@router.post("/signup",response_model =DeliveryPartnerRead )
async def register_delivery_partner(seller:DeliveryPartnerCreate ,service:DeliveryDep):
    return await service.add(seller)


@router.post("/login")
async def Login__delivery_partner(request_form:Annotated[OAuth2PasswordRequestForm,Depends()],service:DeliveryDep):
    token=await service.token(request_form.username,request_form.password)
    return{
        "access_token": token,
        "type" : "jwt",
    }


@router.get("/logout")
async def logout__delivery_partner(token_data: Annotated[dict,Depends(get_partner_access_token)]):
   return await add_jti_to_blacklist(token_data["jti"] )                       