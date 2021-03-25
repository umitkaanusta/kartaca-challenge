from sqlalchemy import Column, Integer, String

from api.database import Base


class Kitty(Base):
    __tablename__ = "kitties"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)


class KittyLog(Base):
    __tablename__ = "kittylogs"
    id = Column(Integer, primary_key=True, index=True)
    method = Column(String)
    response_time = Column(Integer)
    timestamp = Column(Integer)
