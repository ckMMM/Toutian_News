from . import AsyncSession, select
from models.news import Category

# 获取新闻分类列表
async def get_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    stmt = select(Category).offset(skip).limit(limit)
    data = await db.execute(stmt)
    return data.scalars().all()