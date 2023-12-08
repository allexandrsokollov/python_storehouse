import uuid
from typing import List

from fastapi import APIRouter, HTTPException

from app.services.storehouse_services import LocationService
from app.storehouse_api.models import DetailLocationModel, CreateLocationModel, MultiResponseModel

location_router = APIRouter()


@location_router.post("/", response_model=DetailLocationModel)
async def create_supplier(supplier: CreateLocationModel):
    supplier_service = LocationService()
    return await supplier_service.create(supplier)


@location_router.get("/{location_id}", response_model=DetailLocationModel)
async def get_supplier(location_id: uuid.UUID):
    supplier_service = LocationService()
    supplier = await supplier_service.retrieve(location_id)

    if not supplier:
        raise HTTPException(
            status_code=400,
            detail=f"supplier with this id {location_id} does not exists",
        )

    return supplier


@location_router.get(
    "/", response_model=MultiResponseModel[DetailLocationModel]
)
async def get_all_suppliers(offset: int, limit: int):
    supplier_service = LocationService()
    suppliers, count = await supplier_service.get_all(offset=offset, limit=limit)

    response = MultiResponseModel[DetailLocationModel](data=suppliers, count=count)

    return response


@location_router.put("/{location_id}", response_model=DetailLocationModel)
async def update_supplier(location_id: uuid.UUID, supplier_data: CreateLocationModel):
    supplier_service = LocationService()
    updates = await supplier_service.update(location_id, supplier_data)

    if not updates:
        raise HTTPException(
            status_code=400,
            detail=f"supplier with this id {location_id} does not exists",
        )

    return updates


@location_router.delete("/{location_id}")
async def update_supplier(location_id: uuid.UUID):
    supplier_service = LocationService()
    res = await supplier_service.delete(location_id)

    if not res:
        raise HTTPException(
            status_code=400,
            detail=f"supplier with this id {location_id} does not exists",
        )

    return {"success": True}
