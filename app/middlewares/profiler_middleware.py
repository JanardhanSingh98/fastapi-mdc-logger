from pyinstrument import Profiler
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware


class ProfilerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        profiler = Profiler()
        profiler.start()

        response = await call_next(request)

        profiler.stop()
        print(profiler.output_text(unicode=True, color=True))
        return response
