import uuid
from typing import List

from fastapi import APIRouter, HTTPException

from app.services.storehouse_services import UserServie, SupplierService
from app.storehouse_api.models import (
    CreateSupplierModel,
    SupplierModel,
    UpdateSupplierModel,
)

supplier_router = APIRouter()


@supplier_router.post("/", response_model=SupplierModel)
async def create_supplier(supplier: CreateSupplierModel):
    supplier_service = SupplierService()
    return await supplier_service.create(supplier)


@supplier_router.get("/{supplier_id}", response_model=SupplierModel)
async def get_supplier(supplier_id: uuid.UUID):
    supplier_service = SupplierService()
    supplier = await supplier_service.get(supplier_id)

    if not supplier:
        raise HTTPException(
            status_code=400,
            detail=f"supplier with this id {supplier_id} does not exists",
        )

    return supplier


@supplier_router.get("/", response_model=List[SupplierModel])
async def get_all_suppliers():
    supplier_service = SupplierService()
    suppliers = await supplier_service.get_all()

    return suppliers


@supplier_router.put("/{supplier_id}", response_model=SupplierModel)
async def update_supplier(supplier_id: uuid.UUID, supplier_data: UpdateSupplierModel):
    supplier_service = SupplierService()
    updates = await supplier_service.update(supplier_id, supplier_data)

    if not updates:
        raise HTTPException(
            status_code=400,
            detail=f"supplier with this id {supplier_id} does not exists",
        )

    return updates


@supplier_router.delete("/{supplier_id}")
async def update_supplier(supplier_id: uuid.UUID):
    supplier_service = SupplierService()
    res = await supplier_service.delete(supplier_id)

    if not res:
        raise HTTPException(
            status_code=400,
            detail=f"supplier with this id {supplier_id} does not exists",
        )

    return {"success": True}
