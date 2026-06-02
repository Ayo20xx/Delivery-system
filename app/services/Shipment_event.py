
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
        subject : str
        context = {}
        template_name : str


        match status:
            case ShipmentStatus.placed :
                    subject="your order is shipped 🚌",
                    context["seller"] = shipment.seller.name,
                    context[ "partner"] = shipment.delivery_partner.name
                    template_name= "mail_placed.html" 
                

            case ShipmentStatus.out_for_delivery:
                subject="your order is out for delivery 🚌",
                context["seller"] = shipment.seller.name,
                context[ "partner"] = shipment.delivery_partner.name
                template_name= "mail_out_for_delivery.html" 


            case ShipmentStatus.delivered:
                subject="your order is delivered 🚌",
                context["seller"] = shipment.seller.name,
                context[ "partner"] = shipment.delivery_partner.name
                template_name= "mail_delivered.html" 

            case ShipmentStatus.cancelled:
                subject="your order has been cancelled 🚌",
                context["seller"] = shipment.seller.name,
                context[ "partner"] = shipment.delivery_partner.name
                template_name= "mail_cancelled.html" 

        await self.notification.send_email_with_template(
            recipients= [shipment.client_contact_email],
            subject= subject,
            context = context,
            template_name = template_name, )