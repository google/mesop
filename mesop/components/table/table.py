from dataclasses import dataclass
from typing import Any, Callable

import mesop.components.table.table_pb2 as table_pb
from mesop.component_helpers import (
  insert_component,
  register_event_handler,
  register_event_mapper,
  register_native_component,
)
from mesop.events import MesopEvent


@dataclass(kw_only=True)
class TableClickEvent(MesopEvent):
  """Event representing a click on the table component cell.

  Attributes:
      row_index: DataFrame row index of the clicked cell in the table.
      col_index: DataFrame col index of the clicked cell in the table.
      key (str): key of the component that emitted this event.
  """

  row_index: int
  col_index: int


def map_table_click_event(event, key):
  click_event = table_pb.TableClickEvent()
  click_event.ParseFromString(event.bytes_value)
  return TableClickEvent(
    key=key.key,
    row_index=click_event.row_index,
    col_index=click_event.col_index,
  )


register_event_mapper(TableClickEvent, map_table_click_event)


@dataclass(kw_only=True)
class TableHeader:
  sticky: bool = False


@dataclass(kw_only=True)
class TableColumn:
  sticky: bool = False


# Don't include type hint since Pydantic can't properly type check the Pandas data
# frame. In addition, we don't want to include Pandas as a dependency into Mesop.
@register_native_component
def table(
  data_frame: Any,
  *,
  on_click: Callable[[TableClickEvent], Any] | None = None,
  header: TableHeader | None = None,
  columns: dict[str, TableColumn] | None = None,
):
  """
  This function creates a table from Pandas data frame

  Args:
      data_frame: Pandas data frame.
      on_click: Triggered when a table cell is clicked. The [click event](https://developer.mozilla.org/en-US/docs/Web/API/HTMLElement/click_event) is a native browser event.
      header: Configures table header to be sticky or not.
      columns: Configures table columns to be sticky or not. The key is the name of the column.
  """
  if not columns:
    columns = {}
  if not header:
    header = TableHeader()
  insert_component(
    type_name="table",
    proto=table_pb.TableType(
      displayed_columns=list(data_frame.columns),
      data_source=_to_data_source(data_frame),
      on_table_click_event_handler_id=register_event_handler(
        on_click, event=TableClickEvent
      )
      if on_click
      else "",
      header=table_pb.TableHeader(sticky=header.sticky),
      columns={
        column_name: table_pb.TableColumn(sticky=column.sticky)
        for column_name, column in columns.items()
      },
    ),
  )


def _to_data_source(data_frame) -> list[table_pb.TableRow]:
  """Convert Pandas data frame for display as a table.

  All values will be converted to strings for display purposes on the frontend.

  The special Pandas `Index` column is included automatically, so we can refer back to
  same cell on the server to handle user events.
  """
  data = []
  for df_row in data_frame.itertuples(name=None):
    data.append(
      table_pb.TableRow(
        index=df_row[0],
        cell_values=[str(row) for row in df_row[1:]],
      )
    )
  return data
