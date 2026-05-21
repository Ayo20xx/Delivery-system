from datetime import datetime, timedelta

import jwt
from app.config import security_settings

def generate_access_token(data : dict,exp:timedelta=timedelta(days=1)):
    token=jwt.encode(
           payload={
                    **data,
               "exp": datetime.now() + exp
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
    except jwt.PyJWKError:
        return None