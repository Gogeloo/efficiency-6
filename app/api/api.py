# Create API routes and include them in the main application
from fastapi import APIRouter
from .endpoints.lua import get_lua_file, list_files, post_lua_file

api_router = APIRouter()

api_router.include_router(get_lua_file.router, tags=["Raw Files"], prefix="/lua/file")
api_router.include_router(list_files.router, tags=["Raw Files"], prefix="/lua/list")
api_router.include_router(post_lua_file.router, tags=["Raw Files"], prefix="/lua/file")
