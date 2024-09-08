import mesop as me

def icon_button_click(e: me.ClickEvent):
    # Add functionality for the icon button click event
    pass

@me.page()
def page():
    with me.box(style=me.Style(padding=me.Padding.all(16), display="flex", flex_direction="column", align_items="flex-start")):
        with me.content_button(type="icon", on_click=icon_button_click, style=me.Style(margin=me.Margin(bottom=16), border_radius=8)):
            me.icon("add")
        content()

def content():
    me.text("Hello, world!")
    me.text("Hello, world!")
    me.text("Hello, world!")