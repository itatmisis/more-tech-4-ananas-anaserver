from datetime import datetime, timedelta
from typing import List, Union
from uuid import UUID

import numpy as np
import sqlalchemy
from sqlalchemy.ext.asyncio import AsyncSession

from anaserver.models import News, NewsEmbedding, Source, User, UserToNews
from anaserver.models.users_embeddings import UserEmbedding


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


async def get_news_by_id(db: AsyncSession, news_id: UUID) -> News:
    result = await db.execute(sqlalchemy.select(News).where(News.id == news_id))
    return result.scalars().first()


async def get_news_by_ids(db: AsyncSession, news_ids: List[UUID]) -> List[News]:
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


async def get_news_embedding(db: AsyncSession, news_id: UUID) -> NewsEmbedding:
    news_embedding = await db.execute(sqlalchemy.select(NewsEmbedding).where(NewsEmbedding.news_id == news_id))
    return news_embedding.scalars().first()


async def get_user_embedding(db: AsyncSession, user_id: int) -> list:
    user_interactions = await db.execute(sqlalchemy.select(UserToNews).where(UserToNews.user_id == user_id))
    user_interactions = user_interactions.scalars().all()
    user_interacted_news = await db.execute(
        sqlalchemy.select(News).where(
            News.id.in_(sqlalchemy.select(UserToNews.news_id).where(UserToNews.user_id == user_id))
        )
    )
    user_interacted_news = user_interacted_news.scalars().all()
    user_interacted_news_embeddings = await get_news_embeddings(db, [news.id for news in user_interacted_news])
    user_coef = {0: 1, 1: 5, 2: -2}
    user_embedding = np.mean(
        [
            np.array(news_embedding.embedding) * user_coef[news_.action_id]
            for news_embedding, news_ in zip(user_interacted_news_embeddings, user_interactions)
        ],
        axis=0,
    ).tolist()
    return user_embedding


async def get_news_embeddings(db: AsyncSession, news_ids: List[UUID]) -> List[NewsEmbedding]:
    news_embeddings = await db.execute(sqlalchemy.select(NewsEmbedding).where(NewsEmbedding.news_id.in_(news_ids)))
    return news_embeddings.scalars().all()


async def get_all_news(db: AsyncSession) -> List[News]:
    news = await db.execute(sqlalchemy.select(News))
    return news.scalars().all()


async def get_closest_news(
    db: AsyncSession, filtered_news: List[News], embedding: Union[UserEmbedding, NewsEmbedding], n: int
) -> List[News]:
    closest_news = await db.execute(
        sqlalchemy.select(News)
        .where(News.id.in_([news_.id for news_ in filtered_news]))
        .where(
            News.id.in_(
                sqlalchemy.select(NewsEmbedding.news_id)
                .order_by(NewsEmbedding.embedding.cosine_distance(embedding.embedding))
                .limit(n)
            )
        )
        .order_by(News.date.desc())
    )
    return closest_news.scalars().all()


async def get_filtered_news(db: AsyncSession, user_id: int) -> List[News]:
    news = await db.execute(
        sqlalchemy.select(News)
        .where(News.id.notin_(sqlalchemy.select(UserToNews.news_id).where(UserToNews.user_id == user_id)))
        .where(News.date >= (datetime.now() - timedelta(days=7)))
        .where(
            sqlalchemy.select(Source)
            .where(Source.id == News.source_id)
            .where(Source.role_id == sqlalchemy.select(User.role).where(User.id == user_id))
        )
    )
    return news.scalars().all()


async def add_action(db: AsyncSession, user_id: int, news_id: UUID, action_id: int) -> None:
    await db.execute(
        sqlalchemy.insert(UserToNews).values(
            user_id=user_id,
            news_id=news_id,
            action_id=action_id,
        )
    )
    await db.commit()


async def get_news_for_user(db: AsyncSession, user_id: int, n: int) -> List[News]:
    user_embedding = await get_user_embedding(db, user_id)
    filtered_news = await get_filtered_news(db, user_id)
    user_embedding = UserEmbedding(user_id=user_id, embedding=user_embedding)
    closeset_news = await get_closest_news(db, filtered_news, user_embedding, n)
    for news in closeset_news:
        await add_action(db, user_id, news.id, 0)
    return closeset_news


async def get_role_embedding(db: AsyncSession, role_id: int) -> List[float]:
    user_embeddings = await db.execute(
        sqlalchemy.select(UserEmbedding).where(
            UserEmbedding.id.in_(sqlalchemy.select(User.id).where(User.role == role_id))
        )
    )
    user_embeddings_lists = user_embeddings.scalars().all()
    role_embedding = np.mean(
        [np.array(user_embedding.embedding) for user_embedding in user_embeddings_lists], axis=0
    ).tolist()
    return role_embedding


async def get_trends_for_role(db: AsyncSession, role_id: int) -> News:
    role_embedding_list = await get_role_embedding(db, role_id)
    role_embedding: UserEmbedding = UserEmbedding(id=role_id, embedding=role_embedding_list)
    closest_article = await get_closest_news(db, await get_all_news(db), role_embedding, 1)
    return closest_article[0]
