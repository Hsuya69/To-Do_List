
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from fastapi import APIRouter,Depends,HTTPException
from pydantic import BaseModel

from App.logs.logs import logger
from App.db.models import get_db,User,Todolist
from App.Auth_folder.Auth import user_from_cookie

    

router=APIRouter()
class tasksinfo(BaseModel):
    taskid:int

class names(BaseModel):
    newname:str

@router.patch("/user/update_name")
async def updatename(newname:names,db:AsyncSession=Depends(get_db),userdata:dict=Depends(user_from_cookie)):
    username=userdata["username"]
    stmt=await db.execute(select(User).filter_by(username=username))
    res=stmt.scalar_one_or_none()
    res.username=newname.newname
    await db.commit()


@router.patch("/user/update_task_name")
async def update_task_name(taskid:tasksinfo,
                     newtaskname:names,
                     userdata:dict=Depends(user_from_cookie),
                     db:AsyncSession=Depends(get_db)):
    username=userdata["username"]
    try:
        stmt=db.execute(select(User).filter_by(username=username))
        res=stmt.scalar_one_or_none()
        if not res:
            raise HTTPException(status_code=401)
        stmt=await db.execute(select(User).join(Todolist).filter_by(userid=res.userid,taskid=taskid.taskid))
        taskname=stmt.scalar_one_or_none()
        taskname=newtaskname.task_name
        await db.commit()
    except Exception as e:
        raise HTTPException(status_code=500)
        


@router.post("/user/update_task")
async def update_task_status(userinfo:tasksinfo,db:AsyncSession=Depends(get_db),userdata:dict=Depends(user_from_cookie)):
    username=userdata["username"]
    stmt=select(User).filter_by(username=username)
    res1=await db.execute(stmt)
    rows=res1.scalar_one_or_none()
    if not rows:
        logger.error("status:401 , no such user")
        raise HTTPException(status_code=401,detail="now such user")
    stmt=select(Todolist).filter_by(userid=rows.userid,taskid=userinfo.taskid)
    res2=await db.execute(stmt)
    rows=res2.scalar_one_or_none()
    if rows.task_status=="incomplete":
        rows.task_status="complete"
        await db.commit()
    else:
        rows.task_status="incomplete"
        await db.commit()

@router.get("/user")
async def show_tasks(
                     userdata:dict=Depends(user_from_cookie),
                     db:AsyncSession=Depends(get_db)
                     ):
    stmt=select(User,Todolist).join(Todolist).filter(User.username==userdata["username"]).order_by("taskid")
    res=await db.execute(stmt)
    rows=res.all()
    tasks=[]
    if not rows:
        stmt=select(User).filter(User.username==userdata["username"])
        res=await db.execute(stmt)
        rows=res.scalar_one_or_none()
        if not rows:
            logger.error("status:401 , no such user")
            raise HTTPException(status_code=401,detail="user not found")
        return{"user_id":rows.userid,"name":rows.username,"tasks":tasks}
    for _,t in rows:
        tasks.append({"taskid":t.taskid,"task":t.task_name,"task_status":t.task_status})
    u,_=rows[0]
    logger.info(f"status:200 , /user ,user_id:{u.userid},name:{u.username}")
    return{"user_id":u.userid,"name":u.username,"tasks":tasks}
