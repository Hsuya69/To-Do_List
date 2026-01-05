from App.logs.logs import logger
from fastapi import Depends,HTTPException,status,Cookie
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError,jwt,ExpiredSignatureError
from passlib.context import CryptContext
from pydantic import BaseModel
from datetime import datetime,timezone,timedelta
import os
from App.db.models import User as UserModel,get_db
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from dotenv import load_dotenv


load_dotenv()

secret_key=os.getenv("secret_key")
algo="HS256"
token_expiring_time=30

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")
oauth2scheme=OAuth2PasswordBearer(tokenUrl="/login")

class UserData(BaseModel):
    username:str 
    disabled:bool |None=None

class Token(BaseModel):
    access_token:str
    token_type:str

class Token_data(BaseModel):
    user_name:str | None=None

class UserinDB(BaseModel):
    hashed_pwd:str
    username:str
    disabled : bool = False


async def get_user(username:str,db:AsyncSession=Depends(get_db)):
    result = await db.execute(select(UserModel).filter(UserModel.username==username))
    User_result=result.scalar_one_or_none()
    if User_result is None:
        return None
    return UserinDB(username=User_result.username,
                    hashed_pwd=User_result.hashed_pwd)

async def authenticate(db:AsyncSession,username:str,pwd:str):
    user= await get_user(username,db)
    if not user:
        return False
    if not pwd_context.verify(pwd,user.hashed_pwd):
        return False
    return user

def create_access_token(data:dict,expire_delta:timedelta):
    to_encode=data.copy()
    if expire_delta:
        expire=datetime.now(timezone.utc)+expire_delta
    else:
        expire=datetime.now(timezone.utc)+timedelta(token_expiring_time)
    to_encode.update({"exp":expire})
    encoded_jwt=jwt.encode(to_encode,secret_key,algo)
    return encoded_jwt

async def get_current_user(token:str=Depends(oauth2scheme) ,db:AsyncSession=Depends(get_db)):
    credential_error=HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                   detail="could not validate credential",
                                   headers={"WWW-Authenticate":"bearer"})
    
    try:
        payload=jwt.decode(token,secret_key,algorithms=[algo])
        username=payload.get("sub")
        if not username:
            return credential_error
        tokendata=Token_data(user_name=username)

    except JWTError:
        raise credential_error
    
    user= await get_user(username=tokendata.user_name,db=db)
    if not user:
        raise credential_error
    return user

def get_current_active_user(current_user:UserinDB=Depends(get_current_user)):
    if current_user.disabled:
        return HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="inactive user")
    return current_user

async def user_from_cookie(access_token:str|None=Cookie(default=None)):
    if access_token is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="not authenticated")
    try:
        payload=jwt.decode(access_token,secret_key,algorithms=[algo])
        username:str=payload.get("sub")
        if not username:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid token")
        return {"username":username}
    except ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="invalid tooken")
        


