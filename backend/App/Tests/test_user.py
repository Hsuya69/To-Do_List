from App.routes.users import login,signup
from httpx import AsyncClient,ASGITransport
import pytest
from App.main import app

base_url="http://test"

@pytest.mark.parametrize(
    "username,password,expected",[
        ("test_user","test_pwd",{"message":"username already exists"}),
        ("test_user","test_pwd",{"message":"account created successfully!!"}),
    ],
)
async def test_signup(db_session,username,password,expected):
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport,base_url=base_url) as ac:
        response = await ac.post("/signup",json={"username":username,"password":password})
        assert response.json()["detail"]==expected 

