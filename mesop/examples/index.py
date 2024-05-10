import mesop as me
from mesop.examples.shared.navmenu import scaffold


@me.page(path="/index")
def index():
  with scaffold(url="/"):
    body()


def body():
  with me.box(
    style=me.Style(
      font_family="Google Sans Text",
      background="white",
      padding=me.Padding.all(16),
    )
  ):
    me.markdown(
      """
# Welcome

## Components

- [buttons](/buttons)
- [badge](/components/badge/e2e/badge_app)
- [box](/components/box/e2e/box_app)
- [checkbox](/components/checkbox/e2e/checkbox_app)
- [divider](/components/divider/e2e/divider_app)
- [icon](/components/icon/e2e/icon_app)
- [input](/components/input/e2e/input_app)
- [markdown](/components/markdown/e2e/markdown_app)
- [progress bar](/components/progress_bar/e2e/progress_bar_app)
- [progress spinner](/components/progress_spinner/e2e/progress_spinner_app)
- [radio](/components/radio/e2e/radio_app)
- [select](/components/select/e2e/select_app)
- [select toggle](/components/slide_toggle/e2e/slide_toggle_app)
- [slider](/components/slider/e2e/slider_app)
- [text](/components/text/e2e/text_app)
- [tooltip](/components/tooltip/e2e/tooltip_app)

"""
    )
