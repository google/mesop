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


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/feedback",
)
def feedback_page():
  state = me.state(FeedbackState)

  me.text("Provide your feedback:", type="headline-5")

  with me.box(style=me.Style(display="flex", flex_direction="row", gap=20)):
    me.button("👍", type="flat", on_click=lambda _: on_feedback(True))
    me.button("👎", type="flat", on_click=lambda _: on_feedback(False))

  if state.ask_reason:
    me.textarea(label="Tell us why", on_input=on_reason_input)

  if state.feedback:
    me.text(f"\n\nFeedback : {state.feedback}")
    if state.reason:
      me.text(f"Reason : {state.reason}")
