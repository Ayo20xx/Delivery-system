from fastapi import FastAPI,status,HTTPException
from schemas import ShipmentCreate,ShipmentRead,ShipmentUpdate
from .database import shipments


app= FastAPI()




@app.get("/shipment" ,response_model= ShipmentRead)
def get_shipment_id(id: int ) :
   if id not in shipments:
       raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND,
           detail="given id does not exist "
       )
  
   return shipments[id]
       
@app.post("/shipment",response_model=None)  
def submit_shipment(shipment:ShipmentCreate)-> dict[str,int]:
    new_ID= max(shipments.keys()) +1
    shipments[new_ID] = {
        **shipment.model_dump(),
        "status": "placed",
    }
    return {"id" :new_ID}


@app.patch("/shipment",response_model=ShipmentRead)
def patch_shipment(id:int, body:ShipmentUpdate):
      shipments[id].update(body)
      return shipments[id]
      
@app.delete("/shipments")
def delete_shipment(id:int) -> dict[str,str]:
    shipments.pop(id)
    return {"details":f"shipment with {id} has been deleted"}
