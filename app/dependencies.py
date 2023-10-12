from collections import namedtuple

import aiohttp
from fastapi import Depends, Form, HTTPException, Path, Query, UploadFile
from jose import JWTError, jwt
from starlette import status

from app.auth import TokenData, oauth2_scheme
from app.repositories.mongo.comment_repo import CommentRepositoryMongo
from app.repositories.mongo.follower_repo import FollowerRepositoryMongo
from app.repositories.mongo.mongo_client import MongoRepositoryException
from app.repositories.mongo.post_repo import PostRepositoryMongo
from app.repositories.mongo.strip_repo import StripRepositoryMongo
from app.repositories.mongo.user_repo import UserRepositoryMongo
from app.settings import ALGORITHM, SECRET_KEY


def pagination_params(
    skip: int = Query(0, ge=0),
    limit: int = Query(0, le=1000),
):
    Pagination = namedtuple("Pagination", ["skip", "limit"])
    return Pagination(skip=skip, limit=limit)


async def post_repository_dependency():
    return PostRepositoryMongo()


async def user_repository_dependency():
    return UserRepositoryMongo()


def comment_repository_dependency():
    return CommentRepositoryMongo()


def strip_repository_dependency():
    return StripRepositoryMongo()


def follower_repository_dependency():
    return FollowerRepositoryMongo()


async def verify_users_exist(id: str, follow: str):
    try:
        user_repo = UserRepositoryMongo()
        user, follow_user = await user_repo.get_by_id(id), await user_repo.get_by_id(
            follow
        )
        errors = []
        if user is None:
            errors.append(f'user {id} not found')
        if follow_user is None:
            errors.append(f'user {follow} not found')
        if errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='\n'.join(errors)
            )
    except MongoRepositoryException as e:
        return HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=f'DB error: {str(e)}'
        )


async def verify_users_exist_path(id: str = Path(...), follow: str = Path(...)):
    await verify_users_exist(id, follow)


async def verify_users_exist_form(id: str = Form(...), follow: str = Form(...)):
    await verify_users_exist(id, follow)


async def verify_user_and_post_exist(user: str = Form(...), post: str = Form(...)):
    try:
        user_repo = UserRepositoryMongo()
        user_resul = await user_repo.get_by_id(user)

        post_repo = PostRepositoryMongo()
        post_resul = await post_repo.get_by_id(post)

        errors = []
        if user_resul is None:
            errors.append(f'user {user} not found')
        if post_resul is None:
            errors.append(f'post {post} not found')
        if errors:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail='\n'.join(errors)
            )
    except MongoRepositoryException as e:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=f'DB error: {str(e)}'
        )


async def verify_post_content(
    url: str | None = Form(default=None), file: UploadFile | None = Form(default=None)
):
    if (url is not None and file is not None) or (url is None and file is None):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='only url or only file should be provided',
        )
    if url is None:
        return

    error = False
    detail = ''
    async with aiohttp.ClientSession() as session:
        try:
            async with session.get(url) as response:
                if response.status != status.HTTP_200_OK:
                    error = True
                    detail = 'Wrong url. There is no content.'
        except aiohttp.client_exceptions.ClientConnectionError:
            error = True
            detail = 'Wrong url. There is no content.'

        except aiohttp.client_exceptions.InvalidURL:
            error = True
            detail = 'Invalid url.'

    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
        )


async def authenticate(
    token: str = Depends(oauth2_scheme), repo=Depends(user_repository_dependency)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    try:
        user = await repo.get_by_param({'email': token_data.email})
    except MongoRepositoryException as e:
        raise HTTPException(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT, detail=f'DB error: {str(e)}'
        )

    if user is None:
        raise credentials_exception
