"""
An example is a single input/output pair.
    - Examples are used for fine-tuning a model (i.e. golden example) or running an eval (i.e. expected example).
    - There are two types of examples:
        - **Golden Example**: A golden example is an example that is used to create a golden dataset.
        - **Expected Example**: An expected example is an example that is used to evaluate a producer.
        Internally, once an expected example has been run through an eval, we create an **evaluated example**, but you don't need to create this manually in the UI.
"""

import os
import shutil
from datetime import datetime
from typing import Generic, Literal, TypeVar

from pydantic import BaseModel, field_validator, model_validator

from ai.common.model_validators import (
  convert_empty_string_to_none,
  is_required_str,
)
from ai.common.output_format import OutputFormat


class ExampleInput(BaseModel):
  prompt: str
  input_code: str | None = None
  line_number_target: int | None = None

  @field_validator("prompt", mode="after")
  @classmethod
  def is_required(cls, v):
    return is_required_str(v)

  @field_validator("line_number_target", mode="before")
  @classmethod
  # Intentionally leave out annotations since the input value may be ambiguous.
  def empty_string_to_none(cls, v):
    return convert_empty_string_to_none(v)

  @model_validator(mode="after")
  def is_valid_line_number(self):
    if isinstance(self.line_number_target, int):
      if self.line_number_target < 1:
        raise ValueError("Line number must be greater than 0.")
      # There are times when the input_code is None because it has not been loaded from
      # file yet. So we only validate if the line number exceeds its target if the
      # input_code is populated.
      if self.input_code and self.line_number_target > len(
        self.input_code.split("\n")
      ):
        raise ValueError("Line number exceeds lines in input code.")

    return self


class BaseExample(BaseModel):
  id: str
  input: ExampleInput
  created_at: datetime = None
  updated_at: datetime = None

  @field_validator("id", mode="after")
  @classmethod
  def is_required(cls, v):
    return is_required_str(v)


class ExampleOutput(BaseModel):
  output_code: str | None = None
  raw_output: str | None = None
  output_type: OutputFormat = "diff"
  udiff_output: str | None = None

  @field_validator("output_code", "raw_output", "udiff_output", mode="before")
  @classmethod
  # Intentionally leave out annotations since the input value may be ambiguous.
  def empty_string_to_none(cls, v):
    return convert_empty_string_to_none(v)


class ExpectedExample(BaseExample):
  expect_executable: bool = True
  expect_type_checkable: bool = True


class ExpectResult(BaseModel):
  name: Literal["executable", "type_checkable", "patchable"]
  score: int  # 0 or 1
  message: str | None = None

  @field_validator("score", mode="after")
  @classmethod
  # Intentionally leave out annotations since the input value may be ambiguous.
  def is_valid_score(cls, v: int) -> int:
    if v not in {0, 1}:
      raise ValueError("Score must be 0 or 1.")
    return v

  @field_validator("message", mode="before")
  @classmethod
  # Intentionally leave out annotations since the input value may be ambiguous.
  def empty_string_to_none(cls, v):
    return convert_empty_string_to_none(v)


class EvaluatedExampleOutput(BaseModel):
  time_spent_secs: float
  tokens: int
  output: ExampleOutput
  expect_results: list[ExpectResult]


class EvaluatedExample(BaseModel):
  expected: ExpectedExample
  outputs: list[EvaluatedExampleOutput]


class GoldenExample(BaseExample):
  output: ExampleOutput


T = TypeVar("T", bound=BaseExample)


class ExampleStore(Generic[T]):
  def __init__(self, entity_type: type[T], *, dirname: str):
    self.entity_type = entity_type
    self.directory_path = os.path.join(
      os.path.dirname(__file__), "..", "..", "..", "data", dirname
    )

  def get(self, id: str) -> T:
    dir_path = os.path.join(self.directory_path, id)
    json_path = os.path.join(dir_path, "example_input.json")
    with open(json_path) as f:
      entity_json = f.read()
    entity = self.entity_type.model_validate_json(entity_json)
    input = entity.input
    input_py_path = os.path.join(dir_path, "input.py")
    if os.path.exists(input_py_path):
      with open(input_py_path) as f:
        input.input_code = f.read()
    if isinstance(entity, GoldenExample):
      output_py_path = os.path.join(dir_path, "output.py")
      if os.path.exists(output_py_path):
        with open(output_py_path) as f:
          entity.output.output_code = f.read()
      raw_output_path = os.path.join(dir_path, "raw_output.txt")
      if os.path.exists(raw_output_path):
        with open(raw_output_path) as f:
          entity.output.raw_output = f.read()
      udiff_output_path = os.path.join(dir_path, "udiff.txt")
      if os.path.exists(udiff_output_path):
        with open(udiff_output_path) as f:
          entity.output.udiff_output = f.read()
    return entity

  def get_all(self) -> list[T]:
    entities: list[T] = []
    for filename in os.listdir(self.directory_path):
      entities.append(self.get(filename))
    return entities

  def save(self, entity: T, overwrite: bool = False):
    id = entity.id
    dir_path = os.path.join(self.directory_path, id)

    # Update timestamps
    current_time = datetime.utcnow()
    if entity.created_at is None:
      entity.created_at = current_time
    entity.updated_at = current_time

    if not overwrite:
      if os.path.exists(dir_path):
        raise ValueError(
          f"{self.entity_type.__name__} with id {id} already exists"
        )
      else:
        os.mkdir(dir_path)
    json_path = os.path.join(dir_path, "example_input.json")
    input_code = entity.input.input_code
    if input_code:
      input_py_path = os.path.join(dir_path, "input.py")
      with open(input_py_path, "w") as f:
        f.write(input_code)
    entity.input.input_code = None

    if isinstance(entity, GoldenExample):
      output_py_path = os.path.join(dir_path, "output.py")
      with open(output_py_path, "w") as f:
        f.write(entity.output.output_code)
      raw_output_path = os.path.join(dir_path, "raw_output.txt")
      with open(raw_output_path, "w") as f:
        f.write(entity.output.raw_output)
      entity.output.output_code = None
      entity.output.raw_output = None
    with open(json_path, "w") as f:
      f.write(entity.model_dump_json(indent=4))

  def delete(self, entity_id: str):
    shutil.rmtree(os.path.join(self.directory_path, entity_id))


expected_example_store = ExampleStore(
  ExpectedExample, dirname="expected_examples"
)
golden_example_store = ExampleStore(GoldenExample, dirname="golden_examples")
