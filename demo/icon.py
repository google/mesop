import mesop as me


@me.page(path="/icon")
def app():
  me.text("home icon")
  me.icon(icon="home")
