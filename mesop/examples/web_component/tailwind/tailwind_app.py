import mesop as me
import mesop.labs as mel


@mel.web_component(path="./tailwind.js")
def tailwind():
  pass


@me.page(
  path="/web_component/tailwind/tailwind_app",
)
def page():
  me.text("Loaded")
  tailwind()
  with me.box(style=me.Style(classes=["text-lg", "font-medium"])):
    me.text("hi")
