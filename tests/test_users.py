from app import schemas
from .database import session, client

def test_root(client):
    res = client.get("/")
    print(res.json().get("message"))           # print(res) return Response 200 with pytest. To get the string "hello wordl", print(res.json())
    assert res.json().get("message") == "Hello World"
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users/",json = {"email":"test@gmail.com", "password":"test"})

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "test@gmail.com"
    assert res.status_code == 201

def test_login_user(client):
    res = client.post("/login", data = {"username":"test@gmail.com", "password":"test"})    # in the request form, email is switched by username
    assert res.status_code == 200
