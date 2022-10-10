from typing import TYPE_CHECKING

import yaml
from dataclasses import dataclass

if TYPE_CHECKING:
    from app.web.app import Application


@dataclass
class SessionConfig:
    key: bytes


@dataclass
class BotConfig:
    token: str
    group_id: int


@dataclass
class DataBaseConfig:
    host: str = "localhost"
    port: int = 5432
    user: str = "postgres"
    password: str = "postgres"
    database: str = "vkbot"


@dataclass
class RedisConfig:
    host: str
    port: int


@dataclass
class Config:
    session: SessionConfig = None
    bot: BotConfig = None
    database: DataBaseConfig = None
    database_url: str = None
    redis: RedisConfig = None


def setup_config(app: "Application", config_path: str):
    with open(config_path, "r") as f:
        raw_config = yaml.safe_load(f)

    app.config = Config(
        session=SessionConfig(key=raw_config["session"]["key"]),
        bot=BotConfig(token=raw_config["bot"]["token"],
                      group_id=raw_config["bot"]["group_id"]),
        database=DataBaseConfig(host=raw_config["database"]["host"],
                                port=raw_config["database"]["port"],
                                user=raw_config["database"]["user"],
                                password=raw_config["database"]["password"],
                                database=raw_config["database"]["database"]),
        redis=RedisConfig(host=raw_config["redis"]["host"],
                          port=raw_config["redis"]["port"]),
    )
    db_conf = app.config.database
    app.config.database_url = f'postgresql+asyncpg://' \
                              f'{db_conf.user}:{db_conf.password}' \
                              f'@{db_conf.host}:{db_conf.port}/{db_conf.database}'
