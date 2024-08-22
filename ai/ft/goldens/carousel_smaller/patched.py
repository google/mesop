import mesop as me

@me.stateclass
class State:
    current_image: int

def next_image(e: me.ClickEvent):
    state = me.state(State)
    state.current_image = (state.current_image + 1) % len(images)

def prev_image(e: me.ClickEvent):
    state = me.state(State)
    state.current_image = (state.current_image - 1) % len(images)

images = [
    "https://picsum.photos/id/1018/800/400",
    "https://picsum.photos/id/1015/800/400",
    "https://picsum.photos/id/1019/800/400",
]

@me.page()
def image_carousel():
    state = me.state(State)
    
    with me.box(style=me.Style(display="flex", flex_direction="column", align_items="center", gap=24, padding=me.Padding.all(32))):
        me.text("Image Carousel", type="headline-3", style=me.Style(color=me.theme_var("primary"), margin=me.Margin(bottom=16)))
        
        with me.box(style=me.Style(position="relative", width=800, height=400, border_radius=16, overflow_x="hidden", box_shadow="0 4px 6px rgba(0, 0, 0, 0.1)")):
            me.image(src=images[state.current_image], alt=f"Image {state.current_image + 1}", 
                     style=me.Style(width="100%", height="100%"))
            
            with me.box(style=me.Style(position="absolute", top=0, left=0, right=0, bottom=0, 
                                       display="flex", justify_content="space-between", align_items="center", 
                                       padding=me.Padding.all(16))):
                with me.content_button(on_click=prev_image, style=me.Style(background=me.theme_var("surface"), color=me.theme_var("on-surface"), 
                                         border_radius=28, padding=me.Padding.all(12), opacity=0.8)):
                    me.icon(icon="chevron_left")
                with me.content_button(on_click=next_image, style=me.Style(background=me.theme_var("surface"), color=me.theme_var("on-surface"), 
                                         border_radius=28, padding=me.Padding.all(12), opacity=0.8)):
                    me.icon(icon="chevron_right")
        
        with me.box(style=me.Style(display="flex", align_items="center", gap=8, margin=me.Margin(top=16))):
            for i in range(len(images)):
                dot_style = me.Style(
                    width=12, 
                    height=12, 
                    border_radius=6, 
                    background=me.theme_var("primary") if i == state.current_image else me.theme_var("surface"),
                    border=me.Border.all(me.BorderSide(width=2, color=me.theme_var("primary"))),
                )
                me.box(style=dot_style)
        
        me.text(f"Image {state.current_image + 1} of {len(images)}", type="body-1", 
                style=me.Style(color=me.theme_var("on-surface-variant"), margin=me.Margin(top=8)))