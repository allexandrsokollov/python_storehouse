import uuid
from typing import Union, List

from pydantic import BaseModel, EmailStr


class UserModel(BaseModel):
    id: uuid.UUID
    name: str
    surname: str
    email: EmailStr


class CreateUser(BaseModel):
    name: str
    surname: str
    email: EmailStr


class UserUpdate(BaseModel):
    name: str | None
    surname: str | None
    email: EmailStr | None


class CreatePalletModel(BaseModel):
    title: str
    description: str
    supplier_id: uuid.UUID
    location_id: uuid.UUID | None
    user_id: uuid.UUID | None


class PalletModel(CreatePalletModel):
    id: uuid.UUID
    location: Union["LocationModel", None]
    supplier: "SupplierModel"
    user: UserModel | None


class UpdatePalletModel(BaseModel):
    title: str | None
    description: str | None
    supplier_id: uuid.UUID | None
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


class SupplierWithPallets(SupplierModel):
    pallets: List[PalletModel] | None


class CreateSupplierModel(BaseModel):
    name: str
