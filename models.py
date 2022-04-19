from enum import Enum
from typing import List, Optional
from uuid import UUID, uuid4
from datetime import date

from pydantic import BaseModel, validator, Field


class Genre(BaseModel):
    name: str


class Author(BaseModel):
    first_name: str
    last_name: str
    age: int = Field(..., gt=15, lt=90)

    # or like this
    # @validator('age')
    # def validate_age(cls, v):
    #     if v < 0:
    #         raise ValueError('Age must be positive')
    #     return v


class Book(BaseModel):
    title: str
    writer: str
    duration: str
    date: date
    summary: str
    genres: List[Genre]
    pages: int


class Gender(str, Enum):
    male = "male"
    female = "female"


class Role(str, Enum):
    admin = "admin"
    user = "user"
    student = "student"


class User(BaseModel):
    id: Optional[UUID] = uuid4()
    first_name: str
    last_name: str
    middle_name: Optional[str]
    gender: Gender
    roles: List[Role]


class UserUpdateRequest(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    middle_name: Optional[str]
    roles: Optional[List[Role]]
