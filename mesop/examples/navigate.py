import mesop as me


def navigate(event: me.ClickEvent):
  me.navigate("/about")


@me.page(path="/")
def home():
  me.text("This is the home page")
  me.button("navigate to about page", on_click=navigate)


@me.page(path="/about")
def about():
  me.text("This is the about page")
