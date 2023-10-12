from datetime import timedelta
from fastapi import APIRouter, Depends, Form

from app.auth import Token, create_access_token, verify_password
from app.dependencies import user_repository_dependency
from app.dto.responses import ResponseGenerator
from app.repositories.mongo.mongo_client import MongoRepositoryException
from app.settings import ACCESS_TOKEN_EXPIRE_MINUTES

router = APIRouter(prefix='/token', tags=['access'])


@router.post('/', response_model=Token)
async def login_for_access_token(
    email: str = Form(), password: str = Form(), repo=Depends(user_repository_dependency)
):
    try:
        user = await repo.get_by_param({'email': email})
    except MongoRepositoryException as e:
        return ResponseGenerator.db_connection_error_response(str(e))

    if user is None:
        return ResponseGenerator.auth_erro_response()
    if not verify_password(password, user.password):
        return ResponseGenerator.auth_erro_response()

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
