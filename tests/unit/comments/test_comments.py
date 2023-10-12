# import uuid

# import pytest
# from httpx import AsyncClient
# from starlette import status

# from app.app import create_app
# from app.models.country import Country
# from app.repositories.mongo.country_repo import CountryRepositoryMongo
# from tests.fixtures import anyio_backend, mock_client_init
# from tests.unit.countries.test_data import COUNTRY_LIST
# from tests.unit.posts.test_data import POST_DATA_WITH_FILE
# from tests.unit.users.test_data import USER_DATA_WITHOUT_FILE
# from app.dependencies import authenticate

# async def successful_auth():
#     return True

# APP = create_app()
# APP.dependency_overrides[authenticate] = successful_auth



# @pytest.fixture
# async def create_user_and_post(mock_client_init):
#     repo = CountryRepositoryMongo()
#     for key, value in COUNTRY_LIST.items():
#         country = Country(id=key, name=value)
#         await repo.create_update(country)

#     async with AsyncClient(app=APP, base_url="http://test") as ac:
#         response = await ac.post("v1/users/", data=USER_DATA_WITHOUT_FILE)
#         user = response.json()['id']

#         data = POST_DATA_WITH_FILE.copy()
#         files = []
#         files.append(('file', ('image.jpeg', data.get('file'), 'image/jpeg')))
#         data['user'] = user
#         response = await ac.post("v1/posts/", data=data, files=files)
#         post = response.json()['id']

#     return user, post


# @pytest.mark.anyio
# @pytest.mark.parametrize(
#     'wrong_user, wrong_post, expected_status',
#     [
#         (False, False, status.HTTP_201_CREATED),
#         (False, True, status.HTTP_400_BAD_REQUEST),
#         (True, False, status.HTTP_400_BAD_REQUEST),
#     ],
# )
# async def test_create_comment(
#     anyio_backend,
#     mock_client_init,
#     create_user_and_post,
#     wrong_user,
#     wrong_post,
#     expected_status,
# ):
#     user, post = create_user_and_post

#     comment_data = {
#         'user': str(uuid.uuid4()) if wrong_user else user,
#         'post': str(uuid.uuid4()) if wrong_post else post,
#         'text': 'test-text',
#     }

#     async with AsyncClient(app=APP, base_url="http://test") as ac:
#         response = await ac.post("v1/comments/", data=comment_data)

#         assert response.status_code == expected_status
#         if expected_status == status.HTTP_201_CREATED:
#             for key in comment_data.keys():
#                 assert comment_data[key] == response.json()[key]


# async def test_find_comments_by_post(
#     anyio_backend,
#     mock_client_init,
#     create_user_and_post,
# ):
#     user, post = create_user_and_post

#     comment_data = {
#         'user': user,
#         'post': post,
#         'text': 'test-text',
#     }

#     async with AsyncClient(app=APP, base_url="http://test") as ac:
#         for i in range(10):
#             await ac.post("v1/comments/", data=comment_data)

#         response = await ac.get(f"v1/comments/?post={post}&skip=2&limit=5")
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.json()['comments']) == 5

#         response = await ac.get(f"v1/comments/?post={str(uuid.uuid4())}&skip=2&limit=5")
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.json()['comments']) == 0


# async def test_update_comment(
#     anyio_backend,
#     mock_client_init,
#     create_user_and_post,
# ):
#     user, post = create_user_and_post

#     comment_data = {
#         'user': user,
#         'post': post,
#         'text': 'test-text',
#     }

#     async with AsyncClient(app=APP, base_url="http://test") as ac:
#         response = await ac.post("v1/comments/", data=comment_data)
#         comment = response.json()['id']

#         updated_data = {
#             'text': 'updated-text',
#         }
#         response = await ac.patch(f"v1/comments/{comment}", data=updated_data)
#         assert response.status_code == status.HTTP_200_OK
#         assert response.json()['text'] == updated_data['text']


# async def test_delete_comment(
#     anyio_backend,
#     mock_client_init,
#     create_user_and_post,
# ):
#     user, post = create_user_and_post

#     comment_data = {
#         'user': user,
#         'post': post,
#         'text': 'test-text',
#     }

#     async with AsyncClient(app=APP, base_url="http://test") as ac:
#         response = await ac.post("v1/comments/", data=comment_data)
#         comment = response.json()['id']

#         response = await ac.get(f"v1/comments/?post={post}")
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.json()['comments']) == 1

#         response = await ac.delete(f"v1/comments/{comment}")
#         assert response.status_code == status.HTTP_202_ACCEPTED

#         response = await ac.get(f"v1/comments/?post={post}")
#         assert response.status_code == status.HTTP_200_OK
#         assert len(response.json()['comments']) == 0
