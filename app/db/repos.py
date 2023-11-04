import uuid
from abc import ABC, abstractmethod

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User, Pallet, Location, Supplier
from app.storehouse_api.models import SupplierModel


class AbstractAsyncRepo(ABC):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    @abstractmethod
    async def create(self, *args, **kwargs):
        pass


class UserRepo(AbstractAsyncRepo):
    async def create(self, name: str, surname: str, email: str) -> User:
        new_user = User(name=name, surname=surname, email=email)
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user


class LocationRepo(AbstractAsyncRepo):
    async def create(
        self, shelving: int, floor: int, position: int, pallet: Pallet | None
    ) -> Location:
        new_location = Location(
            shelving=shelving, floor=floor, position=position, pallet=pallet
        )
        self.db_session.add(new_location)
        await self.db_session.flush()
        return new_location


class PalletRepo(AbstractAsyncRepo):
    async def create(
        self,
        title: str,
        description: str,
        location_id: uuid.UUID | None,
        supplier_id: uuid.UUID | None,
    ) -> Pallet:
        new_pallet = Pallet(
            title=title,
            description=description,
            location_id=location_id,
            supplier_id=supplier_id,
        )
        self.db_session.add(new_pallet)
        await self.db_session.flush()
        return new_pallet


class SupplierRepo(AbstractAsyncRepo):
    async def create(self, name: str) -> Supplier:
        new_supplier = Supplier(name=name)
        self.db_session.add(new_supplier)
        await self.db_session.flush()
        return new_supplier

    async def retrieve(self, supplier_uuid: uuid.UUID) -> SupplierModel:
        supplier = await self.db_session.get(Supplier, supplier_uuid)
        return SupplierModel(id=supplier.id, name=supplier.name, pallets=None)
