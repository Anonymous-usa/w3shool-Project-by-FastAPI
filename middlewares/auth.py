from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from starlette.responses import JSONResponse
from auth.utils import decode_jwt  

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        token = request.headers.get("Authorization")
        user = None

        if token and token.startswith("Bearer "):
            try:
                payload = decode_jwt(token[7:])

                # ⚡ Теперь поддерживаем список ролей
                roles = payload.get("roles", [])
                if isinstance(roles, str):
                    roles = [roles]  # если вдруг пришла одна строка

                user = {
                    "id": payload.get("sub"),
                    "roles": roles
                }

            except Exception:
                return JSONResponse(
                    status_code=401,
                    content={"detail": "Invalid or expired token"}
                )

        request.state.user = user
        return await call_next(request)
