from pydantic import BaseModel


class User(BaseModel):
    id: int | None = (None,)
    email: str = None


class UserIn(User):
    password: str
