from datetime import date

from dateutil.relativedelta import relativedelta

from app.constants import AGE_LIMIT
from tests.unit.countries.test_data import COUNTRY_LIST

country = list(COUNTRY_LIST.keys())[0]
USER_EMAIL = 'test@gmail.com'
USER_SLUG = 'name-last-name'
# -------------------------------------
# -------------CREATE USER-------------
# -------------------------------------

USER_DATA_WITHOUT_FILE = {
    'email': 'test@gmail.com',
    'password': 'password',
    'name': 'name',
    'last_name': 'last-name',
    'country': country,
    'birth_date': '2000-01-01',
}

USER_DATA_WITH_FILE = {
    'email': 'test@gmail.com',
    'password': 'password',
    'name': 'name',
    'last_name': 'last-name',
    'country': country,
    'birth_date': '2000-01-01',
    'file': b"test",
}

USER_DATA_WRONG_EMAIL = {
    'email': 'wrong-email',
    'password': 'password',
    'name': 'name',
    'last_name': 'last-name',
    'country': country,
    'birth_date': '2000-01-01',
}

USER_DATA_WRONG_COUNTRY = {
    'email': 'test@gmail.com',
    'password': 'password',
    'name': 'name',
    'last_name': 'last-name',
    'country': 'no country',
    'birth_date': '2000-01-01',
}

USER_DATA_WRONG_NAME = {
    'email': 'test@gmail.com',
    'password': 'password',
    'name': '***',
    'last_name': 'last-name',
    'country': country,
    'birth_date': '2000-01-01',
}

USER_DATA_WRONG_LAST_NAME = {
    'email': 'test@gmail.com',
    'password': 'password',
    'name': 'name',
    'last_name': '***',
    'country': country,
    'birth_date': '2000-01-01',
}


USER_DATA_LOW_AGE = {
    'email': 'test@gmail.com',
    'password': 'password',
    'name': 'name',
    'last_name': 'last-name',
    'country': country,
    'birth_date': str(date.today() - relativedelta(years=AGE_LIMIT - 1)),
}


# -------------------------------------
# -------------UPDATE USER-------------
# -------------------------------------

USER_DATA_UPDATE_WITH_FILE = {
    'email': 'test@gmail.com',
    'password': 'password',
    'name': 'name',
    'last_name': 'last-name',
    'country': country,
    'birth_date': '2000-01-01',
    'file': b"test",
}

USER_DATA_UPDATE_1 = {
    'last_name': 'UPDATED-last-name',
    'country': list(COUNTRY_LIST.keys())[1],
    'birth_date': '1999-01-01',
}

USER_DATA_UPDATE_2 = {
    'email': 'UPDATED_test@gmail.com',
    'password': 'UPDATED_password',
    'name': 'UPDATED-name',
}
