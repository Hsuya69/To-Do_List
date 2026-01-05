
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import APIRouter,HTTPException,Depends
from pydantic import BaseModel

from App.Auth_folder.Auth import user_from_cookie
from App.logs.logs import logger
from App.db.models import get_db,User,Todolist



router=APIRouter()
class taskdata(BaseModel):
    taskid:int

@router.delete("/user")
async def deleteuser(db:AsyncSession=Depends(get_db),userdata:dict=Depends(user_from_cookie)):
    username=userdata["username"]
    try:
        stmt=await db.execute(select(User).filter_by(username=username))
        res=stmt.scalar_one_or_none()
        if not res:
            logger.error("status:401 , no such user")
            raise HTTPException(status_code=401,detail="no such user")
        await db.delete(res)
        logger.info(f"status:200 , user id{res.userid} deleted")
        await db.commit()
    except Exception as e:
        logger.critical(f"status:500 ,oops!! server error, reason{Exception}-{e}")
        raise HTTPException(status_code=500,detail="oops!! server error")

@router.delete("/user/delete_task")
async def deletetask(taskinfo:taskdata,userdata:dict=Depends(user_from_cookie),db:AsyncSession=Depends(get_db)):
    username=userdata["username"]
    try:
        stmt=select(User).filter_by(username=username)
        res=await db.execute(stmt)
        userinfo=res.scalar_one_or_none()
        if not userinfo:
            logger.error("status:401 , no such user")
            raise HTTPException(status_code=401,detail="no such user")
        stmt=await db.execute(select(Todolist).filter_by(userid=userinfo.userid,taskid=taskinfo.taskid))
        task=stmt.scalar_one_or_none()
        if not task:
            logger.error("status:401 , no such task")
            raise HTTPException(status_code=401,detail="no such task")
        await db.delete(task)
        logger.info(f"status:200 , user id:{userinfo.userid} task id:{task.taskid} deleted")
        await db.commit()

    except Exception as e:
        db.rollback()
        logger.critical(f"status:500 ,oops!! server error, reason{Exception}-{e}")
        raise HTTPException(status_code=500,detail="server error")


        

            
    