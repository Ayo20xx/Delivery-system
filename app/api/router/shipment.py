from uuid import UUID

from fastapi import APIRouter
from app.api.dependencies import  DeliveryPartnerServiceDep, SellerDep, ShipmentServiceDep


from fastapi import HTTPException, status

from app.database.model import Shipment
from app.api.schemas.shipment import ShipmentCreate, ShipmentRead, ShipmentUpdate

router=APIRouter()






@router.get("/shipment/{id}" ,response_model= ShipmentRead,)
async def get_shipment_id(id: UUID, Service:ShipmentServiceDep):
   shipment=await Service.get(id)
   if  shipment is None:
       raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND,
           detail="given id does not exist "
       )
  
   return shipment
       
@router.post("/shipment")  
async def submit_shipment(shipment:ShipmentCreate, Service:ShipmentServiceDep, seller : SellerDep)-> Shipment:
    return await Service.add(shipment,seller)
   
   

@router.patch("/shipment/{id}",response_model=ShipmentRead)
async def Update_shipment(id:UUID, shipment_update:ShipmentUpdate,Service:ShipmentServiceDep,partner:DeliveryPartnerServiceDep) -> ShipmentRead:
    update=shipment_update.model_dump(exclude_none=True)
    if not update:
     raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="no data was found",
     )

    return await Service.update(id,shipment_update,partner)
      
@router.get("/cancel",response_model=ShipmentRead)
async def cancel_shipment(id:UUID,seller:SellerDep,Service:ShipmentServiceDep) -> dict[str,str]:
   
    return await Service.cancel(id,seller)
    
    

