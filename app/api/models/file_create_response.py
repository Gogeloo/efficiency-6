from pydantic import BaseModel, Field

class PostFileResponseModel(BaseModel):
    content: str = Field(..., description="The content of the Lua file", example="We are the champions, my friends")
    path: str = Field(..., description="The path where the Lua file will be saved", example="test.lua")
    overwrite: bool = Field(False, description="Flag to indicate if existing files should be overwritten", example=False)
