from . import *
from crud import news

router = APIRouter(prefix="/api/news", tags=["news"])

# 1. 获取新闻分类列表
@router.get("/categories")
async def get_categories(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    categories = await news.get_categories(db, skip, limit)
    return {
        "code": 200,
        "message": "success",
        "data": categories
    }
