import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

logger = logging.getLogger("app.errors")

class ErrorHandlerMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        try:
            return await call_next(request)
        except Exception as e:
            logger.exception("Unhandled error")
            return JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error", "error": str(e)},
            )
