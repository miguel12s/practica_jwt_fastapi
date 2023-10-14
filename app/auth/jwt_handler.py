# this file is responsible for signing, encoding,decoding and returning jwts

import time
import jwt
from decouple import config

JWT_SECRET=config("secret")
JWT_ALGORITHM=config("algorithm") 

#fucntion returns the generated tokens (JWTs)
def token_response(token:str):
    return {
        "access token":token
    }
def signJwt(userId:str):
    payload = {
        "userId":userId,
        "expiry":time.time()+600
    }
    token=jwt.encode(payload,JWT_SECRET,algorithm=JWT_ALGORITHM)

    return token_response(token)

def decodeJWT(token:str):
    try:
        decode_token=jwt.decode(token,JWT_SECRET,algorithms=JWT_ALGORITHM)
        return decode_token if decode_token['expires'] >=time.time() else None
    except:
        return {}