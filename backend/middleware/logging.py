from http import HTTPStatus

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

from backend.logging import log


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        log.info(f"{request.client.host}:{request.client.port} | {request.method} {request.url.path} - {response.status_code} "
                 f"{HTTPStatus(response.status_code).phrase}")

        return response