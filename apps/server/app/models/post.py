from datetime import datetime
from typing import Optional, List
from beanie import Document, Indexed, Link, PydanticObjectId
from pydantic import ConfigDict, Field
from bson import ObjectId
from .user import User

class Post(Document):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    title: Indexed(str)  # 为标题创建索引
    content: str
    summary: Optional[str] = None
    published: bool = False
    author_id: str  # 改为 str 类型
    tags: List[str] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Settings:
        name = "posts"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "My First Blog Post",
                "content": "This is my first blog post content",
                "summary": "A brief summary",
                "tags": ["blog", "first post"]
            }
        },
        populate_by_name=True
    )

    async def get_author(self) -> User:
        """获取文章作者"""
        return await User.get(self.author_id)
