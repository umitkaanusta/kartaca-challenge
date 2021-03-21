from fastapi.testclient import TestClient

from api.routes import app, mock_db

client = TestClient(app)


"""def test_get_kitties():
    resp = client.get("/api/kitties")
    assert resp.status_code == 200
    assert resp.json() == mock_db


def test_get_kitties_by_id():
    resp = client.get("/api/kitties?kitty_id=1")
    desired = {"id": 1, "name": "tabby"}
    assert resp.status_code == 200
    assert resp.json() == mock_db[1] == desired

    resp_err = client.get("/api/kitties?kitty_id=5")
    assert resp_err.status_code == 404
    assert resp_err.json() == {"detail": "Kitty not found, try with another Id"}


def test_add_kitty():
    resp = client.post("/api/add-kitty?name=meows")
    desired = {"id": 2, "name": "meows"}
    assert resp.status_code == 200
    assert resp.json() == mock_db[2] == desired

    resp_get = client.get("/api/kitties?kitty_id=2")
    desired = {"id": 2, "name": "meows"}
    assert resp_get.status_code == 200
    assert resp_get.json() == mock_db[2] == desired


def test_update_kitty():
    resp_empty = client.put("/api/update-kitty?kitty_id=2")
    assert resp_empty.status_code == 200
    assert resp_empty.json() is None

    resp_err = client.put("/api/update-kitty?kitty_id=5")
    assert resp_err.status_code == 404
    assert resp_err.json() == {"detail": "Kitty not found, try with another Id"}

    resp = client.put("/api/update-kitty?kitty_id=2&new_name=mittens")
    desired = {"id": 2, "name": "mittens"}
    assert resp.status_code == 200
    assert resp.json() == mock_db[2] == desired

    resp_get = client.get("/api/kitties?kitty_id=2")
    desired = {"id": 2, "name": "mittens"}
    assert resp_get.status_code == 200
    assert resp_get.json() == mock_db[2] == desired


def test_delete_kitty():
    len_prev = len(mock_db)
    resp = client.delete("/api/delete-kitty?kitty_id=1")
    assert resp.status_code == 200
    assert resp.json() == {"id": 1, "name": "tabby"}
    assert len_prev - len(mock_db) == 1
    assert [rec["id"] for rec in mock_db] == [0, 1]

    resp_err = client.delete("/api/delete-kitty?kitty_id=2")
    assert resp_err.status_code == 404
    assert resp_err.json() == {"detail": "Kitty not found, try with another Id"}"""


if __name__ == '__main__':
    """test_get_kitties()
    test_get_kitties_by_id()
    test_add_kitty()
    test_update_kitty()
    test_delete_kitty()"""
