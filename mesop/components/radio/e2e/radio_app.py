import mesop as me


@me.stateclass
class State:
  radio_value: str = "2"


def on_change(event: me.RadioChangeEvent):
  s = me.state(State)
  s.radio_value = event.value


@me.page(path="/components/radio/e2e/radio_app")
def app():
  s = me.state(State)
  me.radio(
    on_change=on_change,
    options=[
      me.RadioOption(label="Option 1", value="1"),
      me.RadioOption(label="Option 2", value="2"),
    ],
    value=s.radio_value,
    style=me.Style(
      border=me.Border.all(
        me.BorderSide(
          width=1,
          color="green",
          style="solid",
        )
      )
    ),
  )
  me.text(text="Selected radio value: " + s.radio_value)
