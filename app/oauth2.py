from jose import jwt, JWTError
from datetime import datetime, timedelta


SECRET_KEY = "3456"
ALGORITHM = "HS256"
Access_Token_Expire_min = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=Access_Token_Expire_min)
    print(expire)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
