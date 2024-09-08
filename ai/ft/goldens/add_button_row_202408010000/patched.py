import mesop as me


@me.stateclass
class State:
    pass


def button_click(e: me.ClickEvent):
    print(f"Button {e.key} clicked!")

@me.page()
def hello_world():
    me.text("Hello, World!", type="headline-1")

    with me.box(style=me.Style(display="flex", flex_direction="row", gap=16, margin=me.Margin.symmetric(vertical=24))):
        for i in range(1, 4):
            me.button(f"Button {i}", on_click=button_click, type="flat", key=f"btn_{i}",
                      style=me.Style(border_radius=8, padding=me.Padding.symmetric(horizontal=16, vertical=8)))
