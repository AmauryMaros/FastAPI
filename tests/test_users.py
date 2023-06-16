from app import schemas
from .database import session, client
import pytest
from jose import jwt
from app.config import settings

@pytest.fixture
def test_user(client):
    user_data = {"email":"username1@gmail.com",
                 "password":"pass1"}
    res = client.post("/users/", json = user_data)
    assert res.status_code == 201
    new_user = res.json()
    new_user["password"] = user_data["password"]
    return new_user

def test_create_user(client):
    res = client.post("/users/",json = {"email":"test@gmail.com", "password":"test"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "test@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data = {"username": test_user["email"],             # in the request form, email is switched by username
                                        "password": test_user["password"]})    
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, settings.secret_key, algorithms=[settings.algorithm] )
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200

""" def test_root(client):
    res = client.get("/")
    print(res.json().get("message"))           # print(res) return Response 200 with pytest. To get the string "hello wordl", print(res.json())
    assert res.json().get("message") == "Hello World"
    assert res.status_code == 200 """