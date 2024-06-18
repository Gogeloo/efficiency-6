# Create API routes and include them in the main application
from fastapi import APIRouter
from .endpoints.computer_information import get_active_computers

api_router = APIRouter()

api_router.include_router(get_active_computers.router, tags=[
                          "Computer Information"], prefix="/info")
