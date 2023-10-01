import uuid

from sqlalchemy import Column, UUID, Integer, UniqueConstraint
from sqlalchemy.orm import declarative_base

AppBase = declarative_base()


class Location(AppBase):
    __tablename__ = "location"
    id = Column(UUID, primary_key=True, index=True, unique=True, default=uuid.uuid4)
    shelving = Column(Integer)
    row = Column(Integer)
    column = Column(Integer)
    __table_args__ = (UniqueConstraint('shelving', 'row', 'column'),)
