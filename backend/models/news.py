# 新闻模型类

from datetime import datetime
from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    created_at = mapped_column(
        DateTime,
        default=datetime.now,
        comment="创建时间"
    )
    updated_at = mapped_column(
        DateTime,
        default=datetime.now,
        onupdate=datetime.now,
        comment="更新时间"
    )

# 分类列表
class Category(Base):
    __tablename__ = "news_category"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, comment="分类ID")
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, comment="分类名称")
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0, comment="排序顺序")
    # 设置__repr__内置魔法方法，调试、日志、打印对象时用
    # 给模型一个 “可读的自我介绍”，方便调试，不影响业务逻辑
    def __repr__(self):
        return f"<Category(id={self.id}, name={self.name}, sort_order={self.sort_order})>"
