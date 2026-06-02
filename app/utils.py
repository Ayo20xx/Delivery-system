from datetime import datetime, timedelta, timezone
from pathlib import Path
from uuid import uuid4
from fastapi import HTTPException,status
import jwt
from app.config import security_settings



APP_DIR = Path(__file__).resolve().parent
TEMPLATE_DIR = APP_DIR/"template"

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