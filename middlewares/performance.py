import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

logger = logging.getLogger("app.performance")

class PerformanceMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.perf_counter()
        response = await call_next(request)
        duration = (time.perf_counter() - start_time) * 1000  

        # Пробрасываем в request.state для доступа в эндпоинтах
        request.state.process_time = duration

        # Добавляем в заголовки ответа
        response.headers["X-Process-Time-ms"] = f"{duration:.2f}"

        # Логируем
        logger.info(
            f"{request.method} {request.url.path} "
            f"completed_in={duration:.2f}ms status={response.status_code}"
        )

        return response
