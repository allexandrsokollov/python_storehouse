import uuid
from typing import Union, List

from pydantic import BaseModel, EmailStr


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
