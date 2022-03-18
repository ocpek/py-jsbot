import cherrypy
from slack_bolt import App
from slack_bolt.adapter.cherrypy import SlackRequestHandler
from src.settings import settings
from src.todo import add_todo_command_listener

app = App(token=settings.SLACK_APP_TOKEN, signing_secret=settings.SLACK_SIGNING_SECRET)


@app.event("message")
def message_test(message, logger, *args, **kwargs):
    ts = message["ts"]
    text = message.get("text")
    channel = message["channel"]
    bot_id = message.get("bot_id")
    print(ts, text, channel, bot_id)
    if not bot_id or bot_id != "B033JFZE4Q2":
        return

    if channel == "C033X1649LH":
        pass  # github

    if channel == "D02SC7NEATD":
        pass  # todo


add_todo_command_listener(app)


handler = SlackRequestHandler(app)


class SlackApp(object):
    @cherrypy.expose
    @cherrypy.tools.slack_in()
    def events(self, **kwargs):
        return handler.handle()


wsgiapp = cherrypy.tree.mount(SlackApp(), "/slack")


if __name__ == "__main__":
    cherrypy.config.update({"server.socket_port": settings.PORT})
    cherrypy.quickstart(SlackApp(), "/slack")
