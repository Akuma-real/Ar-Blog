from typing import List, Any
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate, PostResponse, PostInDB
from app.api.deps import get_current_active_user, get_current_superuser
from app.models.user import User
from beanie import PydanticObjectId

router = APIRouter()

async def prepare_post_response(post: Post) -> PostResponse:
    """准备文章响应数据"""
    author = await post.get_author()
    post_dict = post.model_dump()
    post_dict["author"] = author
    return PostResponse(**post_dict)

@router.post("", response_model=PostResponse)
async def create_post(
    post_in: PostCreate,
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """创建新文章 (仅管理员)"""
    post = Post(
        **post_in.model_dump(),
        author_id=str(current_user.id)  # 转换为字符串
    )
    await post.insert()
    return await prepare_post_response(post)

@router.get("", response_model=List[PostResponse])
async def get_posts(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    published: bool = Query(default=True),
) -> Any:
    """获取文章列表 (公开接口)"""
    query = {"published": published} if published else {}
    posts = await Post.find(query).skip(skip).limit(limit).to_list()
    return [await prepare_post_response(post) for post in posts]

@router.get("/drafts", response_model=List[PostResponse])
async def get_drafts(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """获取草稿列表 (仅管理员)"""
    posts = await Post.find({"published": False}).skip(skip).limit(limit).to_list()
    return [await prepare_post_response(post) for post in posts]

@router.get("/{post_id}", response_model=PostResponse)
async def get_post(post_id: str) -> Any:
    """获取特定文章 (公开接口，但只能查看已发布的文章)"""
    post = await Post.get(post_id)
    if not post or (not post.published):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    return await prepare_post_response(post)

@router.get("/{post_id}/draft", response_model=PostResponse)
async def get_draft(
    post_id: str,
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """获取草稿 (仅管理员)"""
    post = await Post.get(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    # 如果文章已发布，返回404错误
    if post.published:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="This is not a draft"
        )
    
    return await prepare_post_response(post)

@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: str,
    post_in: PostUpdate,
    current_user: User = Depends(get_current_superuser)
) -> Any:
    """更新文章 (仅管理员)"""
    post = await Post.get(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    update_data = post_in.model_dump(exclude_unset=True)
    if update_data:
        update_data["updated_at"] = datetime.utcnow()
        await post.update({"$set": update_data})
        post = await Post.get(post_id)
    
    return await prepare_post_response(post)

@router.delete("/{post_id}")
async def delete_post(
    post_id: str,
    current_user: User = Depends(get_current_superuser)
) -> dict:
    """删除文章 (仅管理员)"""
    post = await Post.get(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post not found"
        )
    
    await post.delete()
    return {"status": "success"}
