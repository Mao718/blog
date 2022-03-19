from fastapi import FastAPI
from .apis import APIrouter


def create_app():
    app = FastAPI()
    return app


app = create_app()
app.include_router(APIrouter)
