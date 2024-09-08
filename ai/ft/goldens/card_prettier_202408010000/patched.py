import mesop as me

@me.page()
def card_page():
    with me.box(style=me.Style(
        width=320,
        background=me.theme_var("surface"),
        border_radius=12,
        padding=me.Padding.all(24),
        box_shadow="0 8px 16px rgba(0, 0, 0, 0.1)",
        display="flex",
        flex_direction="column",
        gap=20,
    )):
        with me.box(style=me.Style(display="flex", align_items="center", gap=12)):
            me.icon("card_membership", style=me.Style(color=me.theme_var("primary")))
            me.text("Elegant Card", style=me.Style(color=me.theme_var("on-surface")))

        me.divider()

        me.text("This beautifully designed card showcases a modern and sleek appearance. It combines subtle shadows, smooth transitions, and carefully chosen colors to create an appealing visual element.",
                type="body-1",
                style=me.Style(color=me.theme_var("on-surface-variant"), line_height="1.6"))

        with me.box(style=me.Style(display="flex", justify_content="end", margin=me.Margin(top=16))):
            me.button("Learn More", on_click=card_action, type="flat",
                      style=me.Style(padding=me.Padding.symmetric(horizontal=16, vertical=8),
                                     border_radius=20))

def card_action(e: me.ClickEvent):
    print("Card action clicked")