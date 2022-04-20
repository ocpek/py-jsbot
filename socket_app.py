from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from src.my import add_my_command_listener
from src.settings import settings
from src.todo import add_todo_command_listener

app = App(token=settings.SOCKET_BOT_TOKEN)
add_todo_command_listener(app)
add_my_command_listener(app)


if __name__ == "__main__":
    handler = SocketModeHandler(app, settings.SOCKET_APP_TOKEN)
    handler.start()
