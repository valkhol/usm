from typing import Union
from uuid import UUID
from fastapi import APIRouter, Depends, Path
from starlette import status

from app.dependencies import (authenticate, post_repository_dependency,
                              strip_repository_dependency)
from app.dto.responses import DetailResponse, ResponseGenerator
from app.dto.strip import StripOutlist
from app.repositories.mongo.mongo_client import MongoRepositoryException

router = APIRouter(
    # prefix='/v1/strip', tags=['strip'], dependencies=[Depends(authenticate)]
    prefix='/v1/strip', tags=['strip'],
)


@router.patch(
    '/{id}/watched',
    status_code=status.HTTP_200_OK,
    response_model=Union[None, DetailResponse],
)
async def set_watched(
    id: UUID = Path(),
    repo=Depends(strip_repository_dependency),
):
    try:
        await repo.set_watched(str(id))
    except MongoRepositoryException as e:
        return ResponseGenerator.db_connection_error_response(str(e))


@router.get(
    '/{user}',
    status_code=status.HTTP_200_OK,
    response_model=StripOutlist,
)
async def get_strip(
    user: UUID = Path(),
    repo=Depends(post_repository_dependency),
):
    try:
        posts = await repo.get_strip_of_posts(str(user))
        return {'strip': posts}
    except MongoRepositoryException as e:
        return ResponseGenerator.db_connection_error_response(str(e))
