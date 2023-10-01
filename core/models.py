import uuid
from sqlalchemy import Column, String, DateTime, Boolean, UUID
from sqlalchemy.orm import declarative_base
from datetime import datetime

CoreBase = declarative_base()


class User(CoreBase):
    __tablename__ = "user"

    id = Column(UUID, primary_key=True, unique=True, default=uuid.uuid4)
    name = Column(String)
    email = Column(String, unique=True)
    password = Column(String)
    create_data = Column(DateTime, default=datetime.utcnow)
    is_admin = Column(Boolean, default=False)
