import mesop as me


def load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(
  on_load=load,
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/audio",
)
def app():
  """
  In order to autoplay audio, set the `autoplay` attribute to `True`,
  Note that there are autoplay restrictions in modern browsers, including Chrome,
  are designed to prevent audio or video from playing automatically without user interaction.
  This is intended to improve user experience and reduce unwanted interruptions.
  You can check the [autoplay ability of your application](https://developer.mozilla.org/en-US/docs/Web/Media/Autoplay_guide#autoplay_availability)
  """
  with me.box(style=me.Style(margin=me.Margin.all(15))):
    me.audio(
      src="https://interactive-examples.mdn.mozilla.net/media/cc0-audio/t-rex-roar.mp3",
      # autoplay=True
    )
