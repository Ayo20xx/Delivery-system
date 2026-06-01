
from app.database.model import Shipment, ShipmentEvent, ShipmentStatus
from app.services import  shipment
from app.services.base import BaseService
from app.services.Notification import NotificationService




class ShipmentEventService(BaseService):
    def __init__(self, session,tasks):
        super().__init__(ShipmentEvent, session)
        self.notification = NotificationService()
        self.tasks=tasks

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
        await self._notify(shipment,status)
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
            case ShipmentStatus.cancelled:
                return "cancelled by seller"
            case _:
                return f"scanned at {location}"
            
    async def _notify(self,shipment:Shipment,status:ShipmentStatus):
        match status:
            case ShipmentStatus.placed :
                await self.notification.send_email(
                    recipients=[Shipment.client_contact_email],
                    subject="your order is shipped 🚌",
                    body=f"Your order with {shipment.Seller.name} is picked up by {shipment.delivery_partner.name} and is on its way to you ",
                )
            case ShipmentStatus.out_for_delivery:
                await self.notification.send_email(
                    recipients=[Shipment.client_contact_email],
                    subject="your order is Arriving 🚌",
                    body="Your order with being delivered ,please ensure you are available ",
                )

