from functools import partial
from typing import Any, Callable, Type, TypeVar

from pydantic import BaseModel

import mesop as me
from ai.common.entity_store import EntityStore
from ai.common.example import BaseExample, ExampleStore
from ai.console.scaffold import page_scaffold


@me.stateclass
class State:
  entity: dict[str, Any]


def form_field(field: str, description: str, type: str | None = None):
  disabled = "id" in me.query_params and field == "id"
  me.input(
    disabled=disabled,
    value=str(get_field_value(field)),
    appearance="outline",
    type=type,  # type: ignore
    label=field,
    on_blur=lambda e: update_state(e.key, e.value),
    key=field,
    hint_label=description,
    style=me.Style(width="min(100%, 360px)"),
  )


def update_state(key: str, value: Any):
  state = me.state(State)
  state.entity[key] = value


def get_field_value(field_name: str):
  state = me.state(State)
  # We do some hacky-ish logic to support both dot notation and nested dicts.

  # When the field is set in the current page, we set it with dot notation.
  if field_name in state.entity:
    return state.entity[field_name] or ""

  # Otherwise, if we loaded the entity from the store (i.e. filesystem),
  # we access it as a nested dict.
  keys = field_name.split(".")
  value = state.entity
  for key in keys:
    if isinstance(value, dict):
      value = value.get(key, "")
    else:
      return ""
  return value or ""


T = TypeVar("T", bound=BaseModel)
E = TypeVar("E", bound=BaseExample)


def create_add_edit_page(
  *,
  store: EntityStore[T] | ExampleStore[E],
  entity_type: Type[T] | Type[E],
  entity_name: str,
  root_path: str,
  form: Callable[[], None],
  create_default_entity: Callable[[], dict[str, Any]] | None = None,
  disable_edit: bool = False,
):
  def on_load_edit_page(e: me.LoadEvent):
    me.set_theme_mode("system")
    id = me.query_params.get("id")
    assert id is not None
    entity = store.get(id)
    state = me.state(State)
    state.entity = entity.model_dump()

  def delete(e: me.ClickEvent):
    store.delete(me.state(State).entity["id"])
    reset_and_navigate()

  if not disable_edit:

    @me.page(path=root_path + "/edit", on_load=on_load_edit_page)
    def edit_page():  # type: ignore
      with page_scaffold(title=f"Edit {entity_name}"):
        with me.box(
          style=me.Style(
            display="flex", flex_direction="column", gap=24, max_width=640
          )
        ):
          form()
          with me.box(
            style=me.Style(
              display="flex",
              flex_direction="row",
              justify_content="space-between",
              gap=16,
            )
          ):
            me.button(
              "Back",
              type="stroked",
              on_click=lambda e: reset_and_navigate(),
            )
            me.button("Delete", type="flat", color="warn", on_click=delete)
            me.button(
              "Save", type="flat", on_click=partial(update, overwrite=True)
            )

  def on_load_add_page(e: me.LoadEvent):
    me.set_theme_mode("system")
    state = me.state(State)
    if create_default_entity is not None:
      state.entity = create_default_entity()
    else:
      state.entity = {}

  @me.page(path=root_path + "/add", on_load=on_load_add_page)
  def add_page():  # type: ignore
    with page_scaffold(
      title=f"Add {entity_name}",
    ):
      with me.box(
        style=me.Style(
          display="flex", flex_direction="column", gap=24, max_width=640
        )
      ):
        form()
        with me.box(
          style=me.Style(
            display="flex",
            flex_direction="row",
            justify_content="space-between",
            gap=16,
          )
        ):
          me.button(
            "Back",
            type="stroked",
            on_click=lambda e: reset_and_navigate(),
          )
          me.button("Add", type="flat", on_click=update)

  def update(e: me.ClickEvent, *, overwrite: bool = False):
    state = me.state(State)
    # convert dot notation to nested dicts
    converted: dict[str, Any] = {}
    for key in state.entity:
      keys = key.split(".")
      current = converted
      for k in keys[:-1]:
        if k not in current:
          current[k] = {}
        current = current[k]
      current[keys[-1]] = state.entity[key]

    store.save(entity_type(**converted), overwrite=overwrite)  # type: ignore
    reset_and_navigate()

  def reset_and_navigate():
    state = me.state(State)
    state.entity = {}
    me.navigate(root_path or "/")
