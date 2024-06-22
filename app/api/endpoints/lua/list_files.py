from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import os
import logging
from ....settings import settings  # Adjust this import according to your structure
from ...models.file_list_response import GetFileListResponseModel
from ...models.detailed_error_response import DetailedErrorResponseModel

# Initialize logging
logger = logging.getLogger(__name__)

router = APIRouter()


def list_lua_files(directory: str) -> list:
    """
    List all Lua files in the specified directory and its subdirectories.
    """
    lua_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".lua"):
                relative_path = os.path.relpath(os.path.join(root, file), directory)
                lua_files.append(relative_path)
    return lua_files


@router.get(
    "/",
    response_model=GetFileListResponseModel,
    responses={
        200: {"description": "List of Lua files successfully retrieved"},
        500: {
            "model": DetailedErrorResponseModel,
            "description": "Internal server error",
        },
    },
)
async def get_lua_file_list():
    """
    Endpoint to retrieve a list of all Lua files available, including subdirectories.
    """
    try:
        base_directory = os.path.realpath(settings.path_to_lua_files)
        lua_files = list_lua_files(base_directory)
        return GetFileListResponseModel(files=lua_files)

    except OSError as e:
        logger.error(f"OS error occurred: {str(e)} while listing Lua files.")
        response_model = DetailedErrorResponseModel(
            error="Internal Server Error",
            message="An OS error occurred while listing Lua files.",
            code=500,
            details=str(e),
        )
        return JSONResponse(status_code=500, content=jsonable_encoder(response_model))
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)} while listing Lua files.")
        response_model = DetailedErrorResponseModel(
            error="Internal Server Error",
            message="An unexpected error occurred while listing Lua files.",
            code=500,
            details=str(e),
        )
        return JSONResponse(status_code=500, content=jsonable_encoder(response_model))
