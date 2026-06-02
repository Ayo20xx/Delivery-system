from click import UUID
from fastapi import BackgroundTasks, HTTPException,status
from sqlalchemy import select

from app.utils import decode_url_safe_token, generate_access_token, generate_url_safe_token

from .base import BaseService
from app.database.model import User, seller
from sqlalchemy.ext.asyncio import AsyncSession

from passlib.context import CryptContext

from app.services.Notification import NotificationService
from app.config import app_settings







password_context = CryptContext(schemes=["bcrypt"],deprecated="auto")
class UserService(BaseService):
    def __init__(self,model:User,session:AsyncSession,tasks: BackgroundTasks):
        self.model=model
        self.session = session  
        self.notification_service = NotificationService(tasks)
        self.tasks=tasks



    
    async def _add_user(self,data:dict,router_prefix:str):
        user=self.model(
            **data,
            password_hash =password_context.hash(data["password"]),
        )
        user=await self._add(user)

        token= generate_url_safe_token({
            "email" : user.email,
            "id" : str(user.id)
        })

        self.notification_service.send_email_with_template(
            recipients=[user.email],
            subject= "Verify your email",
            context={
                "username": user.name,
                "verification_url": f"http://{app_settings.App_domain}/{router_prefix}/verify/token={token}",
            },
            template_name="mail_email_verify.html"
        )
        return user 
    

    async def verify_email(self,token:str):
        token_data = decode_url_safe_token(token)
        if not token_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="invalid token"
            )
        
        user=self._get( UUID(token_data["id"]))

        user.email_verified = True









    async def _get_by_email(self,email) -> User | None :
        return await self.session.scalar(select(seller).where(seller.email==email))
    





    
    async def _generate_token(self,email,password)-> str :
       
       user= await self._get_by_email(email)

       if user is None or not password_context.verify(password,user.password_hash):
           raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Email or password is  incorrect ")
       if not user.email_verified:
           raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Email is not verified ")
       token= generate_access_token(data={
           "user" :{
               "name" : user.name,
               "id" : str(user.id),
           }
           
       })
       
        
       return token

        
