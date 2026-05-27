
from app.database.model import Shipment, ShipmentEvent, ShipmentStatus
from app.services import  shipment
from app.services.base import BaseService




class ShipmentEventService(BaseService):
    def __init__(self, session):
        super().__init__(ShipmentEvent, session)

    async def add(
            self ,
            shipments :Shipment,
            location :int=None,
            status : ShipmentStatus=None,
            description : str = None,
    )-> ShipmentEvent:
        if not location or not status:
            last_event =self.get_latest_event(shipments)
            location = location if location else last_event.location
            status = status if status else last_event.status

        new_event= ShipmentEvent(
            location=location,
            status = status,
            description= description if description else self._generate_description(status,location),
            shipment_id= shipment.id,

        )
        return await self._add(new_event)
    
    async def get_latest_event(self,shipments:Shipment):
        timeline=shipments.timeline
        timeline.sort(key=lambda event:event.created_at)
        return timeline[-1]
    def _generate_description(self,status: ShipmentStatus,location : int):
        match status:
            case ShipmentStatus.placed:
                return "assigned delivery partner"
            case ShipmentStatus.out_for_delivery:
                return "shipment out for delivery"
            case ShipmentStatus.delivered:
                return "successfully delivered"
            case _:
                return f"scanned at {location}"