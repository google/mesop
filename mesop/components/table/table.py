from typing import Any

import mesop.components.table.table_pb2 as table_pb
from mesop.component_helpers import insert_component, register_native_component


# Don't include type hint since Pydantic can't properly type check the Pandas data
# frame. In addition, we don't want to include Pandas as a dependency into Mesop.
@register_native_component
def table(data_frame: Any):
  """
  This function creates a table from Pandas data frame

  Args:
      data_frame: Pandas data frame.
  """
  insert_component(
    type_name="table",
    proto=table_pb.TableType(
      displayed_columns=list(data_frame.columns),
      data_source=_to_data_source(data_frame),
    ),
  )


def _to_data_source(data_frame) -> list[table_pb.TableRow]:
  """Convert Pandas data frame for display as a table.

  All values will be converted to strings for display purposes on the frontend.
  """
  columns = list(data_frame.columns)
  data = []
  for df_row in data_frame.itertuples():
    data.append(
      table_pb.TableRow(
        row={col_name: str(getattr(df_row, col_name)) for col_name in columns}
      )
    )
  return data
