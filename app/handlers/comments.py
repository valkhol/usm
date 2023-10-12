from typing import Union
from fastapi import APIRouter, Depends, Path, Query
from starlette import status

from app.dependencies import (authenticate, comment_repository_dependency,
                              pagination_params, verify_user_and_post_exist)
from app.dto.comment import CommentIn, CommentOut, CommentOutList
from app.dto.responses import (DetailResponse, ResponseGenerator,
                               ValidationErrorResponse)
from app.models.comment import Comment
from app.repositories.mongo.mongo_client import MongoRepositoryException

# router = APIRouter(
#     prefix='/v1/comments', tags=['comments'], dependencies=[Depends(authenticate)]
# )

router = APIRouter(
    prefix='/v1/comments', tags=['comments']
)


@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    response_model=Union[CommentOut, ValidationErrorResponse, DetailResponse],
    dependencies=[Depends(verify_user_and_post_exist)],
)
async def create_comment(
    data: CommentIn = Depends(CommentIn.form_create_comment),
    repo=Depends(comment_repository_dependency),
):
    comment: Comment = Comment(
        user=str(data.user),
        post=str(data.post),
        text=data.text,
    )
    try:
        await repo.create_update(comment)
        return await repo.get_by_id(comment.id)
    except MongoRepositoryException as e:
        return ResponseGenerator.db_connection_error_response(str(e))


@router.patch(
    '/{id}',
    status_code=status.HTTP_200_OK,
    response_model=Union[CommentOut, DetailResponse],
)
async def update_comment(
    data: CommentIn = Depends(CommentIn.form_update_comment),
    repo=Depends(comment_repository_dependency),
):
    try:
        comment = await repo.get_by_id(data.id)
        if comment is None:
            return ResponseGenerator.no_instance_found_error_response(
                f'comment not found: {data.id}'
            )

        update_comment: Comment = Comment(
            id=data.id,
            user=comment.user,
            post=comment.post,
            text=data.text,
            created_at=comment.created_at,
        )
        await repo.create_update(update_comment)
        return await repo.get_by_id(data.id)
    except MongoRepositoryException as e:
        return ResponseGenerator.db_connection_error_response(str(e))


@router.delete(
    '/{id}',
    status_code=status.HTTP_202_ACCEPTED,
    response_model=Union[None, DetailResponse],
)
async def delete_comment(id: str = Path(), repo=Depends(comment_repository_dependency)):
    comment = await repo.get_by_id(id)
    if comment is None:
        return ResponseGenerator.no_instance_found_error_response(
            f'comment not found: {id}'
        )
    try:
        await repo.delete(id)
    except MongoRepositoryException as e:
        return ResponseGenerator.db_connection_error_response(str(e))


@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    response_model=Union[CommentOutList, DetailResponse],
)
async def find_comments_by_post(
    post: str = Query(),
    pagination=Depends(pagination_params),
    repo=Depends(comment_repository_dependency),
):
    try:
        comments = await repo.get_by_post(
            post=post, skip=pagination.skip, limit=pagination.limit
        )
    except MongoRepositoryException as e:
        return ResponseGenerator.db_connection_error_response(str(e))

    return {'comments': comments}
