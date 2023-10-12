# import uuid

# import pytest
# from aiohttp import ClientSession
# from fastapi.responses import JSONResponse
# from httpx import AsyncClient
# from starlette import status

# from app.app import create_app
# from tests.fixtures import anyio_backend, mock_client_init
# from tests.unit.posts.test_data import POST_DATA_WITH_FILE
# from tests.unit.users.test_data import USER_DATA_WITHOUT_FILE

# from app.dependencies import authenticate
# from asyncio import sleep

# async def successful_auth():
#     return True

# APP = create_app()
# APP.dependency_overrides[authenticate] = successful_auth


# @pytest.fixture
# async def create_users_and_follow_and_post():
#     async with AsyncClient(app=APP, base_url='http://test') as ac:
#         response = await ac.post('v1/users/', data=USER_DATA_WITHOUT_FILE)
#         user = response.json()['id']

#         response = await ac.post('v1/users/', data=USER_DATA_WITHOUT_FILE)
#         follow = response.json()['id']

#         await ac.post('v1/followers/', data={'id': user, 'follow': follow})

#         data = POST_DATA_WITH_FILE.copy()
#         files = []
#         files.append(('file', ('image.jpeg', data.get('file'), 'image/jpeg')))
#         data['user'] = follow
#         for i in range(10):
#             response = await ac.post('v1/posts/', data=data, files=files)
#         sleep(5)
#     return user


# async def test_strip(
#     anyio_backend,
#     mock_client_init,
#     create_users_and_follow_and_post,
# ):
#     user = create_users_and_follow_and_post

#     async with AsyncClient(app=APP, base_url='http://test') as ac:
#         response = await ac.get(f'v1/strip/{str(uuid.uuid4())}')
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.json()['strip']) == 0

#         response = await ac.get(f'v1/strip/{user}')
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.json()['strip']) == 10

#         skip = 5
#         for strip_record in response.json()['strip']:
#             await ac.patch('v1/strip/{}/watched'.format(strip_record['id']))
#             skip -= 1
#             if skip == 0:
#                 break

#         response = await ac.get(f'v1/strip/{user}')
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.json()['strip']) == 5
