from datetime import datetime


class Follower:
    _id: str
    _follow: str
    _created_at: datetime

    def __init__(self, id: str, follow: str, created_at: datetime = None):
        self._id = id
        self._follow = follow
        self._created_at = datetime.now() if created_at is None else created_at

    @property
    def id(self) -> str:
        return self._id

    @property
    def follow(self) -> str:
        return self._follow

    @property
    def created_at(self) -> datetime:
        return self._created_at
