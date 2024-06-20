from pydantic import BaseModel


class FileResponseModel(BaseModel):
    detail: str
