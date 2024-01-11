import mesop as me
import mesop.labs as mel


@me.page(path="/columns")
def main():
  with mel.columns():
    me.text("first_column")
    me.text("second_column")
