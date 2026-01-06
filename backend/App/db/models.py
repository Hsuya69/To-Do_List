
from sqlalchemy.orm import declarative_base,relationship
from sqlalchemy import Integer,String,Column,ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine,async_sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()
engine=create_async_engine(os.getenv("SUPABASE_DB_URL"),
                           echo=True,
                           connect_args={"ssl":True})
sessionlocal = async_sessionmaker(bind=engine)
Base =declarative_base()

class User(Base):
    __tablename__="users"
    userid = Column(Integer,primary_key=True)
    username = Column(String(40))
    hashed_pwd =Column(String(100),unique=True,nullable=False)
    todos = relationship("Todolist",back_populates="user")

class Todolist(Base):
    __tablename__="todolist"
    taskid = Column(Integer,primary_key=True)
    userid = Column(Integer,ForeignKey("users.userid"),nullable=False)
    task_name = Column(String(200))
    task_status = Column(String(10))
    user_state = Column(String(30),default="login")
    user = relationship("User",back_populates="todos")

async def get_db():
    db=sessionlocal()
    try:
        yield db
    finally:
       await db.close()

