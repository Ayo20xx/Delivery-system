from uuid import UUID

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from app.api.dependencies import  DeliveryPartnerServiceDep, SellerDep, ShipmentServiceDep


from fastapi import HTTPException, status

from app.database.model import Shipment
from app.api.schemas.shipment import ShipmentCreate, ShipmentRead, ShipmentUpdate
from app.utils import TEMPLATE_DIR

router=APIRouter()


templates=Jinja2Templates(TEMPLATE_DIR)


@router.get("/track" ,response_model= ShipmentRead,)
async def Track_id(request:Request,id: UUID, Service:ShipmentServiceDep):
   shipment=await Service.get(id)
   context = shipment.model_dump()
   context["status"] = shipment.status
   context["Partner"] = shipment.delivery_partner.name
   context["timeline"] = shipment.timeline
   
  
   return templates.TemplateResponse(
      request=request,
      name="track.html",
      context= context,
   )




@router.get("/shipment" ,response_model= ShipmentRead,)
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
    
    

