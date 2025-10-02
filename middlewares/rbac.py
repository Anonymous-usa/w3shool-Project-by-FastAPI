from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from starlette.responses import JSONResponse
from permissions import ROLE_PERMISSIONS

class RBACMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        user = getattr(request.state, "user", None)
        if not user:
            return JSONResponse(status_code=401, content={"detail": "Unauthorized"})

        roles = user.get("roles", [])
        if not roles:
            return JSONResponse(status_code=403, content={"detail": "No roles assigned"})

        # Определяем permission по пути и методу
        method = request.method.lower()
        path = request.url.path.strip("/").split("/")[0]  # первый сегмент пути

        if method == "get":
            permission = f"{path}:view"
        elif method == "post":
            permission = f"{path}:create"
        elif method in ("put", "patch"):
            permission = f"{path}:update"
        elif method == "delete":
            permission = f"{path}:delete"
        else:
            permission = f"{path}:{method}"

        # Проверяем все роли пользователя
        for role in roles:
            allowed = ROLE_PERMISSIONS.get(role, [])
            if "*" in allowed or permission in allowed:
                return await call_next(request)

        return JSONResponse(status_code=403, content={"detail": "Forbidden"})
