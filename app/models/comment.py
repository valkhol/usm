import uuid
from datetime import datetime


class Comment:
    _id: str
    _user: str
    _post: str
    _text: str
    _created_at: datetime

    def __init__(
        self,
        post: str,
        user: str,
        text: str,
        id: str | None = None,
        created_at: datetime | None = None,
    ):
        self._id = id if id is not None else str(uuid.uuid4())
        self._user = user
        self._post = post
        self._text = text
        self._created_at = created_at if created_at is not None else datetime.now()

    @property
    def id(self) -> str:
        return self._id

    @property
    def user(self) -> str:
        return self._user

    @property
    def post(self) -> str:
        return self._post

    @property
    def text(self) -> str:
        return self._text

    @property
    def created_at(self) -> datetime:
        return self._created_at
