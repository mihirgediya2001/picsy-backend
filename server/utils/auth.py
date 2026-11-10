from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status, Header
from fastapi.security import OAuth2AuthorizationCodeBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from server.utils.config import settings

from server import crud, schemas
from server.utils.database import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="auth", tokenUrl="token", auto_error=False
)

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "replace-me-with-openssl-rand-hex-32"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 20160


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db, username: str, password: str):
    user = crud.user.get_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str):
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    return payload


async def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if token:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            id: str = payload.get("id")
            if id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        user = crud.user.get_by_id(db, id=id)
        if user is None:
            raise credentials_exception
        return user


async def authenticate_admin(
    Authorization: str = Header(None),
):
    if Authorization != settings.ADMIN_AUTH_KEY:
        raise HTTPException(
            status_code=401,
            detail="Invalid auth key",
        )

    return True


async def get_current_active_user(
    current_user: schemas.UserBase = Depends(get_current_user),
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
