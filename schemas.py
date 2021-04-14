from pydantic import BaseModel
from typing import Optional

class UserRequestModel(BaseModel):
    age: int
    class_of_worker: str
    industry_code: int
    occupation_code: int
    marital_status: Optional[str] = None
    major_industry_code: Optional[str] = None
    major_occupation_code: Optional[str] = None
    hispanic_origin: Optional[str] = None
    sex: Optional[str] = None
