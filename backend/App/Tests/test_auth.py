from App.Auth_folder import *
import pytest

username="kiku"












async def test_getuser(db_session):
    userdata=await get_user("kiku",db_session)
    assert userdata is None or userdata.username=="kiku"

@pytest.mark.parametrize(
        "username,password,username",[
            ("test_user","test_password","test_user"),
            ("test_user","wrong_pwd",False),
            ("no_user","test_password",False),
        ]
)

async def test_authenticate(db_session,fake_token):
    userdata = await authenticate(db_session,"kiku","kiku")