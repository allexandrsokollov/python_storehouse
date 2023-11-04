import uuid

from fastapi import APIRouter

from app.services.storehouse_services import UserServie, SupplierService
from app.storehouse_api.models import (
    CreateSupplierModel,
    SupplierModel,
)

supplier_router = APIRouter()


@supplier_router.post("/", response_model=SupplierModel)
async def create_supplier(supplier: CreateSupplierModel):
    supplier_service = SupplierService()
    return await supplier_service.create(supplier)


@supplier_router.get("/{supplier_id}", response_model=SupplierModel)
async def create_supplier(supplier_id: uuid.UUID):
    supplier_service = SupplierService()
    return await supplier_service.get(supplier_id)
