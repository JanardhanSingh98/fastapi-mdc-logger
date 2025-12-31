import asyncio
import time
from pathlib import Path

from fastapi import Request
from pyinstrument import Profiler
from starlette.middleware.base import BaseHTTPMiddleware


class ProfilerMiddleware(BaseHTTPMiddleware):
    """
    Safe async profiler middleware.
    - One profiler per request
    - Single aggregated HTML output
    """

    _write_lock = asyncio.Lock()

    def __init__(
        self,
        app,
        enabled: bool = False,
        output_file: str = "profiling/profile.html",
    ):
        super().__init__(app)
        self.enabled = enabled
        self.output_file = output_file
        Path(output_file).parent.mkdir(exist_ok=True)

        if enabled:
            # Initialize file once
            if not Path(output_file).exists():
                Path(output_file).write_text("<html><body>\n")

    async def dispatch(self, request: Request, call_next):
        if not self.enabled:
            return await call_next(request)

        profiler = Profiler(interval=0.001, async_mode="enabled")
        profiler.start()

        start = time.perf_counter()
        response = await call_next(request)
        duration = time.perf_counter() - start

        profiler.stop()

        html = profiler.output_html()
        print(profiler.output_text(unicode=True, color=True))

        async with ProfilerMiddleware._write_lock:
            with open(self.output_file, "a") as f:
                f.write(
                    f"<h2>{request.method} {request.url.path} "
                    f"({duration:.3f}s)</h2>\n"
                )
                f.write(html)
                f.write("<hr/>\n")

        return response
