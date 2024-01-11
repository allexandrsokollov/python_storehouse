import uuid
from select import select

from fastapi import Request
from fastapi.templating import Jinja2Templates
from fastapi import APIRouter
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select


from pathlib import Path

from app.db.models import Supplier, Location, Pallet
from app.services.storehouse_services import LocationService, async_session
from app.storehouse_api.handlers.pallet_endpoints import get_pallets, retrieve
from app.storehouse_api.handlers.supplier_endpoints import get_all_suppliers
from app.storehouse_api.models import MultiResponseModel, LocationModel, Statistics

page_router = APIRouter()
BASE_DIR = Path(__file__).resolve().parent

templates = Jinja2Templates(directory=str(Path(BASE_DIR, 'templates')))


@page_router.get('/')
async def index(request: Request):
    page = int(request.query_params.get("page", 1))
    per_page = int(request.query_params.get("per_page", 30))
    offset = (page - 1) * per_page

    data = await get_pallets(offset, per_page)

    return templates.TemplateResponse("index.html", {"request": request, "data": data.data, "count": data.count})


@page_router.get('/pallets/{pallet_id}')
async def index1(request: Request, pallet_id: uuid.UUID):
    data = await retrieve(pallet_id)

    return templates.TemplateResponse("pallet.html", {"request": request, "item": data})


@page_router.get('/pallets/update/{pallet_id}')
async def index2(request: Request, pallet_id: uuid.UUID):
    data = await retrieve(pallet_id)
    sup = await get_all_suppliers(0, 9999999)

    return templates.TemplateResponse("update_pallet.html", {"request": request, "pallet": data,
                                                             "suppliers": sup.data})


@page_router.get('/pallets/create/')
async def index3(request: Request):

    return templates.TemplateResponse("create_pallet.html", {"request": request})


@page_router.get('/locations')
async def index3(request: Request):

    return templates.TemplateResponse("locations.html", {"request": request})


@page_router.get('/suppliers')
async def index3(request: Request):

    return templates.TemplateResponse("suppliers.html", {"request": request})

@page_router.get('/suppliers/update/{id}')
async def index3(request: Request, id: uuid.UUID):

    return templates.TemplateResponse("update_supplier.html", {"request": request})


@page_router.get('/suppliers/create')
async def index3(request: Request):

    return templates.TemplateResponse("create_supplier.html", {"request": request})




@page_router.get(
    "/empty_locations", response_model=MultiResponseModel[LocationModel]
)
async def get_all_suppliers2():
    supplier_service = LocationService()
    suppliers, count = await supplier_service.get_all_empty(offset=0, limit=9999)

    response = MultiResponseModel[LocationModel](data=suppliers, count=count)

    return response



@page_router.get("/get_statistics", response_model=Statistics)
async def get_statistics():
    async with async_session() as session:  # Предполагается, что async_session - async context manager
        # Получаем общее количество поставщиков
        total_suppliers = await session.scalar(select(func.count(Supplier.id)))

        # Получаем количество поставщиков, у которых есть паллеты
        suppliers_with_pallets = await session.scalar(
            select(func.count(Supplier.id)).where(Supplier.pallets.any())
        )

        # Получаем общее количество местоположений
        total_locations = await session.scalar(select(func.count(Location.id)))

        # Получаем количество местоположений, на которых есть паллеты
        locations_with_pallets = await session.scalar(
            select(func.count(Location.id)).where(Location.pallet.has())
        )

        # Получаем общее количество паллет
        total_pallets = await session.scalar(select(func.count(Pallet.id)))

        # Получаем количество паллет, которые находятся на местоположениях
        pallets_in_locations = await session.scalar(
            select(func.count(Pallet.id)).where(Pallet.location_id.isnot(None))
        )

        # Получаем количество паллет, которые принадлежат поставщикам
        pallets_with_suppliers = await session.scalar(
            select(func.count(Pallet.id)).where(Pallet.supplier_id.isnot(None))
        )

        # Получаем количество паллет, которые связаны с пользователями
        pallets_with_users = await session.scalar(
            select(func.count(Pallet.id)).where(Pallet.user_id.isnot(None))
        )

        # Создаем экземпляр модели статистики
        statistics = Statistics(
            total_suppliers=total_suppliers,
            suppliers_with_pallets=suppliers_with_pallets,
            total_locations=total_locations,
            locations_with_pallets=locations_with_pallets,
            total_pallets=total_pallets,
            pallets_in_locations=pallets_in_locations,
            pallets_with_suppliers=pallets_with_suppliers,
            pallets_with_users=pallets_with_users
        )

        return statistics




@page_router.get(
    "/stats", response_model=MultiResponseModel[LocationModel]
)
async def index5(request: Request):

    return templates.TemplateResponse("stats.html", {"request": request})
