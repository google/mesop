import mesop as me
import mesop.labs as mel


@me.page(path="/text_to_image", title="Text to Image Example")
def app():
  mel.text_to_image(
    generate_image,
    title="Text to Image Example",
  )


def generate_image(prompt: str):
  return "https://google.github.io/mesop/assets/editor-v1.png"
