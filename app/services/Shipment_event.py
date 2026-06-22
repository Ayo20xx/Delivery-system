
from random import randint

from app.database.model import Shipment, ShipmentEvent, ShipmentStatus
from app.database.redis import get_verification_code
from app.services.base import BaseService
from app.services.Notification import NotificationService




class ShipmentEventService(BaseService):
    def __init__(self, session,tasks):
        super().__init__(ShipmentEvent, session)
        self.notification = NotificationService(tasks)
        self.tasks = tasks

    async def add(
            self,
            shipment: Shipment,
            location: int | None = None,
            status: ShipmentStatus | None = None,
            description: str | None = None,
    ) -> ShipmentEvent:
        if (location is None or status is None) and shipment.timeline:
            last_event = await self.get_latest_event(shipment)
            location = location if location is not None else last_event.location
            status = status if status is not None else last_event.status

        if location is None or status is None:
            raise ValueError("location and status are required for the first shipment event")

        new_event = ShipmentEvent(
            location=location,
            status=status,
            description=description if description else self._generate_description(status, location),
            shipment_id=shipment.id,
        )
        await self._notify(shipment, status)
        return await self._add(new_event)
    
    async def get_latest_event(self,shipment:Shipment):
        timeline = list(shipment.timeline)
        timeline.sort(key=lambda event:event.created_at)
        return timeline[-1]

    def _generate_description(self,status: ShipmentStatus,location : int):
        match status:
            case ShipmentStatus.Placed:
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

        if status == ShipmentStatus.in_transit:
            return 



        subject : str
        context = {}
        template_name : str


        match status:
            case ShipmentStatus.Placed:
                subject = "your order is shipped 🚌"
                context["id"] = str(shipment.id)
                context["seller"] = shipment.seller.name
                context["partner"] = shipment.delivery_partner.name
                template_name = "mail_placed.html"

            case ShipmentStatus.out_for_delivery:
                subject = "your order is out for delivery 🚌"
                template_name = "mail_out_for_delivery.html"

                code = randint(100_000,999_999)
                get_verification_code(shipment.id,code)


                if shipment.client_contact_phone :
                    await self.notification.send_sms(
                        to= shipment.client_contact_phone,
                        body=f"Your order is arriving soon! Share your {code} with your delivery executive to recive your package "
                    )
                else:
                    await self.notification.send_email(
                        recipients=[shipment.client_contact_email],
                        subject=" Order is arriving",
                        body = f" Your order is arriving soon! Share your {code} with your delivery executive to receive your package "
                    )

            case ShipmentStatus.delivered:
                subject = "your order is delivered 🚌"
                template_name = "mail_delivered.html"

            case ShipmentStatus.cancelled:
                subject = "your order has been cancelled 🚌"
                template_name = "mail_cancelled.html"
            case _:
                subject = "shipment update"
                template_name = "mail_placed.html"

        await self.notification.send_email_with_template(
            recipients= [shipment.client_contact_email],
            subject= subject,
            context = context,
            template_name = template_name, )