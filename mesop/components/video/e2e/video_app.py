import mesop as me


@me.page(path="/components/video/e2e/video_app")
def app():
  me.video(
    src="https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.webm",
    style=me.Style(height=300, width=300),
  )
