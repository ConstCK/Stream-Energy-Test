from pydantic import BaseModel, ConfigDict


class BaseTag(BaseModel):
    name: str



class Tag(BaseTag):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TagCreation(BaseTag):
    notes: list[str] | None = None
