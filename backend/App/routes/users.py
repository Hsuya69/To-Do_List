
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import APIRouter,HTTPException,status,Depends
from fastapi.responses import Response
from pydantic import BaseModel
from datetime import timedelta

from App.logs.logs import logger
from App.db.models import User,get_db
from App.Auth_folder.Auth import pwd_context,Token,authenticate,create_access_token,token_expiring_time


router=APIRouter()

class usermodel(BaseModel):
    username:str
    password:str
@router.post("/signup")
async def signup(
    userdata:usermodel,
    db:AsyncSession=Depends(get_db)):
    
    
    result = await db.execute(select(User).filter(User.username==userdata.username))
    existing_user = result.scalars().first()
    if existing_user:
        logger.warning("status:400, username already exists")
        raise HTTPException(status_code=400,detail="username already exists")

    try:
        hashed_password=pwd_context.hash(userdata.password)
        userinfo=User(username=userdata.username,hashed_pwd=hashed_password)
        db.add(userinfo)
        await db.commit()
        logger.info(f"added user with userid:{User.userid}")
    except Exception as e:
        await db.rollback()
        logger.error("status:400 , signup error")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="signup error")
    logger.info("status:200 ,account created successfully")
    return {"message":"account created successfully!!"}
    
    
@router.post("/login",response_model=Token)
async def login(res:Response,
                userdata:usermodel,
                db:AsyncSession=Depends(get_db)):
    user=await authenticate(db,userdata.username,userdata.password)
    if not user:
        logger.error("status:400 , incorrect username or password")
        raise HTTPException(status_code=401,detail="incorrect username or password")
    
    access_token=create_access_token(data={"sub":user.username},expire_delta=timedelta(minutes=token_expiring_time))
    
    #cookie
    res.set_cookie(key="access_token",
                   value=access_token,
                   httponly=True,
                   samesite="none",
                   secure = True,
                   path="/")
    logger.info(f"cookie created: token{access_token}")
    return {"access_token":access_token,
            "token_type":"bearer"}


