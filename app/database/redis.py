from uuid import UUID

from redis.asyncio import Redis 

from app.config import Db_settings 


_token_blacklist=Redis(
    host= Db_settings.REDIS_HOST,
    port = Db_settings.REDIS_PORT,
    db= 0
)

_shipment_verification_code = Redis(
        host= Db_settings.REDIS_HOST,
         port = Db_settings.REDIS_PORT,
         db= 1

)


async def add_jti_to_blacklist(jti:str):
    await _token_blacklist.set(jti,"blacklisted")


async def is_jti_blacklisted(jti:str):
    return await _token_blacklist.exists(jti)

async def get_verification_code(id: UUID,code:int):
    await _shipment_verification_code.set(str(id),code)

async def is_verification_code(code:int):
    return await _shipment_verification_code.get(code)
