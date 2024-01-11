import uuid
from typing import Union, List, TypeVar, Generic

from pydantic import BaseModel, EmailStr

T = TypeVar("T", bound=BaseModel)


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
    name: Union[str, None]
    surname: Union[str, None]
    email: Union[EmailStr, None]


class CreatePalletModel(BaseModel):
    title: str
    description: str
    supplier_id: uuid.UUID
    location_id: uuid.UUID | None
    user_id: uuid.UUID | None


class PalletModelMain(CreatePalletModel):
    id: uuid.UUID
    location: Union["LocationModel", None]


class PalletModel(CreatePalletModel):
    id: uuid.UUID
    location: Union["LocationModel", None]
    supplier: Union["SupplierModel", None]
    user: UserModel | None


class UpdatePalletModel(BaseModel):
    title: str | None
    description: str | None
    supplier_id: uuid.UUID | None
    location_id: uuid.UUID | None
    user_id: uuid.UUID | None


class CreateLocationModel(BaseModel):
    shelving: int
    floor: int
    position: int


class LocationModel(CreateLocationModel):
    id: uuid.UUID


class DetailLocationModel(CreateLocationModel):
    id: uuid.UUID
    pallet: Union["PalletModel", None]


class CreateSupplierModel(BaseModel):
    name: str


class SupplierModel(CreateSupplierModel):
    id: uuid.UUID | None


class UpdateSupplierModel(BaseModel):
    name: str


class SupplierWithPallets(SupplierModel):
    pallets: List[PalletModel] | None


class MultiResponseModel(BaseModel, Generic[T]):
    data: List[T]
    count: int


class Statistics(BaseModel):
    total_suppliers: int
    suppliers_with_pallets: int
    total_locations: int
    locations_with_pallets: int
    total_pallets: int
    pallets_in_locations: int
    pallets_with_suppliers: int
    pallets_with_users: int
