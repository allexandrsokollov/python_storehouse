import uuid
from abc import ABC, abstractmethod
from typing import List, Optional, Union

from fastapi import FastAPI, APIRouter
from pydantic import BaseModel, EmailStr
from sqlalchemy import Column, UUID, String, Boolean, Integer, UniqueConstraint, ForeignKey
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base, mapped_column, Mapped, relationship

import config

engine = create_async_engine(config.DATABASE_URL, future=True, echo=True)


async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str]
    surname: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    pallets: Mapped[List["Pallet"]] = relationship(back_populates="user")


class Location(Base):
    __tablename__ = 'location'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    shelving: Mapped[int] = mapped_column(nullable=False)
    floor: Mapped[int] = mapped_column(nullable=False)
    position: Mapped[int] = mapped_column(nullable=False)
    pallet: Mapped[Optional["Pallet"]] = relationship(back_populates="location")

    __table_args__ = (UniqueConstraint("shelving", "floor", "position", name="unique position constraint"),)


class Pallet(Base):
    __tablename__ = 'pallet'

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    title: Mapped[str] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=False)
    location: Mapped[Optional["Location"]] = relationship(back_populates="pallet")
    location_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("location.id"))
    supplier: Mapped["Supplier"] = relationship(back_populates='pallets')
    supplier_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("supplier.id"))
    user: Mapped["User"] = relationship(back_populates="pallets")
    user_id: Mapped[Optional[uuid.UUID]] = mapped_column(ForeignKey("user.id"))


class Supplier(Base):
    __tablename__ = "supplier"

    id: Mapped[uuid.UUID] = mapped_column(UUID, primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(nullable=False)
    pallets: Mapped[List["Pallet"]] = relationship(back_populates="supplier")


class AbstractAsyncRepo(ABC):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    @abstractmethod
    async def create(self, *args, **kwargs):
        pass


class UserRepo(AbstractAsyncRepo):
    async def create(self, name: str, surname: str, email: str) -> User:
        new_user = User(
            name=name, surname=surname, email=email
        )
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user


class LocationRepo(AbstractAsyncRepo):

    async def create(self, shelving: int, floor: int, position: int, pallet: Pallet | None) -> Location:
        new_location = Location(shelving=shelving, floor=floor, position=position, pallet=pallet)
        self.db_session.add(new_location)
        await self.db_session.flush()
        return new_location


class PalletRepo(AbstractAsyncRepo):

    async def create(self, title: str, description: str,
                     location_id: uuid.UUID | None, supplier_id: uuid.UUID | None) -> Pallet:
        new_pallet = Pallet(title=title, description=description, location_id=location_id, supplier_id=supplier_id)
        self.db_session.add(new_pallet)
        await self.db_session.flush()
        return new_pallet


class SupplierRepo(AbstractAsyncRepo):

    async def create(self, name: str) -> Supplier:
        new_supplier = Supplier(name=name)
        self.db_session.add(new_supplier)
        await self.db_session.flush()
        return new_supplier


class UserModel(BaseModel):
    id: uuid.UUID
    name: str
    surname: str
    email: EmailStr
    # pallets: List["PalletModel"]


class CreateUser(BaseModel):
    name: str
    surname: str
    email: EmailStr
    # pallets: List["PalletModel"]


class PalletModel(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    location: Union["LocationModel", None]
    supplier_id: uuid.UUID
    user: UserModel | None


class CreatePalletModel(BaseModel):
    title: str
    description: str
    supplier_id: uuid.UUID
    location_id: uuid.UUID | None
    user_id: uuid.UUID | None


class LocationModel(BaseModel):
    id: uuid.UUID | None
    shelving: int
    floor: int
    position: int
    pallet: PalletModel | None


class SupplierModel(BaseModel):
    id: uuid.UUID | None
    name: str
    pallets: List[PalletModel] | None


class CreateSupplierModel(BaseModel):
    name: str


class UserServie:

    async def create(self, data: CreateUser):
        async with async_session() as session:
            async with session.begin():
                user_repo = UserRepo(session)
                user = await user_repo.create(name=data.name, surname=data.surname, email=data.email)
                return UserModel(id=user.id, name=user.name, surname=user.surname, email=user.email)


class SupplierService:

    async def create(self, data: CreateSupplierModel):
        async with async_session() as session:
            async with session.begin():
                supplier_repo = SupplierRepo(session)
                supplier = await supplier_repo.create(name=data.name)
                return SupplierModel(id=supplier.id, name=supplier.name, pallets=None)


class PalletService:
    async def create(self, pallet: CreatePalletModel) -> PalletModel:
        async with async_session() as session:
            async with session.begin():
                pallet_repo = PalletRepo(session)
                new_pallet = await pallet_repo.create(title=pallet.title, description=pallet.description,
                                                      location_id=None, supplier_id=pallet.supplier_id)
                return PalletModel(id=new_pallet.id, title=new_pallet.title, description=new_pallet.description,
                                   supplier_id=new_pallet.supplier_id, location=None,
                                   user=None)


app = FastAPI(title="storehouse")

user_router = APIRouter()
supplier_router = APIRouter()
pallet_router = APIRouter()


@user_router.post("/", response_model=UserModel)
async def create_user(user: CreateUser):
    user_service = UserServie()
    return await user_service.create(user)


@supplier_router.post("/", response_model=SupplierModel)
async def create_supplier(supplier: CreateSupplierModel):
    supplier_service = SupplierService()
    return await supplier_service.create(supplier)


@pallet_router.post("/", response_model=PalletModel)
async def create_pallet(pallet: CreatePalletModel):
    pallet_service = PalletService()
    return await pallet_service.create(pallet)


@app.get("/")
async def root():
    return {"data": 'Main page'}


main_api_router = APIRouter()
main_api_router.include_router(user_router, prefix="/users", tags=["user"])
main_api_router.include_router(supplier_router, prefix="/suppliers", tags=["supplier"])
main_api_router.include_router(pallet_router, prefix="/pallet", tags=["pallet"])

app.include_router(main_api_router)

