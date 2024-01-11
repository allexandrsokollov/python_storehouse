import uuid

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from app import config
from app.db.repos import UserRepo, SupplierRepo, PalletRepo, LocationRepo
from app.storehouse_api.models import (
    CreateUser,
    UserModel,
    CreateSupplierModel,
    SupplierModel,
    CreatePalletModel,
    PalletModel,
    UserUpdate,
    UpdatePalletModel,
    UpdateSupplierModel,
    CreateLocationModel,
    DetailLocationModel, LocationModel,
)

engine = create_async_engine(
    config.DATABASE_URL, future=True, echo=True, pool_size=5, max_overflow=10
)


async_session = async_sessionmaker(engine)


class UserServie:
    async def create(self, data: CreateUser):
        async with async_session() as session:
            async with session.begin():
                user_repo = UserRepo(session)
                user = await user_repo.create(
                    name=data.name, surname=data.surname, email=data.email
                )
                return UserModel(
                    id=user.id, name=user.name, surname=user.surname, email=user.email
                )

    async def retrieve(self, user_id: uuid.UUID):
        async with async_session() as session:
            async with session.begin():
                user_repo = UserRepo(session)
                user = await user_repo.retrieve(user_id)

                if not user:
                    return None

                return UserModel.model_validate(user, from_attributes=True)

    async def update(self, user_id: uuid.UUID, user_data: UserUpdate):
        async with async_session() as session:
            async with session.begin():
                user_repo = UserRepo(session)
                user = await user_repo.update(user_id, user_data)

                if not user:
                    return None

                return UserModel.model_validate(user, from_attributes=True)

    async def delete(self, user_id: uuid.UUID):
        async with async_session() as session:
            async with session.begin():
                user_repo = UserRepo(session)
                res = await user_repo.delete(user_id=user_id)

                if not res:
                    return None

                return True


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

                if not supplier:
                    return None

                return SupplierModel(id=supplier.id, name=supplier.name, pallets=None)

    async def get_all(self, offset: int, limit: int):
        async with async_session() as session:
            async with session.begin():
                supplier_repo = SupplierRepo(session)
                suppliers, count = await supplier_repo.get_all(
                    offset=offset, limit=limit
                )

                data = []
                for row in suppliers:
                    data.append(SupplierModel.model_validate(row, from_attributes=True))

                return data, count

    async def update(self, supplier_id: uuid.UUID, supplier_data: UpdateSupplierModel):
        async with async_session() as session:
            async with session.begin():
                supplier_repo = SupplierRepo(session)

                updated = await supplier_repo.update(supplier_id, supplier_data)

                if not updated:
                    return None

                return SupplierModel.model_validate(updated, from_attributes=True)

    async def delete(self, supplier_id: uuid.UUID):
        async with async_session() as session:
            async with session.begin():
                supplier_repo = SupplierRepo(session)

                res = await supplier_repo.delete(supplier_id)

                return res


class LocationService:
    async def create(self, location: CreateLocationModel):
        async with async_session() as session:
            async with session.begin():
                location_repo = LocationRepo(session)
                new_location = await location_repo.create(**location.model_dump())

                return DetailLocationModel.model_validate(
                    new_location, from_attributes=True
                )

    async def get_all(self, offset: int, limit: int):
        async with async_session() as session:
            async with session.begin():
                location_repo = LocationRepo(session)
                locations, count = await location_repo.get_all(
                    offset=offset, limit=limit
                )

                data = []
                for row in locations:
                    data.append(
                        LocationModel.model_validate(row, from_attributes=True)
                    )

                return data, count

    async def get_all_empty(self, offset: int, limit: int):
        async with async_session() as session:
            async with session.begin():
                location_repo = LocationRepo(session)
                locations, count = await location_repo.get_all(
                    offset=offset, limit=limit
                )

                data = []
                for row in locations:
                    if row.pallet is None:
                        data.append(
                            LocationModel.model_validate(row, from_attributes=True)
                        )

                return data, count

    async def retrieve(self, location_id: uuid.UUID):
        async with async_session() as session:
            async with session.begin():
                location_repo = LocationRepo(session)
                location_data = await location_repo.retrieve(location_id)

                if not location_data:
                    return None

                return LocationModel.model_validate(
                    location_data, from_attributes=True
                )

    async def update(self, location_id: uuid.UUID, location_data: CreateLocationModel):
        async with async_session() as session:
            async with session.begin():
                location_repo = LocationRepo(session)

                updated_data = await location_repo.update(location_id, location_data)

                if not updated_data:
                    return updated_data

                return DetailLocationModel.model_validate(
                    updated_data, from_attributes=True
                )

    async def delete(self, location_id: uuid.UUID):
        async with async_session() as session:
            async with session.begin():
                location_repo = LocationRepo(session)

                res = await location_repo.delete(location_id)

                return res


class PalletService:
    async def create(self, pallet: CreatePalletModel) -> PalletModel:
        async with async_session() as session:
            async with session.begin():
                pallet_repo = PalletRepo(session)
                print(
                    pallet.title,
                    pallet.supplier_id,
                    pallet.description,
                    pallet.location_id,
                )
                new_pallet = await pallet_repo.create(
                    title=pallet.title,
                    description=pallet.description,
                    location_id=pallet.location_id,
                    supplier_id=pallet.supplier_id,
                )
                return PalletModel(
                    id=new_pallet.id,
                    title=new_pallet.title,
                    description=new_pallet.description,
                    supplier_id=new_pallet.supplier_id,
                    location_id=pallet.location_id,
                    user_id=pallet.user_id,
                    supplier=None,
                    location=None,
                    user=None,
                )

    async def get_all(self, offset: int, limit: int, search: str = None, supplier_search: str = None):
        async with async_session() as session:
            async with session.begin():
                pallet_repo = PalletRepo(session)
                pallets, count = await pallet_repo.get_all(offset=offset, limit=limit,
                                                           name_search=search, supplier_search=supplier_search)

                palett_models = [
                    PalletModel.model_validate(row, from_attributes=True)
                    for row in pallets
                ]
                return palett_models, count

    async def retrieve(self, pallet_id: uuid.UUID):
        async with async_session() as session:
            async with session.begin():
                pallet_repo = PalletRepo(session)
                pallet = await pallet_repo.retrieve(pallet_id)

                if not pallet:
                    return None

                result = PalletModel.model_validate(pallet, from_attributes=True)
                return result

    async def update(self, pallet_id: uuid.UUID, pallet_data: UpdatePalletModel):
        async with async_session() as session:
            async with session.begin():
                pallet_repo = PalletRepo(session)
                updated = await pallet_repo.update(pallet_id, pallet_data)

                if not updated:
                    return None

                return PalletModel.model_validate(updated, from_attributes=True)

    async def delete(self, pallet_id: uuid.UUID):
        async with async_session() as session:
            async with session.begin():
                pallet_repo = PalletRepo(session)

                result = await pallet_repo.delete(pallet_id)

                return result
