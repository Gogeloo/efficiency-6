from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
import os
import logging
from ....settings import settings  # Adjust this import according to your structure
from ...models.detailed_error_response import DetailedErrorResponseModel
from ...models.file_get_response import GetFileResponseModel

# Initialize logging
logger = logging.getLogger(__name__)

router = APIRouter()


def get_full_file_path(relative_path: str) -> str:
    """
    Construct the full file path and ensure it's within the base directory.
    """
    base_directory = os.path.realpath(settings.path_to_lua_files)
    file_path = os.path.realpath(os.path.join(base_directory, relative_path))

    # Ensure the file path is within the base directory
    if not file_path.startswith(base_directory):
        logger.warning(f"Invalid file path access attempt: {file_path}")
        raise HTTPException(status_code=400, detail="Invalid file path")

    return file_path


def file_exists(file_path: str) -> bool:
    """
    Check if the file exists and is a regular file.
    """
    return os.path.isfile(file_path)


@router.get(
    "/{relative_path:path}",
    response_class=FileResponse,
    responses={
        200: {
            "model": GetFileResponseModel,
            "content": {"application/octet-stream": {}},
            "description": "Lua file successfully retrieved",
        },
        400: {
            "model": DetailedErrorResponseModel,
            "description": "Invalid file path or type",
        },
        404: {"model": DetailedErrorResponseModel, "description": "Lua file not found"},
        500: {
            "model": DetailedErrorResponseModel,
            "description": "Internal server error",
        },
    },
)
async def get_lua_file(relative_path: str):
    """
    Endpoint to retrieve a Lua file by its relative path.
    """
    try:
        file_path = get_full_file_path(relative_path)
        file_path_with_extension = (
            f"{file_path}.lua" if not file_path.endswith(".lua") else file_path
        )

        if not file_exists(file_path) and not file_exists(file_path_with_extension):
            logger.info(
                f"Lua file not found: {file_path} or {file_path_with_extension}"
            )
            raise HTTPException(status_code=404, detail="Lua file not found")

        if file_exists(file_path_with_extension):
            file_path = file_path_with_extension

        logger.info(f"Serving Lua file: {file_path}")
        return FileResponse(file_path)

    except HTTPException as http_exc:
        # Re-raise HTTP exceptions directly
        raise http_exc
    except OSError as e:
        logger.error(f"OS error occurred: {str(e)} | File: {relative_path}")
        response_model = DetailedErrorResponseModel(
            error="Internal Server Error",
            message=f"An OS error occurred while processing the request for file {relative_path}.",
            code=500,
            details=str(e),
        )
        return JSONResponse(status_code=500, content=jsonable_encoder(response_model))
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)} | File: {relative_path}")
        response_model = DetailedErrorResponseModel(
            error="Internal Server Error",
            message=f"An unexpected error occurred while processing the request for file {relative_path}.",
            code=500,
            details=str(e),
        )
        return JSONResponse(status_code=500, content=jsonable_encoder(response_model))
