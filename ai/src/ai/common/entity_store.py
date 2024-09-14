import os
from typing import Generic, TypeVar

from pydantic import BaseModel, field_validator

from ai.common.model_validators import is_required_str

T = TypeVar("T", bound=BaseModel)


def get_data_path(dirname: str) -> str:
  return os.path.join(
    os.path.dirname(__file__), "..", "..", "..", "data", dirname
  )


class BaseEntity(BaseModel):
  id: str

  @field_validator("id", mode="after")
  @classmethod
  def id_required(cls, v):
    return is_required_str(v)


class EntityStore(Generic[T]):
  def __init__(self, entity_type: type[T], *, dirname: str):
    self.entity_type = entity_type
    self.directory_path = get_data_path(dirname)

  def get(self, id: str) -> T:
    file_path = os.path.join(self.directory_path, f"{id}.json")
    with open(file_path) as f:
      entity_json = f.read()
    entity = self.entity_type.model_validate_json(entity_json)
    return entity

  def get_all(self) -> list[T]:
    entities: list[T] = []
    for filename in os.listdir(self.directory_path):
      if filename.endswith(".json"):
        file_path = os.path.join(self.directory_path, filename)
        with open(file_path) as f:
          entity_json = f.read()
        entities.append(self.entity_type.model_validate_json(entity_json))
    entities.sort(key=lambda x: x.id, reverse=True)
    return entities

  def save(self, entity: T, overwrite: bool = False):
    id = entity.id  # type: ignore
    entity_path = os.path.join(self.directory_path, f"{id}.json")
    if not overwrite and os.path.exists(entity_path):
      raise ValueError(
        f"{self.entity_type.__name__} with id {id} already exists"
      )
    with open(entity_path, "w") as f:
      f.write(entity.model_dump_json(indent=4))

  def delete(self, entity_id: str):
    os.remove(os.path.join(self.directory_path, f"{entity_id}.json"))
