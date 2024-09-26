import mesop as me


@me.stateclass
class FeedbackState:
  feedback: str = ""
  reason: str = ""
  ask_reason: bool = False


def on_feedback(isup: bool):
  state = me.state(FeedbackState)
  state.feedback = "Thumbs up!" if isup else "Thumbs down!"
  state.ask_reason = not isup


def on_reason_input(e: me.InputEvent):
  state = me.state(FeedbackState)
  state.reason = e.value


def load(e: me.LoadEvent):
  me.set_theme_mode("system")


@me.page(
  on_load=load,
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/feedback",
)
def feedback_page():
  state = me.state(FeedbackState)
  with me.box(style=me.Style(margin=me.Margin.all(15))):
    me.text("Provide your feedback:", type="headline-5")

    with me.box(style=me.Style(display="flex", flex_direction="row", gap=20)):
      with me.content_button(type="icon", on_click=lambda _: on_feedback(True)):
        me.icon("thumb_up")
      with me.content_button(
        type="icon", on_click=lambda _: on_feedback(False)
      ):
        me.icon("thumb_down")

    if state.ask_reason:
      with me.box(style=me.Style(margin=me.Margin(top=15))):
        me.textarea(label="Tell us why", on_input=on_reason_input)

    if state.feedback:
      with me.box(style=me.Style(margin=me.Margin(top=15))):
        me.text(f"\n\nFeedback : {state.feedback}")
        if state.reason:
          me.text(f"Reason : {state.reason}")
