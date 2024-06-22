from fastapi import APIRouter, HTTPException, Depends, Body
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import os
import logging
from ....settings import Settings
from ...models.detailed_error_response import DetailedErrorResponseModel
from ...models.file_create_response import PostFileRequestModel, PostFileResponseModel
from fastapi.encoders import jsonable_encoder
from typing import Annotated

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


def ensure_directory_exists(file_path: str) -> None:
    """
    Ensure that the directory for the file path exists.
    """
    directory = os.path.dirname(file_path)
    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception as e:
            raise OSError(f"Error creating directory: {str(e)}")


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
    if credentials.credentials != settings.auth_key:  # type: ignore # noqa: F821
        raise HTTPException(status_code=401, detail="Unauthorized")
    return credentials.credentials


def get_settings() -> Settings:
    """
    Dependency to get settings.
    """
    return Settings()


def create_error_response(status_code: int, error: str, message: str, details: str):
    """
    Create a detailed error response.
    """
    response_model = DetailedErrorResponseModel(
        error=error, message=message, code=status_code, details=details
    )
    return JSONResponse(
        status_code=status_code, content=jsonable_encoder(response_model)
    )


@router.post(
    "/create",
    responses={
        201: {
            "model": PostFileResponseModel,
            "description": "File successfully created",
        },
        400: {
            "model": DetailedErrorResponseModel,
            "description": "Invalid file path or type",
        },
        409: {
            "model": DetailedErrorResponseModel,
            "description": "File already exists. Use overwrite flag to replace it.",
        },
        500: {
            "model": DetailedErrorResponseModel,
            "description": "Internal server error",
        },
    },
)
async def create_lua_file(
    request: Annotated[
        PostFileRequestModel,
        Body(
            ...,
            example={
                "content": "Menu = {}\nMenu.__index = Menu\n\n-- Constructor\nfunction Menu:new()\n    local self = setmetatable({}, Menu)\n    self.items = {}\n    self.selectedItems = {}\n    self.currItem = 1\n    return self\nend\n\nfunction Menu:down()\n    self.currItem = self.currItem + 1\n    if self.currItem > #self.items then\n        self.currItem = 1\n    end\nend\n\nfunction Menu:up()\n    self.currItem = self.currItem - 1\n    if self.currItem < 1 then\n        self.currItem = #self.items\n    end\nend\n\nreturn Menu",
                "path": "subdir/example.lua",
                "overwrite": False,
            },
        ),
    ],
    auth_key: str = Depends(get_auth_key),
    settings: Settings = Depends(get_settings),
):
    """
    Endpoint to create a new Lua file in the specified directory.
    """
    try:
        path = validate_path(request.path)
        content = validate_content(request.content)

        # Automatically add .lua extension if not present
        if not path.endswith(".lua"):
            path += ".lua"

        base_directory = os.path.realpath(settings.path_to_lua_files)
        file_path = os.path.realpath(os.path.join(base_directory, path))

        # Ensure the file path is within the base directory
        if not file_path.startswith(base_directory):
            logger.warning(f"Invalid file path access attempt: {file_path}")
            raise HTTPException(status_code=400, detail="Invalid file path")

        # Ensure the directory exists
        ensure_directory_exists(file_path)

        # Check if the file already exists
        if os.path.exists(file_path) and not request.overwrite:
            logger.warning(
                f"File already exists and overwrite not allowed: {file_path}"
            )
            raise HTTPException(
                status_code=409,
                detail="File already exists. Use overwrite flag to replace it.",
            )

        # Save the file content
        save_file_content(content, file_path)

        logger.info(f"File successfully created or overwritten: {file_path}")
        response_model = PostFileResponseModel(
            message="File successfully created or overwritten", file_path=file_path
        )
        return JSONResponse(status_code=201, content=jsonable_encoder(response_model))

    except ValueError as ve:
        logger.warning(f"Validation error: {str(ve)}")
        return create_error_response(400, "Validation Error", str(ve), str(ve))
    except HTTPException as http_exc:
        # Re-raise HTTP exceptions directly
        raise http_exc
    except OSError as e:
        logger.error(f"OS error occurred: {str(e)} while creating file: {path}")
        return create_error_response(
            500,
            "Internal Server Error",
            "An OS error occurred while creating the file.",
            str(e),
        )
    except Exception as e:
        logger.error(f"Unexpected error occurred: {str(e)} while creating file: {path}")
        return create_error_response(
            500,
            "Internal Server Error",
            "An unexpected error occurred while creating the file.",
            str(e),
        )
