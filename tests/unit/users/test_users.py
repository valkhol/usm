import pytest
from httpx import AsyncClient
from starlette import status
from app.dependencies import authenticate
from app.app import create_app
from tests.fixtures import anyio_backend, mock_client_init
from tests.unit.users.test_data import (USER_DATA_LOW_AGE, USER_DATA_UPDATE_1,
                                        USER_DATA_UPDATE_2,
                                        USER_DATA_UPDATE_WITH_FILE,
                                        USER_DATA_WITH_FILE,
                                        USER_DATA_WITHOUT_FILE,
                                        USER_DATA_WRONG_COUNTRY,
                                        USER_DATA_WRONG_EMAIL,
                                        USER_DATA_WRONG_LAST_NAME,
                                        USER_DATA_WRONG_NAME, USER_EMAIL,
                                        USER_SLUG)


async def successful_auth():
    return True

APP = create_app()
APP.dependency_overrides[authenticate] = successful_auth


@pytest.mark.anyio
@pytest.mark.parametrize(
    'user_data, expected_status',
    [
        (USER_DATA_WITH_FILE, status.HTTP_201_CREATED),
        (USER_DATA_WITHOUT_FILE, status.HTTP_201_CREATED),
        (USER_DATA_WRONG_EMAIL, status.HTTP_400_BAD_REQUEST),
        (USER_DATA_WRONG_COUNTRY, status.HTTP_400_BAD_REQUEST),
        (USER_DATA_WRONG_NAME, status.HTTP_400_BAD_REQUEST),
        (USER_DATA_WRONG_LAST_NAME, status.HTTP_400_BAD_REQUEST),
        (USER_DATA_LOW_AGE, status.HTTP_400_BAD_REQUEST),
    ],
)
async def test_create_user(anyio_backend, mock_client_init, user_data, expected_status):
    files = []
    if user_data.get('file') is not None:
        files.append(('user_photo', ('image.jpeg', user_data.get('file'), 'image/jpeg')))

    async with AsyncClient(app=APP, base_url="http://test") as ac:
        response = await ac.post("v1/users/", data=user_data, files=files)

    assert response.status_code == expected_status

    if user_data == USER_DATA_WITH_FILE:
        assert response.json()['photo_file'] is not None
    if user_data == USER_DATA_WITHOUT_FILE:
        assert response.json()['photo_file'] is None


@pytest.mark.anyio
@pytest.mark.parametrize(
    'user_data, expected_status',
    [
        (USER_DATA_UPDATE_WITH_FILE, status.HTTP_200_OK),
        (USER_DATA_UPDATE_1, status.HTTP_200_OK),
        (USER_DATA_UPDATE_2, status.HTTP_200_OK),
    ],
)
async def test_update_user(anyio_backend, mock_client_init, user_data, expected_status):
    files = []
    if user_data.get('file') is not None:
        files.append(('user_photo', ('image.jpeg', user_data.get('file'), 'image/jpeg')))

    async with AsyncClient(app=APP, base_url="http://test") as ac:
        response = await ac.post("v1/users/", data=USER_DATA_WITH_FILE)
        user_id = response.json()['id']

        response = await ac.patch(f"v1/users/{user_id}", data=user_data, files=files)

    assert response.status_code == expected_status

    if user_data == USER_DATA_UPDATE_WITH_FILE:
        assert response.json()['photo_file'] is not None
    else:
        for key in user_data.keys():
            if key == 'birth_date':
                assert response.json()[key].startswith(user_data[key])
            elif key == 'password':
                continue
            else:
                assert user_data[key] == response.json()[key]


@pytest.mark.anyio
async def test_get_user(anyio_backend, mock_client_init):
    async with AsyncClient(app=APP, base_url="http://test") as ac:
        response = await ac.post("v1/users/", data=USER_DATA_WITHOUT_FILE)
        user_id = response.json()['id']

        response = await ac.get(f"v1/users/{user_id}")

        response_wrong_id = await ac.get("v1/users/wrong-id")

    assert response.status_code == status.HTTP_200_OK
    for key in USER_DATA_WITHOUT_FILE.keys():
        if key == 'birth_date':
            assert response.json()[key].startswith(USER_DATA_WITHOUT_FILE[key])
        elif key == 'password':
            continue
        else:
            assert USER_DATA_WITHOUT_FILE[key] == response.json()[key]
    assert response_wrong_id.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
@pytest.mark.parametrize(
    'email, slug, expected_status',
    [
        (USER_EMAIL, None, status.HTTP_200_OK),
        (None, USER_SLUG, status.HTTP_200_OK),
        (None, None, status.HTTP_400_BAD_REQUEST),
        ('wrong@email.com', None, status.HTTP_200_OK),
    ],
)
async def test_get_user_by_param(
    anyio_backend, mock_client_init, email, slug, expected_status
):
    params = {}
    if email is not None:
        params['email'] = email

    if slug is not None:
        params['slug'] = slug

    async with AsyncClient(app=APP, base_url="http://test") as ac:
        response = await ac.post("v1/users/", data=USER_DATA_WITHOUT_FILE)

        response = await ac.get(
            "v1/users/?{}".format(
                '&'.join([f'{key}={value}' for key, value in params.items()])
            )
        )

    assert response.status_code == expected_status


@pytest.mark.anyio
async def test_delete_user(anyio_backend, mock_client_init):
    async with AsyncClient(app=APP, base_url="http://test") as ac:
        response = await ac.post("v1/users/", data=USER_DATA_WITHOUT_FILE)
        user_id = response.json()['id']

        response = await ac.delete(f"v1/users/{user_id}")
        assert response.status_code == status.HTTP_202_ACCEPTED

        response = await ac.get(f"v1/users/{user_id}")
        assert response.status_code == status.HTTP_400_BAD_REQUEST


@pytest.mark.anyio
async def test_search_user(anyio_backend, mock_client_init):
    user_data = USER_DATA_WITHOUT_FILE.copy()
    user_data['name'] = 'find-me'

    async with AsyncClient(app=APP, base_url="http://test") as ac:
        for i in range(10):
            await ac.post("v1/users/", data=user_data)

        skip = 5
        limit = 5
        response = await ac.get(f"v1/users/search/slug?skip={skip}&limit={limit}&search=find")
        assert response.status_code == status.HTTP_200_OK
        assert response.json().get('users') is not None
        assert len(response.json().get('users')) == 5
