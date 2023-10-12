import uuid
from datetime import datetime
from tempfile import SpooledTemporaryFile


class Post:
    _id: str
    _user: str
    _topic: str
    _description: str
    _file: SpooledTemporaryFile
    _url: str
    _created_at: datetime

    def __init__(
        self,
        user: str,
        topic: str,
        description: str,
        id: str | None = None,
        created_at: datetime | None = None,
        file: SpooledTemporaryFile | None = None,
        url: str | None = None,
    ):
        self._id = id if id is not None else str(uuid.uuid4())
        self._user = user
        self._topic = topic
        self._description = description
        self._file = file
        self._url = url
        self._created_at = created_at if created_at is not None else datetime.now()

    @property
    def id(self) -> str:
        return self._id

    @property
    def user(self) -> str:
        return self._user

    @property
    def topic(self) -> str:
        return self._topic

    @property
    def description(self) -> str:
        return self._description

    @property
    def file(self) -> str:
        return self._file

    @property
    def url(self) -> str:
        return self._url

    @property
    def created_at(self) -> datetime:
        return self._created_at
