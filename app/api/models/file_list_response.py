from pydantic import BaseModel, Field
from typing import List


class GetFileListResponseModel(BaseModel):
    files: List[str] = Field(
        description="List of Lua files available",
        example=["test.lua", "test_folder/test2.lua"]
    )
