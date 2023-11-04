import uuid
from abc import ABC, abstractmethod
from typing import List, Iterable

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from app.db.models import User, Pallet, Location, Supplier
from app.storehouse_api.models import SupplierModel, UserUpdate, UpdatePalletModel


class AbstractAsyncRepo(ABC):
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    @abstractmethod
    async def create(self, *args, **kwargs):
        pass


class UserRepo(AbstractAsyncRepo):
    async def create(self, **fields) -> User:
        new_user = User(**fields)
        self.db_session.add(new_user)
        await self.db_session.flush()
        return new_user

    async def retrieve(self, user_id: uuid.UUID):
        query = select(User).filter(User.id == user_id)

        res = await self.db_session.execute(query)
        user = res.scalars().one_or_none()
        return user

    async def update(self, user_id: uuid.UUID, user_data: UserUpdate):
        user = await self.retrieve(user_id=user_id)

        if not user:
            return None

        for var, value in (user_data.model_dump(exclude_unset=True)).items():
            setattr(user, var, value)

        await self.db_session.flush()
        return user

    async def delete(self, user_id: uuid.UUID):
        user = await self.retrieve(user_id)

        if not user:
            return None

        await self.db_session.delete(user)

        return True


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

    async def get_all(self) -> Iterable[Pallet]:
        query = select(Pallet).options(
            selectinload(Pallet.supplier), selectinload(Pallet.user)
        )
        res = await self.db_session.execute(query)
        result = res.scalars().all()

        return result

    async def retrieve(self, pallet_id: uuid.UUID):
        query = (select(Pallet).filter(Pallet.id == pallet_id).
                 options(selectinload(Pallet.location), selectinload(Pallet.supplier)))

        res = await self.db_session.execute(query)
        pallet = res.scalars().one_or_none()

        return pallet

    async def update(self, pallet_id: uuid.UUID, pallet_data: UpdatePalletModel):
        pallet = await self.retrieve(pallet_id)

        if not pallet:
            return None

        for var, value in pallet_data.model_dump(exclude_unset=True).items():
            setattr(pallet, var, value)

        await self.db_session.flush()

        return pallet

    async def delete(self, pallet_id: uuid.UUID):
        pallet = await self.retrieve(pallet_id)

        if not pallet:
            return None

        await self.db_session.delete(pallet)

        return True


class SupplierRepo(AbstractAsyncRepo):
    async def create(self, name: str) -> Supplier:
        new_supplier = Supplier(name=name)
        self.db_session.add(new_supplier)
        await self.db_session.flush()
        return new_supplier

    async def retrieve(self, supplier_uuid: uuid.UUID) -> SupplierModel:
        supplier = await self.db_session.get(Supplier, supplier_uuid)
        return SupplierModel(id=supplier.id, name=supplier.name, pallets=None)
