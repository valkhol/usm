from pydantic import BaseModel, typing

from app.dto.post import PostOut


class StripOutlist(BaseModel):
    strip: typing.List[typing.Dict[str, typing.Union[str, PostOut]]]

    class Config:
        orm_mode = True
