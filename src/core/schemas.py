from pydantic import BaseModel


class UniversalModelSchema(BaseModel):
    id: int
    name: str


class UniversalNameSchema(BaseModel):
    name: str
