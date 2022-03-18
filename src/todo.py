import sqlite3
from datetime import datetime

from pydantic import BaseModel
from src.todo_slack_util import empty_block, list_header_blocks


class Row(sqlite3.Row):
    def dict(self):
        return {x: self[x] for x in self.keys()}


class TODO(BaseModel):
    id: int
    text: str
    created_dt: datetime
    resolved: bool

    class Config:
        orm_mode = True

    def get_slack_block(self):
        yield {"type": "divider"}
        yield {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": f"~{self.text}~" if self.resolved else self.text,
            },
            "accessory": {
                "type": "button",
                "text": {"type": "plain_text", "text": "resolve", "emoji": True},
                "value": f"{self.id}",
                "action_id": "todo-message-action",
            },
        }


class DB:
    q_get = "select * from todo where id = ?"
    q_list = "select * from todo"
    q_list_with_resolved = "select * from todo where resolved = ? order by created_dt desc"
    q_add = "insert into todo (text) values(?)"
    q_resolve = "update todo set resolved = ?, resolved_dt = ? where id = ?"

    def __init__(self):
        self.con = sqlite3.connect("db/sqlite3/todo.db", check_same_thread=False)
        self.con.row_factory = Row

    def list(self):
        for row in self.con.execute(self.q_list_with_resolved, (False,)):
            yield TODO(**row.dict())

    def _get(self, _id, cur):
        for row in cur.execute(self.q_get, (_id,)):
            return TODO(**row.dict())

    def get(self, _id):
        with self.con as con:
            self._get(_id, con.cursor())

    def add(self, text):
        with self.con as con:
            con.execute(self.q_add, (text,))

    def resolve(self, _id):
        with self.con as con:
            con.execute(self.q_resolve, (True, datetime.now(), _id))
            return self._get(_id, con.cursor())


class TODOApp:
    def __init__(self):
        self.db = DB()

    def ls(self):
        blocks = {"blocks": list(list_header_blocks())}
        item_blocks = []
        for msg in self.db.list():
            item_blocks.extend(msg.get_slack_block())
        if not item_blocks:
            item_blocks = [empty_block()]
        item_blocks.append({"type": "divider"})
        blocks["blocks"].extend(item_blocks)
        return blocks

    def add(self, text):
        self.db.add(text)

    def resolve(self, _id):
        self.db.resolve(_id)


def add_todo_command_listener(app):
    todo_app = TODOApp()

    @app.command("/todo")
    def todo(ack, respond, body):
        command, *text = body.get("text").split(None, 1)
        text = text[0] if text else ""
        if command == "ls":
            ack()
            respond(todo_app.ls())
        if command == "add":
            todo_app.add(text)
            ack()
            respond(todo_app.ls())

    @app.action("todo-message-action")
    def resolove_action(ack, action, respond, logger):
        message_id = action.get("value")
        todo_app.resolve(message_id)
        ack()
        respond(todo_app.ls())