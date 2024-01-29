from pydantic import BaseModel


class Appeal(BaseModel):
    id: int
    name: str
