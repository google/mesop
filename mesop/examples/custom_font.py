import mesop as me


@me.page(
  path="/custom_font",
  stylesheets=["https://fonts.googleapis.com/css2?family=Tiny5&display=swap"],
)
def app():
  me.text("custom font", style=me.Style(font_family="Tiny5"))
