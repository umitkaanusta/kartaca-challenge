from fastapi.testclient import TestClient

from api.routes import app, mock_db

client = TestClient(app)


def test_get_kitties():
    resp = client.get("/api/kitties")
    assert resp.status_code == 200
    assert resp.json() == mock_db


def test_get_kitties_by_id():
    resp = client.get("/api/kitties?kitty_id=1")
    assert resp.status_code == 200
    assert resp.json() == mock_db[1]
    resp_err = client.get("/api/kitties?kitty_id=5")
    assert resp_err.status_code == 404
    assert resp_err.json() == {"detail": "Kitty not found, try with another Id"}


if __name__ == '__main__':
    test_get_kitties()
    test_get_kitties_by_id()
