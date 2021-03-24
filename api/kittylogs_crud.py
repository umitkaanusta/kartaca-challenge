from sqlalchemy.orm import Session
from api import models


def create_log(db: Session, method: str, response_time: int, timestamp: int):
    db_log = models.KittyLog()
    db_log.method = method
    db_log.response_time = response_time
    db_log.timestamp = timestamp
    db.add(db_log)
    db.commit()
    db.refresh(db_log)


def read_logs(db: Session):
    return db.query(models.KittyLog).all()
