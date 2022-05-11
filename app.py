import cherrypy
import jwt
import requests
from cherrypy.lib.httputil import urljoin
from cherrypy.lib.static import serve_file
from slack_bolt import App
from slack_bolt.adapter.cherrypy import SlackRequestHandler
from src.my import add_my_command_listener
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
add_my_command_listener(app)


handler = SlackRequestHandler(app)


class AuthApp:
    @cherrypy.expose
    def redirect(self, *args, code, **kwargs):
        response = requests.post(
            "https://kauth.kakao.com/oauth/token",
            data={
                "grant_type": "authorization_code",
                "client_id": "55d107cc13782df053bd65833c0a5357",
                "code": code,
            },
        )
        resp_dict = response.json()
        cookie = cherrypy.response.cookie
        cookie["access_token"] = resp_dict["access_token"]
        cookie["refresh_token"] = resp_dict["refresh_token"]
        cookie["id_token"] = resp_dict["id_token"]
        return response.json()


class SlackApp:
    @cherrypy.expose
    @cherrypy.tools.slack_in()
    def events(self, **kwargs):
        return handler.handle()


class RootApp:
    @classmethod
    def jwt_auth(cls, token):
        if not token:
            raise cherrypy.HTTPError(401, "You are not authorized to access that resource")
        jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])

    @cherrypy.expose
    def serve(self, filepath, token, *args, **kwargs):
        self.jwt_auth(token)
        path = urljoin(settings.SOURCE_ROOT, filepath)
        return serve_file(path)


if __name__ == "__main__":
    cherrypy.config.update({"server.socket_host": "0.0.0.0"})
    cherrypy.config.update({"server.socket_port": settings.PORT})
    cherrypy.tree.mount(RootApp(), "/")
    cherrypy.quickstart(SlackApp(), "/slack")
