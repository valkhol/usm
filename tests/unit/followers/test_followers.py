# import uuid

# import pytest
# from httpx import AsyncClient
# from starlette import status

# from app.app import create_app
# from tests.fixtures import anyio_backend, mock_client_init
# from tests.unit.users.test_data import USER_DATA_WITHOUT_FILE

# from app.dependencies import authenticate

# async def successful_auth():
#     return True

# APP = create_app()
# APP.dependency_overrides[authenticate] = successful_auth


# @pytest.fixture
# async def create_users():
#     async with AsyncClient(app=APP, base_url="http://test") as ac:
#         response = await ac.post("v1/users/", data=USER_DATA_WITHOUT_FILE)
#         user_1 = response.json()['id']
#         response = await ac.post("v1/users/", data=USER_DATA_WITHOUT_FILE)
#         user_2 = response.json()['id']
#     return user_1, user_2


# @pytest.mark.anyio
# @pytest.mark.parametrize(
#     'wrong_user_1, wrong_user_2, expected_status',
#     [
#         (False, False, status.HTTP_201_CREATED),
#         (True, False, status.HTTP_400_BAD_REQUEST),
#         (False, True, status.HTTP_400_BAD_REQUEST),
#     ],
# )
# async def test_create_follow(
#     anyio_backend,
#     mock_client_init,
#     create_users,
#     wrong_user_1,
#     wrong_user_2,
#     expected_status,
# ):
#     user_1, user_2 = create_users
#     if wrong_user_1:
#         user_1 = str(uuid.uuid4())
#     if wrong_user_2:
#         user_2 = str(uuid.uuid4())

#     async with AsyncClient(app=APP, base_url="http://test") as ac:
#         response = await ac.post("v1/followers/", data={'id': user_1, 'follow': user_2})

#     assert response.status_code == expected_status


# @pytest.mark.anyio
# async def test_delete_follow(anyio_backend, mock_client_init, create_users):
#     user_1, user_2 = create_users
#     async with AsyncClient(app=APP, base_url="http://test") as ac:
#         await ac.post("v1/followers/", data={'id': user_1, 'follow': user_2})

#         response = await ac.delete("v1/followers/{}/{}".format(user_1, user_2))
#         assert response.status_code == status.HTTP_202_ACCEPTED

#         response = await ac.delete("v1/followers/{}/{}".format(user_1, str(uuid.uuid4())))
#         assert response.status_code == status.HTTP_400_BAD_REQUEST

#         response = await ac.delete("v1/followers/{}/{}".format(str(uuid.uuid4()), user_2))
#         assert response.status_code == status.HTTP_400_BAD_REQUEST

#         response = await ac.delete("v1/followers/{}/{}".format(user_2, user_1))
#         assert response.status_code == status.HTTP_400_BAD_REQUEST


# @pytest.mark.anyio
# async def test_get_follows(
#     anyio_backend,
#     mock_client_init,
# ):
#     async with AsyncClient(app=APP, base_url="http://test") as ac:
#         users = []
#         for i in range(10):
#             response = await ac.post("v1/users/", data=USER_DATA_WITHOUT_FILE)
#             users.append(response.json()['id'])

#         user = users[0]
#         for i in range(1, 10):
#             await ac.post("v1/followers/", data={'id': user, 'follow': users[i]})

#         response = await ac.get(f"v1/followers/{user}")
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.json()['follows']) == 9

#         response = await ac.get(f"v1/followers/{str(uuid.uuid4())}")
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.json()['follows']) == 0
