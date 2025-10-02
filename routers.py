from fastapi import FastAPI

from auth.views import auth_router
from api.views.category import category_router
from api.views.content_version import content_version_router
from api.views.content import content_router
from api.views.example import example_router
from api.views.lesson import lesson_router
from api.views.quiz import quiz_router

app = FastAPI()

app.include_router(category_router)
app.include_router(content_version_router)
app.include_router(content_router)
app.include_router(example_router)
app.include_router(lesson_router)
app.include_router(quiz_router)

app.include_router(auth_router)