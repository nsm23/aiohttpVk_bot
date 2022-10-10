import time

from aiohttp.web_exceptions import HTTPNotImplemented
from aiohttp_apispec import (docs,
                             response_schema,
                             request_schema)
from aiohttp_session import new_session

from app.admin.schemes import (AdminResponseSchema,
                               AdminRequestSchema,
                               AdminResponseDataSchema)
from app.web.app import View
from app.web.mixins import AuthRequiredMixin
from app.web.utils import authenticate, json_response


class AdminLoginView(View):
    @docs(tags=["admin"],
          summary="Auth",
          description="Auth admin")
    @response_schema(AdminResponseSchema, 200)
    @request_schema(AdminRequestSchema)
    async def post(self):
        app = self.request.app
        data = self.request['data']
        email = data['email']
        password = data['password']

        admin = await authenticate(email, password, app)
        session = await new_session(self.request)
        session['last_visit'] = time.time()
        session['email'] = email

        return json_response(data=AdminResponseDataSchema().dumps(admin))

    async def get(self):
        raise HTTPNotImplemented(text="method 'get' not implemented")

    
@docs(tags=['admin'],
      summary="Who am i",
      description='current admin')
@response_schema(AdminResponseSchema, 200)
class AdminCurrentView(View, AuthRequiredMixin):
    async def post(self):
        raise HTTPNotImplemented(text="method 'post' not implemented")

    async def get(self):
        admin = await self.check_auth()
        return json_response(data=AdminResponseDataSchema().dumps(admin))


