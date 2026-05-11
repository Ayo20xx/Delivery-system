from fastapi import APIRouter
from app.services.shipment import ShipmentService


from fastapi import HTTPException, status

from app.database.model import Shipment
from app.database.session import SessionDep
from .schemas.shipment import ShipmentCreate, ShipmentRead, ShipmentUpdate

router=APIRouter()






@router.get("/shipment/{id}" ,response_model= ShipmentRead,)
async def get_shipment_id(id: int, session:SessionDep) -> ShipmentRead:
   shipment=ShipmentService(session).get(id)
   if  shipment is None:
       raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND,
           detail="given id does not exist "
       )
  
   return shipment
       
@router.post("/shipment")  
async def submit_shipment(shipment:ShipmentCreate, session:SessionDep)-> Shipment:
    return await ShipmentService(session).add(shipment)
   
   

@router.patch("/shipment/{id}",response_model=ShipmentRead)
async def patch_shipment(id:int, shipment_update:ShipmentUpdate,session:SessionDep) -> ShipmentRead:
    update=shipment_update.model_dump(exclude_none=True)
    if not update:
     raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="no data was found",
     )
    shipment=await ShipmentService(session).update(shipment_update)
    return shipment
      
@router.delete("/shipment/{id}")
async def delete_shipment(id:int,session:SessionDep) -> dict[str,str]:
   
    await ShipmentService(session).delete(id)
    await session.commit()

    return {"details":f"shipment with {id} has been deleted"}
