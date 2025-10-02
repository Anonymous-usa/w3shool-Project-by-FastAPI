from fastapi import FastAPI

from auth.views import auth_router
from api.views.category import category_router
from api.views.content_version import content_version_router
from api.views.content import content_router
from api.views.example import example_router
from api.views.lesson import lesson_router
from api.views.quiz import quiz_router



from middlewares.cors import setup_cors
from middlewares.logging import LoggingMiddleware
from middlewares.request_id import RequestIDMiddleware
from middlewares.auth import AuthMiddleware
from middlewares.errors import ErrorHandlerMiddleware
from middlewares.performance import PerformanceMiddleware

app = FastAPI()

#Custom routers
app.include_router(category_router)
app.include_router(content_version_router)
app.include_router(content_router)
app.include_router(example_router)
app.include_router(lesson_router)
app.include_router(quiz_router)
app.include_router(auth_router)

#CORS
setup_cors(app)

#Custom middlewares
app.add_middleware(LoggingMiddleware)
app.add_middleware(RequestIDMiddleware)
app.add_middleware(AuthMiddleware)
app.add_middleware(ErrorHandlerMiddleware)
app.add_middleware(PerformanceMiddleware)