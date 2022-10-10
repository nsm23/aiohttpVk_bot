from dataclasses import dataclass
from hashlib import sha256
from typing import Optional

from sqlalchemy import Column, Integer, String

from app.store.database.gino_base import db


@dataclass
class Admin:
    id: int
    email: str
    password: Optional[sha256] = None

    def password_is_valid(self, password: str):
        return self.password == sha256(password.encode()).hexdigest()


class AdminModel(db):
    __tablename__ = "admin"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    def to_dc(self) -> Admin:
        return Admin(
            id=self.id,
            email=self.email,
            password=self.password
        )

