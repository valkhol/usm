import uuid
from datetime import date, datetime
from tempfile import SpooledTemporaryFile

from slugify import slugify


class User:
    _id: str
    _slug: str
    _email: str
    _password: str
    _name: str
    _last_name: str
    _birth_date: datetime
    _photo_file: SpooledTemporaryFile
    _created_at: datetime
    _country: str

    def __init__(
        self,
        email: str,
        name: str,
        last_name: str,
        country: str,
        birth_date: date,
        password: str | None = None,
        id: str | None = None,
        slug: str | None = None,
        created_at: datetime | None = None,
        photo_file: SpooledTemporaryFile | None = None,
    ):
        self._id = id if id is not None else str(uuid.uuid4())
        self._slug = (
            slug if slug is not None else slugify('{} {}'.format(name, last_name))
        )
        self._email = email
        self._password = password
        self._name = name
        self._last_name = last_name
        self._birth_date = datetime.combine(birth_date, datetime.min.time())
        self._photo_file = photo_file
        self._created_at = created_at if created_at is not None else datetime.now()
        self._country = country

    @property
    def id(self) -> str:
        return self._id

    @property
    def slug(self) -> str:
        return self._slug

    @property
    def email(self) -> str:
        return self._email

    @property
    def password(self) -> str:
        return self._password

    @property
    def name(self) -> str:
        return self._name

    @property
    def last_name(self) -> str:
        return self._last_name

    @property
    def birth_date(self) -> datetime:
        return self._birth_date

    @property
    def photo_file(self) -> SpooledTemporaryFile:
        return self._photo_file

    @property
    def created_at(self) -> datetime:
        return self._created_at

    @property
    def country(self) -> str:
        return self._country
