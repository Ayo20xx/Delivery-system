
from fastapi import HTTPException,status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.schemas.seller import SellerCreate
from app.database.model import seller
from passlib.context import CryptContext
from app.utils import generate_access_token



password_context = CryptContext(schemes=["bcrypt"],deprecated="auto")


class SellerService:
    def __init__(self, session: AsyncSession):
        self.session = session
        

    async def add(self, Credentials:SellerCreate) -> seller :
         new_seller=seller(
             **Credentials.model_dump(exclude=["password"]),
             password_hash= password_context.hash(Credentials.password.encode("utf-8")[:72])
         )
         self.session.add(new_seller)
         await self.session.commit()
         await self.session.refresh(new_seller)

         return new_seller
    
    async def token(self,email,password)-> str :
       
       result = await self.session.execute (select(seller).where(seller.email == email))
       Seller=result.scalar()

       if Seller is None or not password_context.verify(password,Seller.password_hash):
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email or password is  incorrect ")
       token= generate_access_token(data={
           "user" :{
               "name" : Seller.name,
               "id" : str(Seller.id),
           }
           
       })
       
        
       return token
  