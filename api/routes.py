from fastapi import FastAPI, BackgroundTasks, Query, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from loguru import logger
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import time
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

from api.utils import random_wait, kitty_to_json, last_log, process_message
from api import crud, kittylogs_crud, models
from api.database import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

logger.add("kitties.log", format="{message}", level="INFO")

app = FastAPI()


async def write_to_kafka():
    # Async job that instantaneously writes logs to Kafka
    producer = AIOKafkaProducer(bootstrap_servers=["kafka:9093"])
    await producer.start()
    message = bytes(last_log(), "utf-8")
    try:
        await producer.send_and_wait("kittylogs", message)
    finally:
        await producer.stop()


async def kafka_msg_to_db(db):
    consumer = AIOKafkaConsumer(
        "kittylogs",
        group_id="kittygroup",
        bootstrap_servers=["kafka:9093"]
    )
    await consumer.start()
    try:
        async for msg in consumer:
            method, resp_time, timestamp = process_message(msg.value)
            kittylogs_crud.create_log(db, method, resp_time, timestamp)
    finally:
        await consumer.stop()


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
    bg: BackgroundTasks,
    kitty_id: Optional[int] = Query(
        default=None,
        title="Kitty Id",
        description="Get an individual kitty by its Id. Get all kitties if id is not specified."
    ),
    db: Session = Depends(get_db),
):
    bg.add_task(write_to_kafka)
    bg.add_task(kafka_msg_to_db, db)
    if kitty_id is None:
        kitties = [kitty_to_json(k) for k in crud.read_kitties(db)]
        return JSONResponse(status_code=200, content=kitties)
    kitty = kitty_to_json(crud.read_kitty(db, kitty_id))
    if kitty is None:
        raise HTTPException(status_code=404, detail="Kitty not found, try with another Id")
    return JSONResponse(status_code=200, content=kitty)


@app.post("/api/add-kitty")
def add_kitty(
    bg: BackgroundTasks,
    name: str = Query(
        ...,
        title="Name",
        description="Name of the kitty",
        min_length=1,
        max_length=150,
    ),
    db: Session = Depends(get_db)
):
    bg.add_task(write_to_kafka)
    bg.add_task(kafka_msg_to_db, db)
    new = kitty_to_json(crud.create_kitty(db, name))
    return JSONResponse(status_code=200, content=new)


@app.put("/api/update-kitty")
def update_kitty(
    bg: BackgroundTasks,
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
    bg.add_task(write_to_kafka)
    bg.add_task(kafka_msg_to_db, db)
    if new_name is None:
        return JSONResponse(status_code=200)
    if crud.read_kitty(db, kitty_id) is None:
        raise HTTPException(status_code=404, detail="Kitty not found, try with another Id")
    updated = kitty_to_json(crud.update_kitty(db, kitty_id, new_name))
    return JSONResponse(status_code=200, content=updated)


@app.delete("/api/delete-kitty")
def delete_kitty(
    bg: BackgroundTasks,
    kitty_id: int = Query(
        ...,
        title="Kitty Id",
        description="Get the kitty to be deleted"
    ),
    db: Session = Depends(get_db)
):
    bg.add_task(write_to_kafka)
    bg.add_task(kafka_msg_to_db, db)
    if crud.read_kitty(db, kitty_id) is None:
        raise HTTPException(status_code=404, detail="Kitty not found, try with another Id")
    deleted = kitty_to_json(crud.delete_kitty(db, kitty_id))
    return JSONResponse(status_code=200, content=deleted)


@app.get("/logs")
def get_logs(
    db: Session = Depends(get_db),
):
    # endpoint for e2e tests
    content = kittylogs_crud.read_logs(db)
    content = [{"method": log_.method,
                "response_time": log_.response_time,
                "timestamp": log_.timestamp} for log_ in content]
    return JSONResponse(status_code=200, content=content)
