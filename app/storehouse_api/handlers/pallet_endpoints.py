import uuid

from fastapi import APIRouter, HTTPException

from app.services.storehouse_services import PalletService
from app.storehouse_api.models import PalletModel, CreatePalletModel, UpdatePalletModel, MultiResponseModel

pallet_router = APIRouter()


@pallet_router.post("/", response_model=PalletModel)
async def create_pallet(pallet: CreatePalletModel):
    pallet_service = PalletService()
    return await pallet_service.create(pallet)


@pallet_router.get("/", response_model=MultiResponseModel[PalletModel])
async def get_pallets(offset: int, limit: int, search: str = None, supplier_id: str = None):
    pallet_service = PalletService()
    pallets, count = await pallet_service.get_all(offset=offset, limit=limit, search=search, supplier_search=supplier_id)

    response = MultiResponseModel[PalletModel](data=pallets, count=count)
    return response


@pallet_router.get("/{pallet_id}", response_model=PalletModel)
async def retrieve(pallet_id: uuid.UUID):
    pallet_service = PalletService()
    pallet = await pallet_service.retrieve(pallet_id)

    if not pallet:
        raise HTTPException(
            status_code=400, detail=f"pallet with this id {pallet_id} does not exists"
        )

    return pallet


@pallet_router.put("/{pallet_id}", response_model=PalletModel)
async def update_pallet(pallet_id: uuid.UUID, pallet_data: UpdatePalletModel):
    pallet_service = PalletService()
    updated = await pallet_service.update(pallet_id, pallet_data)

    if not updated:
        raise HTTPException(
            status_code=400, detail=f"pallet with this id {pallet_id} does not exists"
        )

    return updated


@pallet_router.delete("/{pallet_id}")
async def delete_pallet(pallet_id: uuid.UUID):
    print('at deleting')
    pallet_service = PalletService()
    res = await pallet_service.delete(pallet_id)
    print('deleting res', res)

    if not res:
        raise HTTPException(
            status_code=400, detail=f"pallet with this id {pallet_id} does not exists"
        )

    return {"success": True}
