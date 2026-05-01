from fastapi import FastAPI,status
from typing import Any
from fastapi import HTTPException
from schemas import ShipmentCreate,ShipmentRead,ShipmentUpdate



app= FastAPI()
shipments = { 
    12701:{    
        "weight": 1.2,
        "content": "wooden table",
        "status": "in transit",
    },
    12702:{    
        "weight": 2.5,
        "content": "office chair",
        "status": "delivered",
    },
    12703:{    
        "weight": 0.8,
        "content": "laptop",
        "status": "pending",
    },
    12704:{    
        "weight": 5.3,
        "content": "bookshelf",
        "status": "in transit",
    },
    12705:{    
        "weight": 1.1,
        "content": "desk lamp",
        "status": "delivered",
    },
    12706:{    
        "weight": 3.7,
        "content": "monitor stand",
        "status": "pending",
    },
    12707:{    
        "weight": 0.5,
        "content": "keyboard",
        "status": "in transit",
    }
}
    



@app.get("/shipment" ,response_model= ShipmentRead)
def get_shipment_id(id: int ) :
   if id not in shipments:
       raise HTTPException(
           status_code=status.HTTP_404_NOT_FOUND,
           detail="given id does not exist "
       )
  
   return shipments[id]
       
@app.post("/shipment")  
def submit_shipment(body:ShipmentCreate)-> dict[str,Any]:
    new_ID= max(shipments.keys()) +1
    shipments[new_ID]={

        "content": body.content,
        "weight": body.weight,
        "status": "placed"
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
