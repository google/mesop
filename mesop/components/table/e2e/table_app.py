from datetime import datetime

import numpy as np
import pandas as pd

import mesop as me


@me.stateclass
class State:
  selected_cell: str = "No cell selected."


df = pd.DataFrame(
  data={
    "NA": [pd.NA, pd.NA, pd.NA],
    "Index": [3, 2, 1],
    "Bools": [True, False, np.bool_(True)],
    "Ints": [101, 90, np.int64(-55)],
    "Floats": [2.3, 4.5, np.float64(-3.000000003)],
    "Strings": ["Hello", "World", "!"],
    "Date Times": [
      pd.Timestamp("20180310"),
      pd.Timestamp("20230310"),
      datetime(2023, 1, 1, 12, 12, 1),
    ],
  }
)


@me.page(path="/components/table/e2e/table_app")
def app():
  state = me.state(State)

  with me.box(style=me.Style(padding=me.Padding.all(10), width=500)):
    me.table(
      df,
      on_click=on_click,
      header=me.TableHeader(sticky=True),
      columns={
        "NA": me.TableColumn(sticky=True),
        "Index": me.TableColumn(sticky=True),
      },
    )

  with me.box(
    style=me.Style(
      background="#ececec",
      margin=me.Margin.all(10),
      padding=me.Padding.all(10),
    )
  ):
    me.text(state.selected_cell)


def on_click(e: me.TableClickEvent):
  state = me.state(State)
  state.selected_cell = (
    f"Selected cell at col {e.col_index} and row {e.row_index} "
    f"with value {df.iat[e.row_index, e.col_index]!s}"
  )
