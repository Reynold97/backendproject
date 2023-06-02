from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "85a81eaaf5dfeae613fde5e7822933c1dde26d5518201f79cf936d67c8098921"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_acces_token(data: dict):
    to_encode = data.copy()
    expire =  datetime.now() + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY,algorithm= ALGORITHM)
    return encoded_jwt