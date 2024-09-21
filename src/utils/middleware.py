from fastapi import HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
import time
from starlette.requests import Request
from starlette.responses import Response


class AuthTimeMiddleware(BaseHTTPMiddleware):
    client_attempt = {}

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        if request.url.path == "/auth/":
            current_time = time.time()

            if request.client.host not in self.client_attempt:
                self.client_attempt[request.client.host] = (1, current_time)
            else:
                attempt, last_visit = self.client_attempt[request.client.host]
                if current_time - last_visit < 30:
                    if attempt >= 3:
                        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
                    else:
                        self.client_attempt[request.client.host] = (attempt + 1, current_time)
                else:
                    self.client_attempt[request.client.host] = (1, current_time)

        response = await call_next(request)
        return response
