import mesop as me
import mesop.components.button.button_pb2 as button_pb


class Bar:
  val: str
  pass


class Foo:
  val: str


b = button_pb.ButtonType()
b.color = "abc"
print("~ b", b)
c = button_pb.ButtonType()
print("~ c", c)


@me.stateclass
class State:
  button: button_pb.ButtonType
  a: str
  b: Bar


s = State()
s.button.color = "foo"
print("s.button (1)", s.button)
s.b.val = "hi"
print(s)
print("---")
b = State()
print("b.button (2)", b.button)
print(b)


@me.page()
def page():
  me.text("mutable state")
