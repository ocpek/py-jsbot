from pydantic import BaseModel, Field
from src.slack_block_kit.object import PlainText


class Element(BaseModel):
    pass


class Button(Element):
    type: str = Field("button", const=True)
    value: str
    action_id: str
    text: PlainText
