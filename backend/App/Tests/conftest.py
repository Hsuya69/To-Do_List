import asyncio
import pytest
from App.Auth_folder.Auth import secret_key,algo
from App.db import base
from sqlalchemy.ext.asyncio import AsyncSession,create_async_engine
from sqlalchemy.orm import sessionmaker
from jose import jwt
from datetime import timezone,timedelta,datetime
import os
from dotenv import load_dotenv
load_dotenv()

test_db_url=os.getenv("test_db_url") 
engine = create_async_engine(test_db_url,echo=False)   
async_session=sessionmaker(engine, expire_on_commit=False,class_=AsyncSession)

@pytest.fixture(scope="session")
def event_loop():
    loop=asyncio.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def anyio():
    return "asyncio"

@pytest.fixture(scope="session")
async def test_engine():
    async with engine.begin() as conn:
        await conn.run_sync(base.metadata.drop_all)
        await conn.run_sync(base.metadata.create_all)
    yield engine
    await engine.dispose()

@pytest.fixture(scope="function")
async def db_session(test_engine):
    async with async_session() as session:
        yield session
        await session.rollback()

@pytest.fixture
def fake_token():
    data={"sub":"test_user","exp":datetime.now(timezone.utc)+timedelta(minutes=5)}
    return jwt.encode(data,secret_key,algo)