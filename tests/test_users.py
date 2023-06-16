from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db, Base
import pytest

# creation of a new DB dependency to do our test on a test db & not on the dev db
SQLACHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

engine = create_engine(SQLACHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit = False, autoflush = False, bind = engine)

#client = TestClient(app)
# To create & destroy test db at every test :

@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


def test_root(client):
    res = client.get("/")
    print(res.json().get("message"))           # print(res) return Response 200 with pytest. To get the string "hello wordl", print(res.json())
    assert res.json().get("message") == "Hello World"
    assert res.status_code == 200

def test_create_user(client):
    res = client.post("/users", json = {"email":"test@gmail.com", "password":"test"})

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "test@gmail.com"
    assert res.status_code == 201