import uuid
from typing import List, Optional

from sqlalchemy import UUID, UniqueConstraint, ForeignKey
from sqlalchemy.orm import declarative_base, mapped_column, Mapped, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "user"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str]
    surname: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    pallets: Mapped[List["Pallet"]] = relationship(back_populates="user")


class Location(Base):
    __tablename__ = "location"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    shelving: Mapped[int] = mapped_column(nullable=False)
    floor: Mapped[int] = mapped_column(nullable=False)
    position: Mapped[int] = mapped_column(nullable=False)
    pallet: Mapped[Optional["Pallet"]] = relationship(back_populates="location")

    __table_args__ = (
        UniqueConstraint(
            "shelving", "floor", "position", name="unique position constraint"
        ),
    )


class Pallet(Base):
    __tablename__ = "pallet"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[Optional["Location"]] = relationship(back_populates="pallet")
    location_id: Mapped[uuid.UUID | None] = mapped_column(ForeignKey("location.id"))
    supplier: Mapped["Supplier"] = relationship(back_populates="pallets")
    supplier_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("supplier.id"))
    user: Mapped["User"] = relationship(back_populates="pallets")
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("user.id"))


class Supplier(Base):
    __tablename__ = "supplier"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(nullable=False)
    pallets: Mapped[List["Pallet"]] = relationship(back_populates="supplier")
