import uvicorn

from routers import app


if __name__ == "__main__":
    uvicorn.run("manage:app", host="localhost", port=8000, reload=True)