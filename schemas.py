from pydantic import BaseModel
from typing import List, Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None

class UserBase(BaseModel):
    username: str
    role: str

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    class Config:
        from_attributes = True

class StudentBase(BaseModel):
    roll_number: str
    name: str
    email: str
    course: str

class StudentCreate(StudentBase):
    pass

class StudentResponse(StudentBase):
    id: int
    class Config:
        from_attributes = True

class SubjectBase(BaseModel):
    code: str
    name: str

class SubjectCreate(SubjectBase):
    max_internal: float = 30.0
    max_external: float = 70.0

class SubjectResponse(SubjectBase):
    id: int
    max_internal: float
    max_external: float
    class Config:
        from_attributes = True

class MarkBase(BaseModel):
    internal_marks: float
    external_marks: float

class MarkCreate(MarkBase):
    student_id: int
    subject_id: int

class MarkResponse(MarkBase):
    id: int
    student_id: int
    subject_id: int
    class Config:
        from_attributes = True

class StudentDetailedResponse(StudentResponse):
    marks: List[MarkResponse] = []
