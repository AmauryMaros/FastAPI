from app import schemas
from .database import session, client
import pytest
from jose import jwt
from app.config import settings

def test_create_user(client):
    res = client.post("/users/",json = {"email":"test@gmail.com", "password":"test"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "test@gmail.com"
    assert res.status_code == 201

def test_login_user(client, test_user):
    res = client.post("/login", data = {"username": test_user["email"],             # in the request form, email is switched by username
                                        "password": test_user["password"]})    
    login_res = schemas.Token(**res.json())
    payload = jwt.decode(login_res.access_token, 
                         settings.secret_key, 
                         algorithms=[settings.algorithm])
    
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_res.token_type == "bearer"
    assert res.status_code == 200


@pytest.mark.parametrize("email, password, status_code", 
                         [("wrongemail@gmail.com","test",403),
                          ("test@gmail.com", "wrongpass", 403),
                          ("wrongmail@gmail.com","wrongpass", 403),
                          (None, "test", 422),
                          ("test@gmail.com", None, 422)])

def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post("/login", data = {"username": email,
                                        "password": password})
    
    assert res.status_code == status_code

""" def test_root(client):
    res = client.get("/")
    print(res.json().get("message"))           # print(res) return Response 200 with pytest. To get the string "hello wordl", print(res.json())
    assert res.json().get("message") == "Hello World"
    assert res.status_code == 200 """