# app/api/models/detailed_error_response.py

from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime


class DetailedErrorResponseModel(BaseModel):
    error: str
    message: str
    code: Optional[int] = None
    details: Optional[Any] = None
    timestamp: datetime = datetime.now()
