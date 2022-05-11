from src.common import SlackBaseAppHelper


class MyAppHelper(SlackBaseAppHelper):
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
        # 면허증
        return self.message(
            [
                self.image(image_url="http://kekeke.co.kr/serve?filepath=driver_front.jpg", alt_text=""),
                self.image(image_url="http://kekeke.co.kr/serve?filepath=driver_back.jpg", alt_text=""),
            ]
        )

    def resident(self, *, user):
        # 등본
        return self.message(
            [
                self.image(image_url="http://kekeke.co.kr/serve?filepath=resident_1.jpg", alt_text=""),
                self.image(image_url="http://kekeke.co.kr/static/filepath=resident_2.jpg", alt_text=""),
            ]
        )

    def credit(self, *, user):
        return self.message(
            [self.image(image_url="https://api.slack.com/img/blocks/bkb_template_images/tripAgent_1.png", alt_text="")]
        )


def add_my_command_listener(app):
    helper = MyAppHelper()

    @app.command("/my")
    def my(ack, respond, body, logger):
        print(body)
        try:
            command, *_ = body.get("text").split(None, 1)
        except ValueError:
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
