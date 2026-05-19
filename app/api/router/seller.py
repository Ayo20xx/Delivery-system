
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import ServiceSellerDep
from app.api.schemas.seller import SellerCreate ,SellerRead


router = APIRouter (prefix="/seller")


@router.post("/signup",response_model =SellerRead )
async def register_seller(seller:SellerCreate,service:ServiceSellerDep):
    return await service.add(seller)


@router.post("/login")
async def Login_seller(request_form:Annotated[OAuth2PasswordRequestForm,Depends()],service:ServiceSellerDep):
    token=await service.token(request_form.username,request_form.password)
    return{
        "access_token": token,
        "type" : "jwt",
    }