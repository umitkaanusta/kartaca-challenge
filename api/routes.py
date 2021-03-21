from fastapi import FastAPI, Query, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from api.utils import random_wait, kitty_to_json
from api import crud, models
from api.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/api/kitties")
def get_kitties(
    kitty_id: Optional[int] = Query(
        default=None,
        title="Kitty Id",
        description="Get an individual kitty by its Id. Get all kitties if id is not specified."
    ),
    db: Session = Depends(get_db)
):
    if kitty_id is None:
        kitties = [kitty_to_json(k) for k in crud.read_kitties(db)]
        return random_wait(JSONResponse(status_code=200, content=kitties))
    kitty = kitty_to_json(crud.read_kitty(db, kitty_id))
    if kitty is None:
        raise HTTPException(status_code=404, detail="Kitty not found, try with another Id")
    return random_wait(JSONResponse(status_code=200, content=kitty))


@app.post("/api/add-kitty")
def add_kitty(
    name: str = Query(
        ...,
        title="Name",
        description="Name of the kitty",
        min_length=1,
        max_length=150,
    ),
    db: Session = Depends(get_db)
):
    new = kitty_to_json(crud.create_kitty(db, name))
    return random_wait(JSONResponse(status_code=200, content=new))


@app.put("/api/update-kitty")
def update_kitty(
    kitty_id: int = Query(
        ...,
        title="Kitty Id",
        description="Get the kitty to be updated, by its Id"
    ),
    new_name: Optional[str] = Query(
        default=None,
        title="New Name",
        description="New name of the kitty",
        min_length=1,
        max_length=150
    ),
    db: Session = Depends(get_db)
):
    if new_name is None:
        return random_wait(JSONResponse(status_code=200))
    if crud.read_kitty(db, kitty_id) is None:
        raise HTTPException(status_code=404, detail="Kitty not found, try with another Id")
    updated = kitty_to_json(crud.update_kitty(db, kitty_id, new_name))
    return random_wait(JSONResponse(status_code=200, content=updated))


@app.delete("/api/delete-kitty")
def delete_kitty(
    kitty_id: int = Query(
        ...,
        title="Kitty Id",
        description="Get the kitty to be deleted"
    ),
    db: Session = Depends(get_db)
):
    if crud.read_kitty(db, kitty_id) is None:
        raise HTTPException(status_code=404, detail="Kitty not found, try with another Id")
    deleted = kitty_to_json(crud.delete_kitty(db, kitty_id))
    return random_wait(JSONResponse(status_code=200, content=deleted))
