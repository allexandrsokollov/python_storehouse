import uuid

from fastapi import APIRouter, HTTPException

from app.services.storehouse_services import UserServie
from app.storehouse_api.models import UserModel, CreateUser, UserUpdate

user_router = APIRouter()


@user_router.post("/", response_model=UserModel)
async def create_user(user: CreateUser):
    user_service = UserServie()
    return await user_service.create(user)


@user_router.get("/{user_id}", response_model=UserModel)
async def get_user(user_id: uuid.UUID):
    user_service = UserServie()
    user = await user_service.retrieve(user_id)

    if not user:
        raise HTTPException(
            status_code=400, detail=f"User with this id: {user_id} does not exists"
        )

    return user


@user_router.put("{user_id}", response_model=UserModel)
async def update_user(user_id: uuid.UUID, user_data: UserUpdate):
    user_service = UserServie()
    user = await user_service.update(user_id, user_data)

    if not user:
        raise HTTPException(
            status_code=400, detail=f"User with this id: {user_id} does not exists"
        )

    return user


@user_router.delete("user_id")
async def delete_user(user_id: uuid.UUID):
    user_service = UserServie()
    res = await user_service.delete(user_id)

    if not res:
        raise HTTPException(
            status_code=400, detail=f"User with this id: {user_id} does not exists"
        )

    return {"success": True}
