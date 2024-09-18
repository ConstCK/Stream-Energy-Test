from pydantic import BaseModel, ConfigDict


# базовая схема для тега
class BaseTag(BaseModel):
    name: str


# Схема для получения тега
class Tag(BaseTag):
    id: int

    model_config = ConfigDict(from_attributes=True)


# Схема для создания тега
class TagCreation(BaseTag):
    notes: list[str] | None = None
