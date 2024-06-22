from pydantic import BaseModel


class GetFileResponseModel(BaseModel):
    detail: str
