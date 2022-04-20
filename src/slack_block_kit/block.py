from __future__ import annotations

from typing import Optional

from pydantic import BaseModel, Field
from src.slack_block_kit.element import Element
from src.slack_block_kit.object import PlainText, Text


class Message(BaseModel):
    blocks: list[Block]


class Block(BaseModel):
    pass


class Header(Block):
    type: str = Field("header", const=True)
    text: PlainText
    block_id: str = ""


class Section(Block):
    type: str = Field("section", const=True)
    text: Text
    block_id: str = ""
    accessory: Optional[Element]


class Actions(Block):
    type: str = Field("actions", const=True)
    elements: list[Element]
    block_id: str = ""


class Image(Block):
    type: str = Field("image", const=True)
    image_url: str
    title: Optional[PlainText]
    alt_text: str = ""
    block_id: str = ""


class Divider(Block):
    type: str = Field("divider", const=True)
