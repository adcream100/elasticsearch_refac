import logging
import time
import json
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from starlette.types import ASGIApp

class AccessLoggingMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp):
        super().__init__(app)
        self.logger = logging.getLogger("api.access")

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        req_body = await self._get_request_body(request)
        client_host = request.client.host if request.client else "unknown"

        self.logger.info(
            f"[REQUEST] {request.method} {request.url.path} | "
            f"From: {client_host} | Body: {req_body}"
        )

        try:
            response = await call_next(request)
            duration = int((time.time() - start_time) * 1000)
            resp_body = await self._get_response_body(response)
            self.logger.info(
                f"[RESPONSE] {request.method} {request.url.path} | "
                f"Status: {response.status_code} | Time: {duration}ms | Body: {resp_body}"
            )
            return response

        except Exception as e:
            duration = int((time.time() - start_time) * 1000)
            self.logger.exception(
                f"[ERROR] {request.method} {request.url.path} | "
                f"Error: {str(e)} | Time: {duration}ms"
            )
            raise

    async def _get_request_body(self, request: Request):
        try:
            body = await request.body()

            try:
                parsed = json.loads(body.decode())
                return json.dumps(parsed)[:300]
            except Exception:
                return body.decode()[:300]
        except Exception:
            return "[unavailable]"

    async def _get_response_body(self, response: Response):

        if hasattr(response, "body_iterator"):
            return "[streaming/large body]"
        try:
            body = b""
            async for chunk in response.body_iterator:
                body += chunk
                if len(body) > 512:
                    break
            return body.decode(errors="ignore")[:300]
        except Exception:
            return "[unavailable]"
