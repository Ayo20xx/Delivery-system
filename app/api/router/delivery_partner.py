
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import DeliveryDep, DeliveryPartnerServiceDep, get_partner_access_token
from app.api.schemas.delivery_partner import DeliveryPartnerCreate ,DeliveryPartnerRead, DeliveryPartnerUpdate
from app.database.redis import add_jti_to_blacklist

router = APIRouter (prefix="/partner")


@router.post("/signup",response_model =DeliveryPartnerRead )
async def register_delivery_partner(seller:DeliveryPartnerCreate ,service):
    return await service.add(seller)


@router.post("/login")
async def Login__delivery_partner(request_form:Annotated[OAuth2PasswordRequestForm,Depends()],service:DeliveryPartnerServiceDep):
    token=await service.token(request_form.username,request_form.password)
    return{
        "access_token": token,
        "type" : "jwt",
    }

@router.get("/verify")
async def verify_seller_email(token:str,service:DeliveryPartnerServiceDep):
    await service.verify_email(token)
    return {"detail": "Account Verified"}


@router.post("/",response_model= DeliveryPartnerRead)
async def update_delivery_partner(partner_update:DeliveryPartnerUpdate,partner:DeliveryDep, service:DeliveryPartnerServiceDep):
        update=partner_update.model_dump(exclude_none=True)
        if not update:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="no data was found",
            )
        return await  service.update (partner.sqlmodel_update(update))



@router.get("/logout")
async def logout__delivery_partner(token_data: Annotated[dict,Depends(get_partner_access_token)]):
   return await add_jti_to_blacklist(token_data["jti"] )                       