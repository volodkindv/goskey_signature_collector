from pydantic import BaseModel


class UserContext(BaseModel):
    pass


class Appeal(BaseModel):
    id: int
    name: str
