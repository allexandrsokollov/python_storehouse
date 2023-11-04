import uuid
from typing import List

from fastapi import APIRouter, HTTPException

from app.services.storehouse_services import UserServie, SupplierService, PalletService
from app.storehouse_api.models import (
    UserModel,
    CreateUser,
    CreateSupplierModel,
    SupplierModel,
    PalletModel,
    CreatePalletModel,
    UserUpdate,
)

user_router = APIRouter()
supplier_router = APIRouter()
pallet_router = APIRouter()


@user_router.post("/", response_model=UserModel)
async def create_user(user: CreateUser):
    user_service = UserServie()
    return await user_service.create(user)


@user_router.get("/{user_id}", response_model=UserModel)
async def get_user(user_id: uuid.UUID):
    user_service = UserServie()
    user = await user_service.retrieve(user_id)

    if not user:
        raise HTTPException(
            status_code=400, detail=f"User with this id: {user_id} does not exists"
        )

    return user


@user_router.put("{user_id}", response_model=UserModel)
async def update_user(user_id: uuid.UUID, user_data: UserUpdate):
    user_service = UserServie()
    user = await user_service.update(user_id, user_data)

    if not user:
        raise HTTPException(
            status_code=400, detail=f"User with this id: {user_id} does not exists"
        )

    return user


@user_router.delete("user_id")
async def delete_user(user_id: uuid.UUID):
    user_service = UserServie()
    res = await user_service.delete(user_id)

    if not res:
        raise HTTPException(
            status_code=400, detail=f"User with this id: {user_id} does not exists"
        )

    return {"success": True}


@supplier_router.post("/", response_model=SupplierModel)
async def create_supplier(supplier: CreateSupplierModel):
    supplier_service = SupplierService()
    return await supplier_service.create(supplier)


@supplier_router.get("/{supplier_id}", response_model=SupplierModel)
async def create_supplier(supplier_id: uuid.UUID):
    supplier_service = SupplierService()
    return await supplier_service.get(supplier_id)


@pallet_router.post("/", response_model=PalletModel)
async def create_pallet(pallet: CreatePalletModel):
    pallet_service = PalletService()
    return await pallet_service.create(pallet)


@pallet_router.get("/", response_model=List[PalletModel])
async def get_pallets():
    pallet_service = PalletService()
    pallets = await pallet_service.get_all()
    return pallets
