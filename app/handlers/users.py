from typing import Union
from fastapi import APIRouter, Depends, Path, Query
from starlette import status

from app.dependencies import (authenticate, pagination_params,
                              user_repository_dependency)
from app.dto.responses import (DetailResponse, ResponseGenerator,
                               ValidationErrorResponse)
from app.dto.user import UserIn, UserOut, UserOutList
from app.models.user import User
from app.repositories.mongo.country_repo import CountryRepositoryMongo
from app.repositories.mongo.mongo_client import MongoRepositoryException

router = APIRouter(prefix='/v1/users', tags=['users'])


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=Union[UserOut, ValidationErrorResponse],
)
async def create_user(
    data: UserIn = Depends(UserIn.form_create_user),
    repo=Depends(user_repository_dependency),
):
    if isinstance(data, ValidationErrorResponse):
        return ResponseGenerator().validation_error_response(data)
    try:
        country = await CountryRepositoryMongo().get_by_id(data.country)
        if country is None:
            return ResponseGenerator().no_instance_found_error_response(
                f'country not found: {data.country}'
            )

        user: User = User(
            email=data.email,
            password=data.password,
            name=data.name,
            last_name=data.last_name,
            birth_date=data.birth_date,
            country=data.country,
            photo_file=None if data.user_photo is None else data.user_photo.file,
        )
        await repo.create_update(user)
        return await repo.get_by_id(user.id)
    except MongoRepositoryException as e:
        return ResponseGenerator.db_connection_error_response(str(e))


@router.get(
    '/{id}',
    status_code=status.HTTP_200_OK,
    response_model=Union[DetailResponse, UserOut],
    # dependencies=[Depends(authenticate)],
)
async def get_user(id: str = Path(), repo=Depends(user_repository_dependency)):
    try:
        user = await repo.get_by_id(id)
    except MongoRepositoryException as e:
        return ResponseGenerator.db_connection_error_response(str(e))

    if user is None:
        return ResponseGenerator.no_instance_found_error_response(f'user not found: {id}')
    return user


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=Union[UserOut, ValidationErrorResponse, None],
    dependencies=[Depends(authenticate)],
)
async def get_user_by_param(
    email: str | None = None,
    slug: str | None = None,
    repo=Depends(user_repository_dependency),
):
    if email is None and slug is None:
        return ResponseGenerator.custom_validation_error_response(
            'No email or slug provided'
        )

    if email is not None:
        params = {'email': email}
    else:
        params = {'slug': slug}

    try:
        user = await repo.get_by_param(params)
    except MongoRepositoryException as e:
        return ResponseGenerator.db_connection_error_response(str(e))

    if user is None:
        return None

    return user


@router.patch(
    '/{id}',
    status_code=status.HTTP_200_OK,
    response_model=Union[UserOut, ValidationErrorResponse, DetailResponse],
    # dependencies=[Depends(authenticate)],
)
async def update_user(
    data: UserIn = Depends(UserIn.form_update_user),
    repo=Depends(user_repository_dependency),
):
    if isinstance(data, ValidationErrorResponse):
        return ResponseGenerator.validation_error_response(data)

    try:
        user = await repo.get_by_id(data.id)
        if user is None:
            return ResponseGenerator.no_instance_found_error_response(
                f'user not found: {data.id}'
            )

        update_user: User = User(
            id=data.id,
            email=data.email if data.email is not None else user.email,
            password=data.password if data.password is not None else user.password,
            name=data.name if data.name is not None else user.name,
            last_name=data.last_name if data.last_name is not None else user.last_name,
            birth_date=data.birth_date
            if data.birth_date is not None
            else user.birth_date,
            country=data.country if data.country is not None else user.country,
            photo_file=None if data.user_photo is None else data.user_photo.file,
            created_at=user.created_at,
        )
        await repo.create_update(update_user)
        return await repo.get_by_id(data.id)

    except MongoRepositoryException as e:
        return ResponseGenerator.db_connection_error_response(str(e))


@router.delete(
    '/{id}',
    status_code=status.HTTP_202_ACCEPTED,
    # dependencies=[Depends(authenticate)],
)
async def delete_user(id: str = Path(), repo=Depends(user_repository_dependency)):
    try:
        user = await repo.get_by_id(id)
        if user is None:
            return ResponseGenerator.no_instance_found_error_response(
                f'user not found: {id}'
            )
        await repo.delete(id)
    except MongoRepositoryException as e:
        return ResponseGenerator.db_connection_error_response(str(e))


@router.get(
    '/search/slug',
    status_code=status.HTTP_200_OK,
    response_model=Union[UserOutList | DetailResponse],
    # dependencies=[Depends(authenticate)],
)
async def search_user(
    search: str = Query(..., min_length=3),
    pagination=Depends(pagination_params),
    repo=Depends(user_repository_dependency),
):
    try:
        users = await repo.get_by_string(
            search=search, skip=pagination.skip, limit=pagination.limit
        )
    except MongoRepositoryException as e:
        return ResponseGenerator.db_connection_error_response(str(e))
    return {'users': users}
