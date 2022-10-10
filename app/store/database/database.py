from typing import TYPE_CHECKING, Optional

from gino import Gino
from sqlalchemy.ext.asyncio import (AsyncEngine,
                                    AsyncSession,
                                    create_async_engine)
from sqlalchemy.orm import sessionmaker

from app.store.database.gino_base import db

if TYPE_CHECKING:
    from app.web.app import Application


class Database:
    def __init__(self, app: "Application"):
        self.app = app
        self._engine: Optional[AsyncEngine] = None
        self._db: Optional[Gino] = None
        self.session: Optional[sessionmaker] = None

    async def connect(self, *_: list, **__: dict) -> None:
        self._db = db
        self._engine = create_async_engine(
            self.app.config.database_url,
            echo=True,
            future=True
        )
        self.session = sessionmaker(self._engine,
                                    expire_on_commit=False,
                                    class_=AsyncSession)

    async def disconnect(self, *_: list, **__: dict) -> None:
        if self._engine:
            await self._engine.dispose()
