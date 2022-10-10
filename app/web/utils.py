from typing import TYPE_CHECKING, Any, Optional
import json
from hashlib import sha256

from aiohttp.web import json_response as aiohttp_json_response
from aiohttp.web_exceptions import HTTPForbidden
from aiohttp.web_response import Response

from app.admin.models import Admin
from app.store.admin.accessor import NotRegistered

if TYPE_CHECKING:
    from app.web.app import Application


def json_response(data: Any, status: str = "ok") -> Response:
    if data is None:
        data = {}
    return aiohttp_json_response(data={"status": status,
                                       "data": data})


def error_json_response(http_status: int,
                        status: str = "error",
                        message: Optional[str] = None,
                        data: Optional[dict] = None):
    if data is None:
        data = {}
    return aiohttp_json_response(status=http_status,
                                 data={"status": status,
                                       "message": str(message),
                                       "data": data})


async def authenticate(email: str, password: str, app: "Application"):
    try:
        admin = await app.store.admins.get_by_email(email)
    except NotRegistered:
        raise HTTPForbidden(text="Wrong email or password")
    if admin.password_is_valid(password):
        return admin
    else:
        return HTTPForbidden(text="Wrong password")


def get_text_exceptions(e: Exception) -> Optional[str]:
    try:
        data = json.loads(e.text)
    except Exception:
        data = e.text
    return data
