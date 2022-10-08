from typing import List

import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from anaserver.models import News, NewsEmbedding, User, UserToNews


async def get_user(db: AsyncSession, user_id: int) -> User:
    result = await db.execute(sqlalchemy.select(User).where(User.id == user_id))
    return result.scalars().first()


async def add_user(db: AsyncSession, user: User) -> User:
    db.add(user)
    await db.commit()
    return user


async def get_users(db: AsyncSession) -> List[User]:
    result = await db.execute(sqlalchemy.select(User))
    return result.scalars().all()


async def get_users_by_role(db: AsyncSession, role_id: int) -> List[User]:
    result = await db.execute(sqlalchemy.select(User).where(User.role == role_id))
    return result.scalars().all()


async def get_news_by_user(db: AsyncSession, user_id: int) -> List[News]:
    news_ids = await db.execute(sqlalchemy.select(UserToNews.news_id).where(UserToNews.user_id == user_id))
    news_ids = news_ids.scalars().all()
    news = await db.execute(sqlalchemy.select(News).where(News.id.in_(news_ids)))
    return news.scalars().all()


async def get_news_by_id(db: AsyncSession, news_id: int) -> News:
    result = await db.execute(sqlalchemy.select(News).where(News.id == news_id))
    return result.scalars().first()


async def get_news_by_ids(db: AsyncSession, news_ids: list) -> List[News]:
    news = await db.execute(sqlalchemy.select(News).where(News.id.in_(news_ids)))
    return news.scalars().all()


async def get_news_by_role(db: AsyncSession, role_id: int) -> List[News]:
    news_ids = await db.execute(
        sqlalchemy.select(UserToNews.news_id).where(
            UserToNews.user_id.in_(sqlalchemy.select(User.id).where(User.role == role_id))
        )
    )
    news_ids = news_ids.scalars().all()
    news = await get_news_by_ids(db, news_ids)
    return news


async def get_news_embedding(db: AsyncSession, news_id: int):
    news_embedding = await db.execute(sqlalchemy.select(NewsEmbedding).where(NewsEmbedding.news_id == news_id))
    return news_embedding.scalars().first()


async def get_news_embeddings(db: AsyncSession, news_ids: list):
    news_embeddings = await db.execute(sqlalchemy.select(NewsEmbedding).where(NewsEmbedding.news_id.in_(news_ids)))
    return news_embeddings.scalars().all()


async def get_all_news(db: AsyncSession):
    news = await db.execute(sqlalchemy.select(News))
    return news.scalars().all()


async def get_closest_news(db: AsyncSession, news_id: int, n: int):
    news_embedding = await get_news_embedding(db, news_id)
    closest_news = await db.execute(
        sqlalchemy.select(News).where(
            News.id.in_(
                sqlalchemy.select(NewsEmbedding.news_id)
                .order_by(NewsEmbedding.embedding.cosine_distance(news_embedding.embedding))
                .limit(n)
            )
        )
    )
    return closest_news.scalars().all()
