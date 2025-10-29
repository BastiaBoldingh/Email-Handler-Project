from datetime import datetime, timedelta
from jose import JWTError, jwt
from werkzeug.security import generate_password_hash, check_password_hash
from app.core.config import settings
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.core.config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")

def hash_password(password):
    return generate_password_hash(password, method="pbkdf2:sha256:600000", salt_length=16)

def verify_password_hash(password, hashed_password):
    return check_password_hash(hashed_password, password)

#JWT settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS265"
ACCESS_TOKEN_EXPIRE = 60 * 24

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now() + expires_delta
    else:
        expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token")
        return username
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token or expired")
