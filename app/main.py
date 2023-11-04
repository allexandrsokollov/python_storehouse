from fastapi import (
    FastAPI,
    APIRouter,
)

from app.storehouse_api.handlers.pallet_endpoints import pallet_router
from app.storehouse_api.handlers.supplier_endpoints import supplier_router
from app.storehouse_api.handlers.user_endpoints import user_router
from app.utils import fill_up

app = FastAPI(title="storehouse")


@app.get("/")
async def root():
    return {"data": 'Main page'}


@app.get("/fill_up_db")
async def root():
    await fill_up()
    return {"data": 'filling up completed successfully'}


main_api_router = APIRouter()
main_api_router.include_router(user_router, prefix="/users", tags=["user"])
main_api_router.include_router(supplier_router, prefix="/suppliers", tags=["supplier"])
main_api_router.include_router(pallet_router, prefix="/pallet", tags=["pallet"])

app.include_router(main_api_router)

