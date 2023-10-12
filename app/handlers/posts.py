from typing import Union
from fastapi import APIRouter, Depends, Path
from starlette import status

from app.dependencies import (authenticate, post_repository_dependency,
                              verify_post_content)
from app.dto.post import PostIn, PostOut
from app.dto.responses import (DetailResponse, ResponseGenerator,
                               ValidationErrorResponse)
from app.models.post import Post
from app.repositories.mongo.mongo_client import MongoRepositoryException

router = APIRouter(
    # prefix='/v1/posts', tags=['posts'], dependencies=[Depends(authenticate)]
    prefix='/v1/posts', tags=['posts']
)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=Union[PostOut, ValidationErrorResponse, DetailResponse],
    dependencies=[Depends(verify_post_content)],
)
async def create_post(
    data: PostIn = Depends(PostIn.form_create_post),
    repo=Depends(post_repository_dependency),
):
    if isinstance(data, ValidationErrorResponse):
        return ResponseGenerator.validation_error_response(data)

    post: Post = Post(
        user=str(data.user),
        topic=data.topic,
        description=data.description,
        url=data.url,
        file=None if data.file is None else data.file.file,
    )
    try:
        await repo.create_update(post)
        return await repo.get_by_id(post.id)
    except MongoRepositoryException as e:
        return ResponseGenerator.db_connection_error_response(str(e))
    except Exception as e:
        return ResponseGenerator.db_connection_error_response(str(e))


@router.get(
    '/{id}',
    status_code=status.HTTP_200_OK,
    response_model=Union[PostOut | DetailResponse],
)
async def get_by_id(id=Path(), repo=Depends(post_repository_dependency)):
    try:
        post = await repo.get_by_id(str(id))
    except MongoRepositoryException as e:
        return ResponseGenerator.db_connection_error_response(str(e))

    if post is None:
        return ResponseGenerator.no_instance_found_error_response(f'post not found: {id}')
    return post


@router.patch(
    '/{id}',
    status_code=status.HTTP_200_OK,
    response_model=Union[PostOut, ValidationErrorResponse, DetailResponse],
    dependencies=[Depends(verify_post_content)],
)
async def update_post(
    data: PostIn = Depends(PostIn.form_update_post),
    repo=Depends(post_repository_dependency),
):
    if isinstance(data, ValidationErrorResponse):
        return ResponseGenerator.validation_error_response(data)
    try:
        post = await repo.get_by_id(str(data.id))
        if post is None:
            return ResponseGenerator.no_instance_found_error_response(
                f'post not found: {id}'
            )

        update_post: Post = Post(
            id=data.id,
            user=post.user,
            topic=data.topic if data.topic is not None else post.topic,
            description=data.description
            if data.description is not None
            else post.description,
            file=data.file
            if data.file is not None
            else None
            if data.url is not None
            else post.file,
            url=data.url
            if data.url is not None
            else None
            if data.file is not None
            else post.url,
            created_at=post.created_at,
        )
        await repo.create_update(update_post, False)
        return await repo.get_by_id(data.id)
    except MongoRepositoryException as e:
        return ResponseGenerator.db_connection_error_response(str(e))


@router.delete(
    '/{id}',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=Union[None, DetailResponse],
)
async def delete_post(id: str = Path(), repo=Depends(post_repository_dependency)):
    try:
        post = await repo.get_by_id(id)
        if post is None:
            return ResponseGenerator.no_instance_found_error_response(
                f'post not found: {id}'
            )
        await repo.delete(id)
    except MongoRepositoryException as e:
        return ResponseGenerator.db_connection_error_response(str(e))
