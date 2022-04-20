from pydantic import BaseSettings


class Settings(BaseSettings):
    SLACK_USER_TOKEN: str
    SLACK_SIGNING_SECRET: str
    SLACK_BOT_TOKEN: str
    SLACK_APP_TOKEN: str
    PORT: int
    SOCKET_BOT_TOKEN: str
    SOCKET_APP_TOKEN: str

    class Config:
        env_file = ".env"


settings: Settings = Settings()
