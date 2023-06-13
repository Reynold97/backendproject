from jose import JWTError, jwt
from datetime import datetime, timedelta

from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

from sqlalchemy.orm import Session

from app import schemas, database, models

SECRET_KEY = "85a81eaaf5dfeae613fde5e7822933c1dde26d5518201f79cf936d67c8098921"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

oauth2_scheme = OAuth2PasswordBearer(tokenUrl= "login")


def create_acces_token(data: dict):
    to_encode = data.copy()
    expire =  datetime.utcnow() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY,algorithm= ALGORITHM)
    return encoded_jwt

def verify_acces_token(token: str, credentials_exceptions):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
        id = payload.get("user_id")
        if id is None:
            raise credentials_exceptions
        token_data = schemas.TokenData(id = id)
    except JWTError:
        raise credentials_exceptions
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code= status.HTTP_401_UNAUTHORIZED, detail= "Invalid credentials",
                                          headers= {"WWW-Authenticate": "Bearer"})
    token = verify_acces_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
