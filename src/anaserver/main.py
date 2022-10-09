from fastapi import FastAPI
import uvicorn

from anaserver import database
from anaserver.routers import news, users, actions

app = FastAPI(title="AnaNews API", description="API for AnaNews", version="0.1.0")
app.include_router(news.router)
app.include_router(users.router)
app.include_router(actions.router)


@app.on_event("startup")
async def startup():
    await database.init_models()


@app.on_event("shutdown")
async def shutdown():
    pass


@app.get("/")
async def start():
    return "hello"


def start_server():
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    start_server()
