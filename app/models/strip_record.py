import uuid
from datetime import datetime


class StripRecord:
    _id: str
    _user: str
    _post: str
    _wathced: bool
    _created_at: datetime

    def __init__(
        self,
        user: str,
        post: str,
        id: str = None,
        wathced: bool = False,
        created_at: datetime = None,
    ):
        self._id = id if id is not None else str(uuid.uuid4())
        self._user = user
        self._post = post
        self._wathced = wathced
        self._created_at = datetime.now() if created_at is None else created_at

    @property
    def id(self):
        return self._id

    @property
    def user(self):
        return self._user

    @property
    def post(self):
        return self._post

    @property
    def watched(self):
        return self._wathced

    @property
    def created_at(self):
        return self._created_at

    def dict_from_instance(self):
        return {
            'id': self.id,
            'user': self.user,
            'post': self.post,
            'watched': self.watched,
            'created_at': self._created_at,
        }
