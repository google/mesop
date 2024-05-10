import mesop as me
import mesop.labs as mel


@me.page(path="/text_to_image", title="Text to Image Example")
def app():
  mel.text_to_image(
    generate_image,
    title="Text to Image Example",
  )


def generate_image(prompt: str):
  return "https://www.google.com/logos/doodles/2024/earth-day-2024-6753651837110453-2xa.gif"
