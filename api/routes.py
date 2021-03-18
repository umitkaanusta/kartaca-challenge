from fastapi import FastAPI, Query, HTTPException, Response
from typing import Optional

from api.utils import random_wait

app = FastAPI()


mock_db = [
    {
        "id": 0,
        "name": "mock"
    },
    {
        "id": 1,
        "name": "tabby"
    }
]


@app.get("/api/kitties")
def get_kitties(
    kitty_id: Optional[int] = Query(
        default=None,
        title="Kitty Id",
        description="Get an individual kitty by its Id. Get all kitties if not specified."
    )
):
    if kitty_id is None:
        return random_wait(Response(status_code=200, content=str(mock_db)))
    try:
        return random_wait(Response(status_code=200, content=str(mock_db[kitty_id])))
    except IndexError:
        return HTTPException(
            status_code=404,
            detail="Kitty not found, try with another Id"
        )


@app.post("/api/add-kitty")
def add_kitty(
    name: str = Query(
        ...,
        title="Name",
        description="Name of the kitty",
        min_length=1,
        max_length=150,
    )
):
    new_id = len(mock_db)
    new = {
        "id": new_id,
        "name": name
    }
    mock_db.append(new)
    return random_wait(Response(status_code=200, content=str(new)))


@app.put("/api/update-kitty")
def update_kitty(
    kitty_id: int = Query(
        ...,
        title="Kitty Id",
        description="Get the kitty to be updated, by its Id"
    ),
    new_name: str = Query(
        default=None,
        title="New Name",
        description="New name of the kitty",
        min_length=1,
        max_length=150
    )
):
    try:
        kitty = mock_db[kitty_id]
    except IndexError:
        return HTTPException(
            status_code=404,
            detail="Kitty not found, try with another Id"
        )
    if new_name is None:
        return random_wait(Response(status_code=200))
    new = {
        "id": kitty_id,
        "name": kitty["name"] if new_name is None else new_name,
    }
    mock_db[kitty_id] = new
    return random_wait(Response(status_code=200, content=str(new)))


@app.delete("/api/delete-kitty")
def delete_kitty(
    kitty_id: int = Query(
        ...,
        title="Kitty Id",
        description="Get the kitty to be deleted"
    ),
):
    try:
        deleted = mock_db.pop(kitty_id)
    except IndexError:
        return HTTPException(
            status_code=404,
            detail="Kitty not found, try with another Id"
        )
    # rearrange Ids
    for idx, d in enumerate(mock_db):
        d["id"] = idx
    return random_wait(Response(status_code=200, content=str(deleted)))
