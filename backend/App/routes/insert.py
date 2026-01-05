
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import APIRouter,Depends
from pydantic import BaseModel

from App.logs.logs import logger
from App.db.models import User,Todolist,get_db
from App.Auth_folder.Auth import user_from_cookie


class taskdata(BaseModel):
    task_name:str

router=APIRouter()

@router.post("/user/add_task")
async def addtask(tasks:taskdata,userinfo:dict=Depends(user_from_cookie),db:AsyncSession=Depends(get_db)):
    username=userinfo["username"]
    task_name=tasks.task_name
    res=await db.execute(select(User).filter_by(username=username))
    userdata=res.scalars().first()
    if not userdata:
        logger.info("no such user")
        return{"msg":"no such user"}
    userid=userdata.userid
    task=Todolist(task_name=task_name,userid=userdata.userid,task_status="incomplete")
    db.add(task)
    await db.commit()
    await db.refresh(task)
    logger.info(f"task added succesfully userid:{userid} task_id:{task.taskid}")
    return{"msg":"task added successfully","task_id":task.taskid}

