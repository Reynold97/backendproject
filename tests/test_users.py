from tests.database import client, session

from app import schemas



def test_create_user(client):
    res = client.post(
        "/users/", json={"email": "reynold@gmail.com", "password": "password123"})

    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "reynold@gmail.com"
    assert res.status_code == 201

def test_login_user(client):
    res = client.post(
        "/login", data={"username": "reynold@gmail.com", "password": "password123"})
    
    assert res.status_code == 200