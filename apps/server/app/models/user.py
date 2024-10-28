from datetime import datetime
from typing import Optional
from beanie import Document, Indexed
from pydantic import EmailStr, ConfigDict, Field
from bson import ObjectId

class User(Document):
    id: Optional[str] = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    username: Indexed(str, unique=True)  # 索引且唯一
    email: Indexed(EmailStr, unique=True)  # 索引且唯一
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Settings:
        name = "users"  # 集合名称

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "username": "johndoe",
                "email": "johndoe@example.com",
                "is_active": True,
            }
        },
        populate_by_name=True
    )
