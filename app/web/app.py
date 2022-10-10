from typing import Optional
from aiohttp.web import (
    Application as AiohttpApplication,
    View as AiohttpView,
    Request as AiohttpRequest)

from app.admin.models import Admin
from app.store.database.database import Database
from app.web.config import setup_config, Config


class Application(AiohttpApplication):
    config: Optional[Config] = None
    store: Optional[Store] = None
    database: Optional[Database] = None
    redis: Optional[RedisDatabase] = None


 class Request(AiohttpRequest):
     admin: Optional[Admin] = None

     @property
     def app(self) -> "Application":
         return super().app()


class View(AiohttpView):
    @property
    def request(self) -> Request:
        return super().request

    @property
    def store(self) -> Store:
        return self.request.app.store

    @property
    def data(self) -> dict:
        return self.request.get("data", {})

app = Application()


def setup_app(config_path: str) -> Application:
    setup_config(app, config_path)

