import uuid

from fastapi import APIRouter

from app.services.storehouse_services import UserServie, SupplierService, PalletService
from app.storehouse_api.models import UserModel, CreateUser, CreateSupplierModel, SupplierModel, PalletModel, \
    CreatePalletModel

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


@supplier_router.get("/{supplier_id}", response_model=SupplierModel)
async def create_supplier(supplier_id: uuid.UUID):
    supplier_service = SupplierService()
    return await supplier_service.get(supplier_id)


@pallet_router.post("/", response_model=PalletModel)
async def create_pallet(pallet: CreatePalletModel):
    pallet_service = PalletService()
    return await pallet_service.create(pallet)
