# Create API routes and include them in the main application
from fastapi import APIRouter
from .endpoints.lua import lua_file, list_files

api_router = APIRouter()

api_router.include_router(lua_file.router, tags=["Raw Files"], prefix="/lua/file")
api_router.include_router(list_files.router, tags=["Raw Files"], prefix="/lua/list")
