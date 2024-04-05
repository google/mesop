from datetime import datetime

import numpy as np
import pandas as pd

import mesop as me


@me.page(path="/components/table/e2e/table_app")
def app():
  with me.box(
    style=me.Style(
      padding=me.Padding(top=10, right=10, left=10, bottom=10), width=500
    )
  ):
    df = pd.DataFrame(
      data={
        "NA": [pd.NA, pd.NA, pd.NA],
        "Bools": [True, False, np.bool_(True)],
        "Ints": [101, 90, np.int64(-55)],
        "Floats": [2.3, 4.5, np.float64(-3.000000003)],
        "Strings": ["Hello", "World", "!"],
        "DateTimes": [
          pd.Timestamp("20180310"),
          pd.Timestamp("20230310"),
          datetime(2023, 1, 1, 12, 12, 1),
        ],
      }
    )
    me.table(df)
