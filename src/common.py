from src.slack_block_kit.block import Actions, Block, Divider, Header, Image, Message, Section
from src.slack_block_kit.element import Button, Element
from src.slack_block_kit.object import PlainText, Text


class SlackBaseAppHelper:
    def message(self, blocks: list[Block]):
        Message.update_forward_refs()
        msg = Message(blocks=blocks)
        return msg.dict()

    def section(self, text: Text) -> Section:
        return Section(text=text)

    def button(self, text: str, value, action_id) -> Button:
        return Button(
            text=PlainText(text=text),
            value=value,
            action_id=action_id,
        )

    def divider(self) -> Divider:
        return Divider()

    def actions(self, btn_list: list[Element]) -> Actions:
        return Actions(elements=btn_list)

    def header(self, text: str) -> Header:
        return Header(text=PlainText(text=text))

    def image(self, image_url, alt_text, title=" ") -> Image:
        return Image(image_url=image_url, title=PlainText(text=title), alt_text=alt_text)
