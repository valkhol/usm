# import pytest

# from app.models.country import Country
# from app.repositories.mongo.country_repo import CountryRepositoryMongo
# from tests.fixtures import mock_client_init
# from tests.unit.countries.test_data import COUNTRY_LIST


# @pytest.mark.asyncio
# async def test_country_repository(mock_client_init):
#     repo = CountryRepositoryMongo()
#     for key, value in COUNTRY_LIST.items():
#         country = Country(id=key, name=value)
#         await repo.create_update(country)

#     n = await repo.collection.count_documents({})

#     assert n == len(COUNTRY_LIST)
#     for key in COUNTRY_LIST.keys():
#         country = await repo.get_by_id(key)
#         assert country is not None
