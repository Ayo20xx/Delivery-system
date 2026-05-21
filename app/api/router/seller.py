
from typing import Annotated

from fastapi import APIRouter, Depends,HTTPException,status
from fastapi.security import OAuth2PasswordRequestForm

from app.api.dependencies import ServiceSellerDep, SessionDep
from app.api.schemas.seller import SellerCreate ,SellerRead
from app.database.model import seller
from app.core.security import Oauth2_scheme
from app.utils import decode_access_token

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


@router.get("/dashboard")
async def get_dashboard(token:Annotated[str,Depends(Oauth2_scheme)], session : SessionDep):
    data= decode_access_token(token)

    if data is None:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="invalid access token"
        )
    Seller= await session.get(seller,data["user"]["id"])

    return Seller 
