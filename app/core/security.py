from fastapi.security import OAuth2PasswordBearer


Oauth2_scheme_seller=OAuth2PasswordBearer(tokenUrl="/seller/login")
Oauth2_scheme_DeliveryPartner=OAuth2PasswordBearer(tokenUrl="/partner/login")

