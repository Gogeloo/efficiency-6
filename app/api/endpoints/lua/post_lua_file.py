from fastapi import APIRouter, HTTPException, Form, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import logging
from datetime import datetime
from ....settings import settings  # Adjust this import according to your structure
from ...models.detailed_error_response import DetailedErrorResponseModel
from fastapi.encoders import jsonable_encoder

# Initialize logging
logger = logging.getLogger(__name__)

router = APIRouter()
security = HTTPBearer()


def save_file_content(file_content: str, file_path: str) -> None:
    """
    Save the provided file content to the specified file path.
    """
    try:
        with open(file_path, "w") as buffer:
            buffer.write(file_content)
    except Exception as e:
        raise OSError(f"Error saving file: {str(e)}")


def validate_path(path: str) -> str:
    """
    Sanitize and validate the file path.
    """
    if ".." in path or path.startswith("/"):
        raise ValueError("Invalid file path")
    return path


def validate_content(content: str) -> str:
    """
    Sanitize and validate the file content.
    """
    # Additional content validation logic can be added here
    return content


def get_auth_key(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Dependency to check the authentication key.
    """
    if credentials.credentials != settings.auth_key:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return credentials.credentials


@router.post(
    "/create",
    responses={
        201: {"description": "File successfully created"},
        400: {
            "model": DetailedErrorResponseModel,
            "description": "Invalid file path or type",
        },
        409: {
            "model": DetailedErrorResponseModel,
            "description": "File already exists",
        },
        500: {
            "model": DetailedErrorResponseModel,
            "description": "Internal server error",
        },
    },
)
async def create_lua_file(
    content: str = Form(...),
    path: str = Form(...),
    auth_key: str = Depends(get_auth_key),
):
    """
    Endpoint to create a new Lua file in the specified directory.
    """
    try:
        path = validate_path(path)
        content = validate_content(content)

        base_directory = os.path.realpath(settings.path_to_lua_files)
        file_path = os.path.realpath(os.path.join(base_directory, path))

        # Ensure the file path is within the base directory
        if not file_path.startswith(base_directory):
            logger.warning(f"Invalid file path access attempt: {file_path}")
            raise HTTPException(status_code=400, detail="Invalid file path")

        # Ensure the file has a .lua extension
        if not file_path.endswith(".lua"):
            logger.warning(f"Invalid file type attempt: {file_path}")
            raise HTTPException(
                status_code=400,
                detail="Invalid file type. Only .lua files are allowed.",
            )

        # Check if the file already exists
        if os.path.exists(file_path):
            logger.warning(f"File already exists: {file_path}")
            raise HTTPException(status_code=409, detail="File already exists")

        # Save the file content
        save_file_content(content, file_path)

        logger.info(f"File successfully created: {file_path}")
        return JSONResponse(
            status_code=201, content={"message": "File successfully created"}
        )

    except ValueError as ve:
        logger.warning(f"Validation error: {str(ve)}")
        raise HTTPException(status_code=400, detail=str(ve))
    except HTTPException as http_exc:
        # Re-raise HTTP exceptions directly
        raise http_exc
    except OSError as e:
        logger.error(f"OS error occurred: {str(e)} while creating file: {path}")
        response_model = DetailedErrorResponseModel(
            error="Internal Server Error",
            message="An OS error occurred while creating the file.",
            code=500,
            details=str(e),
        )
        return JSONResponse(status_code=500, content=jsonable_encoder(response_model))
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)} while creating file: {path}")
        response_model = DetailedErrorResponseModel(
            error="Internal Server Error",
            message="An unexpected error occurred while creating the file.",
            code=500,
            details=str(e),
        )
        return JSONResponse(status_code=500, content=jsonable_encoder(response_model))
