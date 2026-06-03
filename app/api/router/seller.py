
from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import EmailStr

from app.api.dependencies import ServiceSellerDep, get_seller_access_token
from app.api.schemas.seller import SellerCreate ,SellerRead
from app.database.redis import add_jti_to_blacklist

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




@router.get("/logout")
async def logout_seller(token_data: Annotated[dict,Depends(get_seller_access_token)]):
   return await add_jti_to_blacklist(token_data["jti"] )                       

@router.get("/verify")
async def verify_seller_email(token:str,service:ServiceSellerDep):
    await service.verify_email(token)
    return {"detail": "Account Verified"}

@router.get("/forgot_password")
async def forgot_password(email:EmailStr,service:ServiceSellerDep):
    await service.send_password_reset_link(email,router.prefix)
    return {"detail": "check email for password reset link"}


@router.get("/reset_password")
async def reset_password(token:str,password:str,service:ServiceSellerDep):
    await service.reset_password(token,password)
    return {"detail": "Password successfully reset"}


