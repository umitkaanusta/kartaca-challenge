from fastapi import FastAPI, Query, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from loguru import logger
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import time

from api.utils import random_wait, kitty_to_json
from api import crud, models
from api.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

logger.add("kitties.log", format="{message}", level="INFO")

app = FastAPI()


@app.middleware("http")
def log(request: Request, call_next):
    req_time = time.time()
    resp = random_wait(call_next(request))
    resp_time = time.time() - req_time
    if "/api/" in str(request.url):
        # only log requests coming to the kitties api
        logger.info(f"{request.method}, {int(resp_time * 1000)}, {int(req_time)}")
    return resp


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
        return JSONResponse(status_code=200, content=kitties)
    kitty = kitty_to_json(crud.read_kitty(db, kitty_id))
    if kitty is None:
        raise HTTPException(status_code=404, detail="Kitty not found, try with another Id")
    return JSONResponse(status_code=200, content=kitty)


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
    return JSONResponse(status_code=200, content=new)


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
        return JSONResponse(status_code=200)
    if crud.read_kitty(db, kitty_id) is None:
        raise HTTPException(status_code=404, detail="Kitty not found, try with another Id")
    updated = kitty_to_json(crud.update_kitty(db, kitty_id, new_name))
    return JSONResponse(status_code=200, content=updated)


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
    return JSONResponse(status_code=200, content=deleted)
