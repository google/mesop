import mesop as me

@me.stateclass
class State:
    input_text: str
    summary: str

def summarize(e: me.ClickEvent):
    state = me.state(State)
    # Simple summarization by taking the first sentence
    state.summary = state.input_text.split('.')[0] + '.'

def on_input(e: me.InputEvent):
    state = me.state(State)
    state.input_text = e.value

@me.page()
def summarizer_page():
    state = me.state(State)
    
    with me.box(style=me.Style(padding=me.Padding.all(24), max_width=600, margin=me.Margin.symmetric(horizontal="auto"))):
        me.text("Text Summarizer", type="headline-4", style=me.Style(margin=me.Margin(bottom=16)))
        
        me.textarea(
            label="Enter text to summarize",
            on_input=on_input,
            style=me.Style(width="100%", margin=me.Margin(bottom=16)),
            rows=5
        )
        
        me.button(
            "Summarize",
            on_click=summarize,
            type="flat",
            style=me.Style(margin=me.Margin(bottom=16))
        )
        
        if state.summary:
            with me.box(style=me.Style(
                background=me.theme_var("surface"),
                padding=me.Padding.all(16),
                border_radius=8
            )):
                me.text("Summary:", type="subtitle-1", style=me.Style(margin=me.Margin(bottom=8)))
                me.text(state.summary)