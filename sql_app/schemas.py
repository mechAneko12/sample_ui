from typing import Optional, List
import datetime

from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    timestamp: datetime.datetime
    description: List[List[float]]


class ItemCreate(ItemBase):
    pass

class ItemById(BaseModel):
    id: int

class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True
