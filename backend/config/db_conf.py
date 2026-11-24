from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession,  async_sessionmaker
# 导入基类，用于创建所有models中的表
# from models import Base
# 导入环境变量库
from dotenv import load_dotenv
import os
# 加载 .env 文件，.env 只在当前运行的 FastAPI 进程内有效，外面看不见、拿不到
load_dotenv()

# 从进程中读取环境变量
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# 1. 异步连接URL格式：mysql+aiomysql://账号:密码@主机:端口/库名?字符编码（charset=utf8），推荐.env文件中读取
DATABASE_URL = f"mysql+aiomysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 2. 创建异步数据库引擎
async_engine = create_async_engine(
    DATABASE_URL,
    echo=False,          # echo=True 控制台打印执行的 SQL语句，调试开启、生产关闭
    pool_size=10,       # 连接池常驻连接数
    max_overflow=20,     # 连接池最大溢出临时连接
    pool_recycle=3600    # 连接1小时自动回收，避免MySQL断开空闲连接
)

# 3. 创建异步会话工厂
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,   # 绑定数据库引擎
    class_=AsyncSession,  # 绑定会话类（默认不传绑定AsyncSession类）
    expire_on_commit=False  # 会话对象不过期，不用重新查询数据库
)

# 4. FastAPI依赖：获取单次请求的数据库会话依赖
async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session  # 返回数据库会话给 路由处理函数
            # 路由逻辑执行完成无异常
        except Exception:
            await session.rollback()  # 有异常，回滚事务
            raise

# 异步创建所有数据表（项目启动时再执行）
# async def create_all_tables():
#     async with async_engine.begin() as conn:
#         """
#         Base.metadata 会收集所有模型的表结构信息 → 所有表
#         会一次性创建比如：
#             books
#             users
#             orders
#             ... 所有表。
#         """
#         await conn.run_sync(Base.metadata.create_all)
