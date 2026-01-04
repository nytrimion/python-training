from fastapi import FastAPI

from .routes import router

app = FastAPI(title="API with event and job dispatchers")

app.include_router(router)
