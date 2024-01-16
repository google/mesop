import mesop as me
from mesop.labs.layout import columns


@me.page(path="/columns")
def main():
  with columns(columns=2):
    me.text("first_column")
    me.text("second_column")
