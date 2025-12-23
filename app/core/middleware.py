import uuid

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from app.utils.mdc import set_request_id, set_user_id


class MDCMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
        user_id = request.headers.get("X-User-ID", "anonymous")

        set_request_id(request_id)
        set_user_id(user_id)

        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id
        return response
