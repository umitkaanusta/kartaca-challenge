from sqlalchemy import Column, Integer, String

from api.database import Base


class Kitty(Base):
    __tablename__ = "kitties"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
