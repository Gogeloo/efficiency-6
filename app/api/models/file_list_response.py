from pydantic import BaseModel
from typing import List


class FileListResponseModel(BaseModel):
    files: List[str]
