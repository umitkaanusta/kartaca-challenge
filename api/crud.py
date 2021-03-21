from sqlalchemy.orm import Session
from api import models


def create_kitty(db: Session, name: str):
    db_kitty = models.Kitty()
    db_kitty.name = name
    db.add(db_kitty)
    db.commit()
    db.refresh(db_kitty)
    return read_kitty(db, db_kitty.id)


def read_kitty(db: Session, kitty_id: int):
    return db.query(models.Kitty).filter(models.Kitty.id == kitty_id).first()


def read_kitties(db: Session):
    return db.query(models.Kitty).all()


def update_kitty(db: Session, kitty_id: int, new_name: str):
    (db.query(models.Kitty)
        .filter(models.Kitty.id == kitty_id)
        .update({models.Kitty.name: new_name}))
    db.commit()
    return read_kitty(db, kitty_id)


def delete_kitty(db: Session, kitty_id: int):
    deleted = read_kitty(db, kitty_id)
    db.query(models.Kitty).filter(models.Kitty.id == kitty_id).delete()
    db.commit()
    return deleted
