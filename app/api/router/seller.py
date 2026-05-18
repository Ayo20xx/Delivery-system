
from fastapi import APIRouter

from app.api.dependencies import ServiceSellerDep
from app.api.schemas.seller import SellerCreate ,SellerRead


router = APIRouter (prefix="/seller")


@router.post("/signup",response_model =SellerRead )
async def register_seller(seller:SellerCreate,service:ServiceSellerDep):
    return await service.add(seller)