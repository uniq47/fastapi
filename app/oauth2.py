from fastapi import HTTPException, status, Depends
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import database, models, schemas
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
from app import schemas


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

SECRET_KEY = "3456"
ALGORITHM = "HS256"
Access_Token_Expire_min = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=Access_Token_Expire_min)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exceptions):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exceptions
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exceptions
    return token_data


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exceptions = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                           detail="Could not validate credentials ", headers={"WWW-Authenticate": "Bearer"})
    token = verify_access_token(token, credentials_exceptions)
    user = db.query(models.User).filter(models.User.id) == token.id
    return user
