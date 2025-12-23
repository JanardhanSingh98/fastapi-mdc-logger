from contextvars import ContextVar

request_id_ctx = ContextVar("request_id", default=None)
user_id_ctx = ContextVar("user_id", default=None)


def set_request_id(request_id: str):
    request_id_ctx.set(request_id)


def set_user_id(user_id: str):
    user_id_ctx.set(user_id)


def get_mdc():
    return {
        "request_id": request_id_ctx.get(),
        "user_id": user_id_ctx.get(),
    }
