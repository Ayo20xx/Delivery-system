from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4
from fastapi import HTTPException,status
from itsdangerous import  BadSignature, SignatureExpired, URLSafeTimedSerializer
import jwt
from app.config import security_settings


_serializer=URLSafeTimedSerializer(security_settings.JWT_SECRET)


APP_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = APP_DIR/"templates"

def generate_access_token(data : dict,exp:timedelta=timedelta(seconds=15)):
    token=jwt.encode(
           payload={
                    **data,
                    "jti":str(uuid4()),
               "exp": datetime.now(timezone.utc) + exp
               },
           
           algorithm= security_settings.JWT_ALGORITHM,
           key= security_settings.JWT_SECRET,
       )
    return token 

def decode_access_token(token:str)-> dict | None :

    try:
        return  jwt.decode(
        jwt=token,
        key=security_settings.JWT_SECRET,
        algorithms=[security_settings.JWT_ALGORITHM]
    )

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code= status.HTTP_401_UNAUTHORIZED,
            detail="Expired access token"
        )
    except jwt.PyJWKError:
        return None
    


token=_serializer.dumps({"email":"user@his.site"})

token_data=_serializer.loads(token,max_age=timedelta(days=1).total_seconds())



def generate_url_safe_token(data:dict,salt: str | None = None) -> str:
    return _serializer.dumps(data,salt=salt)

def decode_url_safe_token(token:str,salt: str | None = None,expiry:timedelta | None = None) -> dict | None:
    try:
        return _serializer.loads(token,salt=salt,max_age=expiry.total_seconds() if expiry else None)
    except (BadSignature,SignatureExpired):
        return None