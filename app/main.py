from fastapi import FastAPI,status,HTTPException
from .schemas import ShipmentCreate,ShipmentRead,ShipmentUpdate
from contextlib import asynccontextmanager
from datetime import datetime,timedelta
from .database.model import Shipment,ShipmentStatus
from .database.session import SessionDep,create_db_tables

@asynccontextmanager
async def lifespan_handeler(app:FastAPI):
    create_db_tables()
    yield


app= FastAPI(
    lifespan= lifespan_handeler,
)




@app.get("/shipment/{id}" ,response_model= ShipmentRead,)
def get_shipment_id(id: int, session:SessionDep) -> ShipmentRead:
   shipment=session.get(Shipment,id)
   if  shipment is None:
       raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND,
           detail="given id does not exist "
       )
  
   return shipment
       
@app.post("/shipment",response_model=None)  
def submit_shipment(shipment:ShipmentCreate, session:SessionDep)-> dict[str,int]:
    new_shipment=Shipment(
        **shipment.model_dump(),
        status=ShipmentStatus.Placed,
        estimated_delivery=datetime.now() + timedelta(days=3),
    )
    session.add(new_shipment)
    session.commit()
    session.refresh(new_shipment)
    return {"id":new_shipment.id}

@app.patch("/shipment/{id}",response_model=ShipmentRead)
def patch_shipment(id:int, shipment_update:ShipmentUpdate,session:SessionDep) -> ShipmentRead:
    update=shipment_update.model_dump(exclude_none=True)
    if not update:
     raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="no data was found",
     )
    shipment=session.get(Shipment,id)
    shipment = session.get(Shipment, id)
    if not shipment:          # add this
        raise HTTPException(status_code=404, detail="shipment not found")

    shipment.sqlmodel_update(update)
    session.add(shipment)
    session.commit()
    session.refresh(shipment)
     
    return shipment
      
@app.delete("/shipment/{id}")
def delete_shipment(id:int,session:SessionDep) -> dict[str,str]:
    shipment=session.delete(session.get(Shipment,id))
    if not shipment:
        raise HTTPException(
            status_code=404,
            detail="shipment not found"
        )

    session.commit()
    return {"details":f"shipment with {id} has been deleted"}
