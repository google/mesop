import mesop as me


@me.page()
def main_page():
    with me.box(style=me.Style(
        padding=me.Padding.all(24),
        display="grid",
        grid_template_columns="repeat(3, 1fr)",
        gap=16,
        background=me.theme_var("surface"),
        border_radius=8
    )):
        me.text("Welcome to my Mesop app!", type="headline-4")
        
        for i in range(6):
            with me.box(style=me.Style(
                background=me.theme_var("background"),
                padding=me.Padding.all(16),
                border_radius=8,
                box_shadow="0 2px 4px rgba(0,0,0,0.1)"
            )):
                me.text(f"Grid Item {i+1}", type="subtitle-1")
                me.text("This is a sample grid item content.", type="body-2")
                me.button("Click me", type="flat", style=me.Style(margin=me.Margin(top=8)))