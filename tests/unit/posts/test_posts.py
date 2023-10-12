import uuid

import pytest
from aiohttp import ClientSession
from fastapi.responses import JSONResponse
from httpx import AsyncClient
from starlette import status

from app.app import create_app
from tests.fixtures import anyio_backend, mock_client_init
from tests.unit.posts.test_data import (POST_DATA_NO_URL_NO_FILE,
                                        POST_DATA_WITH_FILE,
                                        POST_DATA_WITH_URL,
                                        POST_DATA_WITH_URL_WITH_FILE,
                                        POST_DATA_WITH_WRONG_URL,
                                        UPDATE_POST_DATA)
from tests.unit.users.test_data import USER_DATA_WITHOUT_FILE

from app.dependencies import authenticate


async def successful_auth():
    return True

APP = create_app()
APP.dependency_overrides[authenticate] = successful_auth


@pytest.fixture
async def create_user():
    async with AsyncClient(app=APP, base_url="http://test") as ac:
        response = await ac.post("v1/users/", data=USER_DATA_WITHOUT_FILE)
        user_id = response.json()['id']
    return user_id


class CustomResponse(JSONResponse):
    def __init__(self, status_code, content):
        super().__init__(status_code=status_code, content=content)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, tb):
        return True


@pytest.mark.anyio
@pytest.mark.parametrize(
    'post_data, expected_status',
    [
        (POST_DATA_WITH_FILE, status.HTTP_201_CREATED),
        (POST_DATA_WITH_URL, status.HTTP_201_CREATED),
        # (POST_DATA_WITH_WRONG_URL, status.HTTP_400_BAD_REQUEST),
        (POST_DATA_NO_URL_NO_FILE, status.HTTP_400_BAD_REQUEST),
        (POST_DATA_WITH_URL_WITH_FILE, status.HTTP_400_BAD_REQUEST),
    ],
)
async def test_create_post(
    anyio_backend, mock_client_init, monkeypatch, create_user, post_data, expected_status
):
    checking_status = (
        status.HTTP_400_BAD_REQUEST
        if post_data == POST_DATA_WITH_WRONG_URL
        else status.HTTP_200_OK
    )
    monkeypatch.setattr(
        ClientSession,
        'get',
        lambda x, y: CustomResponse(status_code=checking_status, content='OK'),
    )
    files = []
    if post_data.get('file') is not None:
        files.append(('file', ('image.jpeg', post_data.get('file'), 'image/jpeg')))

    # user = await create_user()
    data = post_data.copy()
    data['user'] = create_user
    async with AsyncClient(app=APP, base_url="http://test") as ac:
        response = await ac.post("v1/posts/", data=data, files=files)

    assert response.status_code == expected_status

    if post_data == POST_DATA_WITH_FILE:
        assert response.json()['file'] is not None
        assert response.json()['url'] is None
    if post_data == POST_DATA_WITH_URL:
        assert response.json()['file'] is None
        assert response.json()['url'] is not None


@pytest.mark.anyio
@pytest.mark.parametrize(
    'success, expected_status',
    [(True, status.HTTP_200_OK), (False, status.HTTP_400_BAD_REQUEST)],
)
async def test_get_post(
    anyio_backend, mock_client_init, create_user, success, expected_status
):
    data = POST_DATA_WITH_FILE.copy()
    data['user'] = create_user
    files = []
    files.append(('file', ('image.jpeg', data.get('file'), 'image/jpeg')))
    async with AsyncClient(app=APP, base_url="http://test") as ac:
        if success:
            post_response = await ac.post("v1/posts/", data=data, files=files)
            post_id = post_response.json()['id']
        else:
            post_id = str(uuid.uuid4())

        response = await ac.get(f"v1/posts/{post_id}")

    assert response.status_code == expected_status
    if success:
        assert all(key in response.json().keys() for key in data.keys())


@pytest.mark.anyio
@pytest.mark.parametrize(
    'post_exists, expected_status',
    [
        (True, status.HTTP_200_OK),
        (False, status.HTTP_400_BAD_REQUEST),
    ],
)
async def test_update_post(
    anyio_backend,
    mock_client_init,
    monkeypatch,
    create_user,
    post_exists,
    expected_status,
):
    monkeypatch.setattr(
        ClientSession,
        'get',
        lambda x, y: CustomResponse(status_code=status.HTTP_200_OK, content='OK'),
    )
    data = POST_DATA_WITH_FILE.copy()
    files = []
    files.append(('file', ('image.jpeg', data.get('file'), 'image/jpeg')))
    data['user'] = create_user
    async with AsyncClient(app=APP, base_url="http://test") as ac:
        if post_exists:
            post_response = await ac.post("v1/posts/", data=data, files=files)
            post_id = post_response.json()['id']
        else:
            post_id = str(uuid.uuid4())

        response = await ac.patch(f"v1/posts/{post_id}", data=UPDATE_POST_DATA)

    assert response.status_code == expected_status

    if post_exists:
        for key in ('url', 'file', 'topic', 'description'):
            assert response.json()[key] == UPDATE_POST_DATA[key]


@pytest.mark.anyio
@pytest.mark.parametrize(
    'post_exists, expected_status',
    [
        (True, status.HTTP_202_ACCEPTED),
        (False, status.HTTP_400_BAD_REQUEST),
    ],
)
async def test_delete_post(
    anyio_backend,
    mock_client_init,
    monkeypatch,
    create_user,
    post_exists,
    expected_status,
):
    data = POST_DATA_WITH_FILE.copy()
    files = []
    files.append(('file', ('image.jpeg', data.get('file'), 'image/jpeg')))
    data['user'] = create_user
    async with AsyncClient(app=APP, base_url="http://test") as ac:
        if post_exists:
            post_response = await ac.post("v1/posts/", data=data, files=files)
            post_id = post_response.json()['id']
        else:
            post_id = str(uuid.uuid4())

        response = await ac.delete(f"v1/posts/{post_id}")

        assert response.status_code == expected_status

        if post_exists:
            response = await ac.get(f"v1/posts/{post_id}")
            assert response.status_code == status.HTTP_400_BAD_REQUEST
