
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import DeliveryDep, DeliveryPartnerServiceDep, get_partner_access_token
from app.api.schemas.delivery_partner import DeliveryPartnerCreate, DeliveryPartnerRead, DeliveryPartnerUpdate
from app.database.redis import add_jti_to_blacklist

router = APIRouter(prefix="/partner")


@router.post("/signup", response_model=DeliveryPartnerRead)
async def register_delivery_partner(delivery_partner: DeliveryPartnerCreate, service: DeliveryPartnerServiceDep):
    return await service.add(delivery_partner)


@router.post("/login")
async def Login__delivery_partner(request_form: Annotated[OAuth2PasswordRequestForm, Depends()], service: DeliveryPartnerServiceDep):
    token = await service.token(request_form.username, request_form.password)
    return {
        "access_token": token,
        "type": "jwt",
    }


@router.get("/verify")
async def verify_partner_email(token: str, service: DeliveryPartnerServiceDep):
    await service.verify_email(token)
    return {"detail": "Account Verified"}


@router.post("/", response_model=DeliveryPartnerRead)
async def update_delivery_partner(partner_update: DeliveryPartnerUpdate, partner: DeliveryDep, service: DeliveryPartnerServiceDep):
    update_data = partner_update.model_dump(exclude_none=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="no data was found",
        )

    if update_data.get("serviceable_zip_codes") is not None:
        partner.serviceable_zip_codes = update_data["serviceable_zip_codes"]
    if update_data.get("max_handling_capacity") is not None:
        partner.max_handling_capacity = update_data["max_handling_capacity"]

    return await service.update(partner)


@router.get("/logout")
async def logout__delivery_partner(token_data: Annotated[dict, Depends(get_partner_access_token)]):
    return await add_jti_to_blacklist(token_data["jti"])
                       