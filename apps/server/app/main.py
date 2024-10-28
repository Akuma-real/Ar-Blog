from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import init_db
from app.api.v1 import auth, posts

app = FastAPI(
    title="Ar-Blog API",
    description="Backend API for Ar-Blog",
    version="0.1.0"
)

# CORS设置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中要设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def start_db():
    await init_db()

# 注册路由
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(posts.router, prefix="/api/v1/posts", tags=["posts"])

@app.get("/")
async def root():
    return {"message": "Welcome to Ar-Blog API"}
