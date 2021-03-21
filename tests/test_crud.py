from sqlalchemy.orm import Session

from api import crud, models
from tests import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)


def test_create_kitty():
    db: Session = SessionLocal()
    kitty = crud.create_kitty(db, "testkitty")
    assert isinstance(kitty, models.Kitty)
    assert kitty.name == "testkitty"
    db.close()


def test_read_kitties():
    db: Session = SessionLocal()
    kitties = crud.read_kitties(db)
    assert len(kitties) == 1
    assert kitties[0] is not None
    kitty = kitties[0]
    assert isinstance(kitty, models.Kitty)
    assert kitty.name == "testkitty"
    db.close()


def test_read_kitty():
    db: Session = SessionLocal()
    kitty_id = crud.read_kitties(db)[0].id
    kitty = crud.read_kitty(db, kitty_id)
    assert isinstance(kitty, models.Kitty)
    assert kitty.name == "testkitty"
    assert kitty.id == kitty_id
    db.close()


def test_update_kitty():
    db: Session = SessionLocal()
    kitty_id = crud.read_kitties(db)[0].id
    updated = crud.update_kitty(db, kitty_id, "testmeow")
    assert isinstance(updated, models.Kitty)
    assert updated.name == "testmeow"
    assert updated.id == kitty_id
    db.close()


def test_delete_kitty():
    db: Session = SessionLocal()
    kitty_id = crud.read_kitties(db)[0].id
    deleted = crud.delete_kitty(db, kitty_id)
    assert isinstance(deleted, models.Kitty)
    assert deleted.name == "testmeow"
    assert deleted.id == kitty_id
    assert len(crud.read_kitties(db)) == 0
    db.close()


if __name__ == '__main__':
    test_create_kitty()
    test_read_kitties()
    test_read_kitty()
    test_update_kitty()
    test_delete_kitty()
