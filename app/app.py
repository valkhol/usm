from fastapi import FastAPI, Request
from app.handlers import comments, followers, posts, strip, token, users, health
from app import midlwares

import logging
import logging.config

from app.settings import LOGGING
logging.config.dictConfig(LOGGING)


def create_app():
    """
    Creates fastAPI application"""
    app = FastAPI()

    app.include_router(health.router)
    app.include_router(token.router)
    app.include_router(users.router)
    app.include_router(followers.router)
    app.include_router(posts.router)
    app.include_router(comments.router)
    app.include_router(strip.router)

    @app.middleware("http")
    async def add_process_time_header(request: Request, call_next):
        response = await midlwares.read_stats(request, call_next)

        return response

    return app
