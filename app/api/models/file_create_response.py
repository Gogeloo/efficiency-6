from pydantic import BaseModel, Field
from datetime import datetime


class PostFileRequestModel(BaseModel):
    content: str = Field(
        ...,
        description="The content of the Lua file",
        example="Menu = {}\nMenu.__index = Menu\n\n-- Constructor\nfunction Menu:new()\n    local self = setmetatable({}, Menu)\n    self.items = {}\n    self.selectedItems = {}\n    self.currItem = 1\n    return self\nend\n\nfunction Menu:down()\n    self.currItem = self.currItem + 1\n    if self.currItem > #self.items then\n        self.currItem = 1\n    end\nend\n\nfunction Menu:up()\n    self.currItem = self.currItem - 1\n    if self.currItem < 1 then\n        self.currItem = #self.items\n    end\nend\n\nreturn Menu",
    )
    path: str = Field(
        ..., description="The path where the Lua file will be saved", example="test.lua"
    )
    overwrite: bool = Field(
        False,
        description="Flag to indicate if existing files should be overwritten",
        example=False,
    )


class PostFileResponseModel(BaseModel):
    message: str = Field(
        ...,
        description="Response message",
        example="File successfully created or overwritten",
    )
    file_path: str = Field(
        ...,
        description="The path where the file was saved",
        example="/path/to/lua/files/test.lua",
    )
    timestamp: datetime = Field(
        default_factory=datetime.now, description="Timestamp of the response"
    )
