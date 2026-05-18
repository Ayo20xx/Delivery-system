
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.seller import SellerCreate

class SellerService:
    def __init__(self, session: AsyncSession):
        self.session = session
        

    async def add(self, seller_create:SellerCreate):
         new_seller=seller_create(
                **seller_create .model_dump(),
            )
         self.session.add(new_seller)
         self.session.commit()
         self.session.refresh(new_seller)