from typing import Union
from uuid import UUID
from fastapi import APIRouter, Depends, Path
from starlette import status

from app.dependencies import (authenticate, follower_repository_dependency,
                              verify_users_exist_form, verify_users_exist_path)
from app.dto.follower import FollowerIn, FollowerOut, FollowsOutList
from app.dto.responses import (DetailResponse, ResponseGenerator,
                               ValidationErrorResponse)
from app.models.followers import Follower
from app.repositories.mongo.mongo_client import MongoRepositoryException

# router = APIRouter(
#     prefix='/v1/followers', tags=['followers'], dependencies=[Depends(authenticate)]
# )

router = APIRouter(
    prefix='/v1/followers', tags=['followers']
)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=Union[FollowerOut, ValidationErrorResponse, DetailResponse],
    dependencies=[Depends(verify_users_exist_form)],
)
async def create_follower(
    data: FollowerIn | ValidationErrorResponse = Depends(FollowerIn.form_create_follower),
    repo=Depends(follower_repository_dependency),
):
    if isinstance(data, ValidationErrorResponse):
        return ResponseGenerator.validation_error_response(data)
    if data.id == data.follow:
        return ResponseGenerator.custom_validation_error_response(
            'user and follower can not be equal'
        )

    follower = Follower(str(data.id), str(data.follow))
    try:
        result_follower = await repo.create(follower)
    except MongoRepositoryException as e:
        return ResponseGenerator.db_connection_error_response(str(e))
    return result_follower


@router.get(
    '/{id}',
    status_code=status.HTTP_200_OK,
    response_model=Union[FollowsOutList, DetailResponse],
)
async def get_follows(
    id: str = Path(...),
    repo=Depends(follower_repository_dependency),
):
    try:
        follows = await repo.get_by_id(id)
    except MongoRepositoryException as e:
        return ResponseGenerator.db_connection_error_response(str(e))
    return {'follows': follows}


@router.delete(
    '/{id}/{follow}',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=Union[ValidationErrorResponse, DetailResponse, None],
    dependencies=[Depends(verify_users_exist_path)],
)
async def delete_follower(
    id: UUID = Path(),
    follow: UUID = Path(),
    repo=Depends(follower_repository_dependency),
):
    record = await repo.get_follow_by_ids(str(id), str(follow))
    if record is None:
        return ResponseGenerator.no_instance_found_error_response(
            'follow record not found'
        )
    try:
        await repo.delete(str(id), str(follow))
    except MongoRepositoryException as e:
        return ResponseGenerator.db_connection_error_response(str(e))
