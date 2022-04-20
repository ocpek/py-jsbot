class MyAppHelper:
    def help(self):
        return ""

    def ls(self, **kwargs):
        return ""

    def drive(self, *, user):
        # 면허증
        return ""

    def resident(self, *, user):
        # 등본
        return ""

    def credit(self, *, user):
        return ""


def add_my_command_listener(app):
    helper = MyAppHelper()

    @app.command("/my")
    def my(ack, respond, body, logger):
        command, *_ = body.get("text").split(None, 1)
        command = command or "ls"

        user = body.get("user_id")
        if func := getattr(helper, command):
            ack()
            respond(func(user=user))

    # @app.action("my-message-action")
    # def resolove_action(ack, action, body, respond, logger):
    #     user = body.get("user", {}).get("id")
    #     message_id = action.get("value")
    #     todo_app.resolve(message_id)
    #     ack()
    #     respond(todo_app.ls(user))
