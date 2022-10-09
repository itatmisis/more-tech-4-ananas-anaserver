from typing import List

from fastapi import FastAPI, HTTPException
import uvicorn

import anaserver.crud as crud  # noqa
import anaserver.database as database
import anaserver.models as models
import anaserver.schemas as schemas

app = FastAPI(title="AnaNews API", description="API for AnaNews", version="0.1.0")


@app.on_event("startup")
async def startup():
    await database.init_models()


@app.on_event("shutdown")
async def shutdown():
    pass


@app.get("/")
async def start():
    return "hello"


@app.get("/news", response_model=List[schemas.News])
async def news():
    try:
        async with database.get_session() as db:
            news_orm: List[models.News] = await crud.get_all_news(db)
            news = [schemas.News.from_orm(news) for news in news_orm]
            return news
    except Exception:
        raise HTTPException(status_code=500, detail="Error while getting news")


@app.post("/user", response_model=List[schemas.User])
async def add_user(user: schemas.UserCreate):
    try:
        async with database.get_session() as db:
            user_orm = models.User(id=user.id, role_id=user.role_id)
            result = await crud.add_user(db, user_orm)
            return result
    except Exception:
        raise HTTPException(status_code=500, detail="Error while adding user")


def start_server():
    uvicorn.run(app, host="127.0.0.1", port=8000)


if __name__ == "__main__":
    start_server()
