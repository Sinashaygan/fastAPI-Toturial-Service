from pydantic import BaseModel


class PersonCreateSchema(BaseModel):
    name: str


class PersonResponseSchema(BaseModel):
    id: int
    name: str
