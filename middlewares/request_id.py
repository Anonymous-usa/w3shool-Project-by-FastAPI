import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Берём существующий X-Request-ID или генерируем новый
        request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))

        # Сохраняем в request.state
        request.state.request_id = request_id

        # Пробрасываем дальше
        response = await call_next(request)

        # Добавляем в заголовки ответа
        response.headers["X-Request-ID"] = request_id
        return response
