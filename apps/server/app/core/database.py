from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import settings
from app.models.user import User
from app.models.post import Post  # 添加这行

async def init_db():
    # 创建 MongoDB 连接
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    # 初始化 beanie，注册所有模型
    await init_beanie(
        database=client[settings.MONGODB_DB_NAME],
        document_models=[User, Post]  # 添加 Post
    )
