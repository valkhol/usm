from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from starlette import status
from starlette.responses import JSONResponse


class ValidationErrorResponse(BaseModel):
    detail: str


class DetailResponse(BaseModel):
    detail: str


class ResponseGenerator:
    @staticmethod
    def db_connection_error_response(error: str):
        return JSONResponse(
            status_code=status.HTTP_504_GATEWAY_TIMEOUT,
            content=jsonable_encoder(DetailResponse(detail=f'DB error: {error}')),
        )

    @staticmethod
    def no_instance_found_error_response(error: str):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(DetailResponse(detail=error)),
        )

    @staticmethod
    def validation_error_response(data: ValidationErrorResponse):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(data),
        )

    @staticmethod
    def custom_validation_error_response(error: str):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content=jsonable_encoder(ValidationErrorResponse(detail=error)),
        )

    @staticmethod
    def auth_erro_response(error: str | None = None):
        error = error or 'Incorrect username or password'
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=jsonable_encoder(DetailResponse(detail=error)),
            headers={"WWW-Authenticate": "Bearer"},
        )
