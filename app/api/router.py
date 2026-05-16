from .router import shipment,seller


from fastapi import APIRouter

master_router = APIRouter()


master_router.include_router(shipment)
master_router.include_router(seller)