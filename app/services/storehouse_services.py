import uuid

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app import config
from app.db.repos import UserRepo, SupplierRepo, PalletRepo
from app.storehouse_api.models import CreateUser, UserModel, CreateSupplierModel, SupplierModel, CreatePalletModel, \
    PalletModel

engine = create_async_engine(config.DATABASE_URL, future=True, echo=True, pool_size=5, max_overflow=10)


async_session = async_sessionmaker(engine)


class UserServie:

    async def create(self, data: CreateUser):
        async with async_session() as session:
            async with session.begin():
                user_repo = UserRepo(session)
                user = await user_repo.create(name=data.name, surname=data.surname, email=data.email)
                return UserModel(id=user.id, name=user.name, surname=user.surname, email=user.email)


class SupplierService:

    async def create(self, data: CreateSupplierModel):
        async with async_session() as session:
            async with session.begin():
                supplier_repo = SupplierRepo(session)
                supplier = await supplier_repo.create(name=data.name)
                return SupplierModel(id=supplier.id, name=supplier.name, pallets=None)

    async def get(self, supplier_uuid: uuid.UUID):
        async with async_session() as session:
            async with session.begin():
                supplier_repo = SupplierRepo(session)
                supplier = await supplier_repo.retrieve(supplier_uuid)
                return SupplierModel(id=supplier.id, name=supplier.name, pallets=None)


class PalletService:
    async def create(self, pallet: CreatePalletModel) -> PalletModel:
        async with async_session() as session:
            async with session.begin():
                pallet_repo = PalletRepo(session)
                new_pallet = await pallet_repo.create(title=pallet.title, description=pallet.description,
                                                      location_id=None, supplier_id=pallet.supplier_id)
                return PalletModel(id=new_pallet.id, title=new_pallet.title, description=new_pallet.description,
                                   supplier_id=new_pallet.supplier_id, location=None,
                                   user=None)

