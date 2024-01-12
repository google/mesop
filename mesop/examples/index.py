import mesop as me
from mesop.examples.shared.navmenu import scaffold


@me.page(path="/")
def index():
  with scaffold(url="/"):
    body()


def body():
  with me.box(
    style=me.Style(
      background="white",
      padding=me.Padding(top=16, bottom=16, left=16, right=16),
    )
  ):
    me.markdown(
      """
# Welcome

## Components

- [buttons](/buttons)

/columns
/components/badge/e2e/badge_app
/components/box/e2e/box_app
/components/checkbox/e2e/checkbox_app
/components/divider/e2e/divider_app
/components/icon/e2e/icon_app
/components/input/e2e/input_app
/components/markdown/e2e/markdown_app
/components/progress_bar/e2e/progress_bar_app
/components/progress_spinner/e2e/progress_spinner_app
/components/radio/e2e/radio_app
/components/select/e2e/select_app
/components/slide_toggle/e2e/slide_toggle_app
/components/slider/e2e/slider_app
/components/text/e2e/text_app
/components/tooltip/e2e/tooltip_app"""
    )
