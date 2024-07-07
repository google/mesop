import mesop as me


@me.content_component
def dialog(is_open: bool):
  """Renders a dialog component.

  The design of the dialog borrows from the Angular component dialog. So basically
  rounded corners and some box shadow.

  One current drawback is that it's not possible to close the dialog
  by clicking on the overlay background. This is due to
  https://github.com/google/mesop/issues/268.

  Args:
    is_open: Whether the dialog is visible or not.
  """
  with me.box(
    style=me.Style(
      background="rgba(0,0,0,0.4)",
      display="block" if is_open else "none",
      height="100%",
      overflow_x="auto",
      overflow_y="auto",
      position="fixed",
      width="100%",
      z_index=1000,
    )
  ):
    with me.box(
      style=me.Style(
        align_items="center",
        display="grid",
        height="100vh",
        justify_items="center",
      )
    ):
      with me.box(
        style=me.Style(
          background="#fff",
          border_radius=20,
          box_sizing="content-box",
          box_shadow=(
            "0 3px 1px -2px #0003, 0 2px 2px #00000024, 0 1px 5px #0000001f"
          ),
          margin=me.Margin.symmetric(vertical="0", horizontal="auto"),
          padding=me.Padding.all(20),
        )
      ):
        me.slot()


@me.content_component
def dialog_actions():
  """Helper component for rendering action buttons so they are right aligned.

  This component is optional. If you want to position action buttons differently,
  you can just write your own Mesop markup.
  """
  with me.box(
    style=me.Style(
      display="flex", justify_content="end", margin=me.Margin(top=20)
    )
  ):
    me.slot()
