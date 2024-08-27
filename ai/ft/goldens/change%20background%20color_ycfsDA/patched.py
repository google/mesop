from dataclasses import dataclass, field

import mesop as me

_INTRO_TEXT = """
# Mesop Markdown Editor Example

This example shows how to make a simple markdown editor.
""".strip()


@dataclass(kw_only=True)
class Note:
  """Content of note."""

  content: str = ""


@me.stateclass
class State:
  notes: list[Note] = field(default_factory=lambda: [Note(content=_INTRO_TEXT)])
  selected_note_index: int = 0
  selected_note_content: str = _INTRO_TEXT
  show_preview: bool = True


@me.page(
  security_policy=me.SecurityPolicy(
    allowed_iframe_parents=["https://google.github.io"]
  ),
  path="/markdown_editor",
  title="Markdown Editor",
)
def page():
  state = me.state(State)

  with me.box(style=_style_container(state.show_preview)):
    # Note list column
    with me.box(style=_STYLE_NOTES_NAV):
      # Toolbar
      with me.box(style=_STYLE_TOOLBAR):
        with me.content_button(on_click=on_click_new):
          with me.tooltip(message="New note"):
            me.icon(icon="add_notes")
        with me.content_button(on_click=on_click_hide):
          with me.tooltip(
            message="Hide preview" if state.show_preview else "Show preview"
          ):
            me.icon(icon="hide_image")

      # Note list
      for index, note in enumerate(state.notes):
        with me.box(
          key=f"note-{index}",
          on_click=on_click_note,
          style=_style_note_row(index == state.selected_note_index),
        ):
          me.text(_render_note_excerpt(note.content))

    # Markdown Editor Column
    with me.box(style=_STYLE_EDITOR):
      me.native_textarea(
        value=state.selected_note_content,
        style=_STYLE_TEXTAREA,
        on_input=on_text_input,
      )

    # Markdown Preview Column
    if state.show_preview:
      with me.box(style=_STYLE_PREVIEW):
        if state.selected_note_index < len(state.notes):
          me.markdown(state.notes[state.selected_note_index].content)


# HELPERS

_EXCERPT_CHAR_LIMIT = 90


def _render_note_excerpt(content: str) -> str:
  if len(content) <= _EXCERPT_CHAR_LIMIT:
    return content
  return content[:_EXCERPT_CHAR_LIMIT] + "..."


# EVENT HANDLERS


def on_click_new(e: me.ClickEvent):
  state = me.state(State)
  # Need to update the initial value of the editor text area so we can
  # trigger a diff to reset the editor to empty. Need to yield this change.
  # for this to work.
  state.selected_note_content = state.notes[state.selected_note_index].content
  yield
  # Reset the initial value of the editor text area to empty since the new note
  # has no content.
  state.selected_note_content = ""
  state.notes.append(Note())
  state.selected_note_index = len(state.notes) - 1
  yield


def on_click_hide(e: me.ClickEvent):
  """Hides/Shows preview Markdown pane."""
  state = me.state(State)
  state.show_preview = bool(not state.show_preview)


def on_click_note(e: me.ClickEvent):
  """Selects a note from the note list."""
  state = me.state(State)
  note_id = int(e.key.replace("note-", ""))
  note = state.notes[note_id]
  state.selected_note_index = note_id
  state.selected_note_content = note.content


def on_text_input(e: me.InputEvent):
  """Captures text in editor."""
  state = me.state(State)
  state.notes[state.selected_note_index].content = e.value


# STYLES

_BACKGROUND_COLOR = "#fafafa"
_FONT_COLOR = "#555"
_NOTE_ROW_FONT_COLOR = "#777"
_NOTE_ROW_FONT_SIZE = "14px"
_SELECTED_ROW_BACKGROUND_COLOR = "#dee3eb"
_DEFAULT_BORDER_STYLE = me.BorderSide(width=1, style="solid", color="#bbb")


def _style_container(show_preview: bool = True) -> me.Style:
  return me.Style(
    background=me.theme_var("surface"),
    color=me.theme_var("on-surface"),
    display="grid",
    grid_template_columns="2fr 4fr 4fr" if show_preview else "2fr 8fr",
    height="100vh",
  )


def _style_note_row(selected: bool = False) -> me.Style:
  return me.Style(
    color=_NOTE_ROW_FONT_COLOR,
    font_size=_NOTE_ROW_FONT_SIZE,
    background=_SELECTED_ROW_BACKGROUND_COLOR if selected else "none",
    padding=me.Padding.all(10),
    border=me.Border(bottom=_DEFAULT_BORDER_STYLE),
    height="100px",
    overflow_x="hidden",
    overflow_y="hidden",
  )


_STYLE_NOTES_NAV = me.Style(overflow_y="scroll", padding=me.Padding.all(15))


_STYLE_TOOLBAR = me.Style(
  padding=me.Padding.all(5),
  border=me.Border(bottom=_DEFAULT_BORDER_STYLE),
)


_STYLE_EDITOR = me.Style(
  overflow_y="hidden",
  padding=me.Padding(left=20, right=15, top=20, bottom=0),
  border=me.Border(
    left=_DEFAULT_BORDER_STYLE,
    right=_DEFAULT_BORDER_STYLE,
  ),
)


_STYLE_PREVIEW = me.Style(
  overflow_y="scroll", padding=me.Padding.symmetric(vertical=0, horizontal=20)
)


_STYLE_TEXTAREA = me.Style(
  color=_FONT_COLOR,
  background=_BACKGROUND_COLOR,
  outline="none",  # Hides focus border
  border=me.Border.all(me.BorderSide(style="none")),
  width="100%",
  height="100%",
)
