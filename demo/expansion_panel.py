from dataclasses import field

import mesop as me


@me.stateclass
class State:
  normal_accordion: dict[str, bool] = field(
    default_factory=lambda: {"pie": True, "donut": False, "icecream": False}
  )
  multi_accordion: dict[str, bool] = field(
    default_factory=lambda: {"pie": False, "donut": False, "icecream": False}
  )


def load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(
  on_load=load,
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/expansion_panel",
)
def app():
  state = me.state(State)
  with me.box(
    style=me.Style(
      display="flex",
      flex_direction="column",
      gap=15,
      margin=me.Margin.all(15),
      max_width=500,
    )
  ):
    me.text("Normal Accordion", type="headline-5")
    with me.accordion():
      with me.expansion_panel(
        key="pie",
        title="Pie",
        description="Type of snack",
        icon="pie_chart",
        disabled=False,
        expanded=state.normal_accordion["pie"],
        hide_toggle=False,
        on_toggle=on_accordion_toggle,
      ):
        me.text(
          "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla sed augue ultricies, laoreet nunc eget, ultricies augue. In ornare bibendum mauris vel sodales. Donec ut interdum felis. Nulla facilisi. Morbi a laoreet turpis, sed posuere arcu. Nam nisi neque, molestie vitae euismod eu, sollicitudin eu lectus. Pellentesque orci metus, finibus id faucibus et, ultrices quis dui. Duis in augue ac metus tristique lacinia."
        )

      with me.expansion_panel(
        key="donut",
        title="Donut",
        description="Type of breakfast",
        icon="donut_large",
        disabled=False,
        expanded=state.normal_accordion["donut"],
        hide_toggle=False,
        on_toggle=on_accordion_toggle,
      ):
        me.text(
          "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla sed augue ultricies, laoreet nunc eget, ultricies augue. In ornare bibendum mauris vel sodales. Donec ut interdum felis. Nulla facilisi. Morbi a laoreet turpis, sed posuere arcu. Nam nisi neque, molestie vitae euismod eu, sollicitudin eu lectus. Pellentesque orci metus, finibus id faucibus et, ultrices quis dui. Duis in augue ac metus tristique lacinia."
        )

      with me.expansion_panel(
        key="icecream",
        title="Ice cream",
        description="Type of dessert",
        icon="icecream",
        disabled=False,
        expanded=state.normal_accordion["icecream"],
        hide_toggle=False,
        on_toggle=on_accordion_toggle,
      ):
        me.text(
          "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla sed augue ultricies, laoreet nunc eget, ultricies augue. In ornare bibendum mauris vel sodales. Donec ut interdum felis. Nulla facilisi. Morbi a laoreet turpis, sed posuere arcu. Nam nisi neque, molestie vitae euismod eu, sollicitudin eu lectus. Pellentesque orci metus, finibus id faucibus et, ultrices quis dui. Duis in augue ac metus tristique lacinia."
        )

    me.text("Multi Accordion", type="headline-5")
    with me.box(
      style=me.Style(display="flex", gap=20, margin=me.Margin(bottom=15)),
    ):
      me.button(
        label="Open All", type="flat", on_click=on_multi_accordion_open_all
      )
      me.button(
        label="Close All", type="flat", on_click=on_multi_accordion_close_all
      )

    with me.accordion():
      with me.expansion_panel(
        key="pie",
        title="Pie",
        description="Type of snack",
        icon="pie_chart",
        expanded=state.multi_accordion["pie"],
        on_toggle=on_multi_accordion_toggle,
      ):
        me.text(
          "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla sed augue ultricies, laoreet nunc eget, ultricies augue. In ornare bibendum mauris vel sodales. Donec ut interdum felis. Nulla facilisi. Morbi a laoreet turpis, sed posuere arcu. Nam nisi neque, molestie vitae euismod eu, sollicitudin eu lectus. Pellentesque orci metus, finibus id faucibus et, ultrices quis dui. Duis in augue ac metus tristique lacinia."
        )

      with me.expansion_panel(
        key="donut",
        title="Donut",
        description="Type of breakfast",
        icon="donut_large",
        expanded=state.multi_accordion["donut"],
        on_toggle=on_multi_accordion_toggle,
      ):
        me.text(
          "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla sed augue ultricies, laoreet nunc eget, ultricies augue. In ornare bibendum mauris vel sodales. Donec ut interdum felis. Nulla facilisi. Morbi a laoreet turpis, sed posuere arcu. Nam nisi neque, molestie vitae euismod eu, sollicitudin eu lectus. Pellentesque orci metus, finibus id faucibus et, ultrices quis dui. Duis in augue ac metus tristique lacinia."
        )

      with me.expansion_panel(
        key="icecream",
        title="Ice cream",
        description="Type of dessert",
        icon="icecream",
        expanded=state.multi_accordion["icecream"],
        on_toggle=on_multi_accordion_toggle,
      ):
        me.text(
          "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla sed augue ultricies, laoreet nunc eget, ultricies augue. In ornare bibendum mauris vel sodales. Donec ut interdum felis. Nulla facilisi. Morbi a laoreet turpis, sed posuere arcu. Nam nisi neque, molestie vitae euismod eu, sollicitudin eu lectus. Pellentesque orci metus, finibus id faucibus et, ultrices quis dui. Duis in augue ac metus tristique lacinia."
        )

    me.text("Expansion Panel", type="headline-5")

    with me.expansion_panel(
      key="pie",
      title="Pie",
      description="Type of snack",
      icon="pie_chart",
    ):
      me.text(
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nulla sed augue ultricies, laoreet nunc eget, ultricies augue. In ornare bibendum mauris vel sodales. Donec ut interdum felis. Nulla facilisi. Morbi a laoreet turpis, sed posuere arcu. Nam nisi neque, molestie vitae euismod eu, sollicitudin eu lectus. Pellentesque orci metus, finibus id faucibus et, ultrices quis dui. Duis in augue ac metus tristique lacinia."
      )


def on_accordion_toggle(e: me.ExpansionPanelToggleEvent):
  """Implements accordion behavior where only one panel can be open at a time"""
  state = me.state(State)
  state.normal_accordion = {"pie": False, "donut": False, "icecream": False}
  state.normal_accordion[e.key] = e.opened


def on_multi_accordion_toggle(e: me.ExpansionPanelToggleEvent):
  """Implements accordion behavior where only multiple panels can be open at a time"""
  state = me.state(State)
  state.multi_accordion[e.key] = e.opened


def on_multi_accordion_open_all(e: me.ClickEvent):
  state = me.state(State)
  for key in state.multi_accordion:
    state.multi_accordion[key] = True


def on_multi_accordion_close_all(e: me.ClickEvent):
  state = me.state(State)
  for key in state.multi_accordion:
    state.multi_accordion[key] = False
