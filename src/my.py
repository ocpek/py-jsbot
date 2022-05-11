from datetime import datetime, timedelta

import jwt
from src.common import SlackBaseAppHelper
from src.settings import settings


class MyAppHelper(SlackBaseAppHelper):
    @classmethod
    def create_token(cls, user):
        return jwt.encode(
            {"user": user, "exp": datetime.now() + timedelta(seconds=10)}, settings.JWT_SECRET, algorithm="HS256"
        )

    def help(self, **kwargs):
        return self.message(
            [
                self.section(
                    "\n".join(
                        [
                            "• /my ls",
                            "• /my drive",
                            "• /my resident",
                            "• /my credit",
                        ]
                    )
                )
            ]
        )

    def ls(self, **kwargs):
        return self.message(
            [
                self.header("my info"),
                self.actions(
                    [
                        self.button(text="면허증", value="1", action_id="drive-action"),
                        self.button(text="등본", value="1", action_id="resident-action"),
                        self.button(text="신용카드", value="1", action_id="credit-action"),
                    ]
                ),
            ]
        )

    def drive(self, *, user):
        jwt_token = self.create_token(user)
        # 면허증
        return self.message(
            [
                self.image(
                    image_url=f"http://kekeke.co.kr/serve?filepath=driver_front.jpg&token={jwt_token}", alt_text=""
                ),
                self.image(
                    image_url=f"http://kekeke.co.kr/serve?filepath=driver_back.jpg&token={jwt_token}", alt_text=""
                ),
            ]
        )

    def resident(self, *, user):
        jwt_token = self.create_token(user)
        # 등본
        return self.message(
            [
                self.image(
                    image_url=f"http://kekeke.co.kr/serve?filepath=resident_1.jpg?token={jwt_token}", alt_text=""
                ),
                self.image(
                    image_url=f"http://kekeke.co.kr/static/filepath=resident_2.jpg?token={jwt_token}", alt_text=""
                ),
            ]
        )

    def credit(self, *, user):
        jwt_token = self.create_token(user)
        return self.message(
            [
                self.image(image_url=f"http://kekeke.co.kr/serve?filepath=credit_1.jpg?token={jwt_token}", alt_text=""),
                self.image(image_url=f"http://kekeke.co.kr/serve?filepath=credit_2.jpg?token={jwt_token}", alt_text=""),
            ]
        )


def add_my_command_listener(app):
    helper = MyAppHelper()

    @app.command("/my")
    def my(ack, respond, body, logger):
        print(body)
        try:
            command, *_ = body.get("text").split(None, 1)
        except (ValueError, AttributeError):
            command = "ls"

        user = body.get("user_id")
        if func := getattr(helper, command):
            ack()
            if msg := func(user=user):
                print(msg)
                respond(msg)

    @app.action("drive-action")
    def drive_action(ack, action, body, respond, logger):
        user = body.get("user", {}).get("id")
        message_id = action.get("value")
        print(message_id)
        ack()
        respond(helper.drive(user=user))

    @app.action("resident-action")
    def resident_action(ack, action, body, respond, logger):
        user = body.get("user", {}).get("id")
        message_id = action.get("value")
        print(message_id)
        ack()
        respond(helper.resident(user=user))

    @app.action("credit-action")
    def credit_action(ack, action, body, respond, logger):
        user = body.get("user", {}).get("id")
        message_id = action.get("value")
        print(message_id)
        ack()
        respond(helper.credit(user=user))
