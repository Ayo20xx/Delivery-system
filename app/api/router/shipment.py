from fastapi import APIRouter
from app.api.dependencies import ShipmentServiceDep


from fastapi import HTTPException, status

from app.database.model import Shipment
from app.api.schemas.shipment import ShipmentCreate, ShipmentRead, ShipmentUpdate

router=APIRouter()






@router.get("/shipment/{id}" ,response_model= ShipmentRead,)
async def get_shipment_id(id: int, Service:ShipmentServiceDep):
   shipment=await Service.get(id)
   if  shipment is None:
       raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND,
           detail="given id does not exist "
       )
  
   return shipment
       
@router.post("/shipment")  
async def submit_shipment(shipment:ShipmentCreate, Service:ShipmentServiceDep)-> Shipment:
    return await Service.add(shipment)
   
   

@router.patch("/shipment/{id}",response_model=ShipmentRead)
async def patch_shipment(id:int, shipment_update:ShipmentUpdate,Service:ShipmentServiceDep) -> ShipmentRead:
    update=shipment_update.model_dump(exclude_none=True)
    if not update:
     raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="no data was found",
     )
    shipment=await Service.update(id,update)
    return shipment
      
@router.delete("/shipment/{id}")
async def delete_shipment(id:int,Service:ShipmentServiceDep) -> dict[str,str]:
   
    await Service.delete(id)
    

    return {"details":f"shipment with {id} has been deleted"}
