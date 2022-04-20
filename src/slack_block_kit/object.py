from typing import Literal

from pydantic import BaseModel, Field


class Object(BaseModel):
    pass


class Text(Object):
    type: Literal["mrkdwn", "plain_text"] = "mrkdwn"
    text: str
    emoji: bool = True


class PlainText(Object):
    type: str = Field("plain_text", const=True)
    emoji: bool = True
    text: str
