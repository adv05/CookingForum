from typing import Optional
from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPL(BaseModel):
    sub: Optional[int] = None
