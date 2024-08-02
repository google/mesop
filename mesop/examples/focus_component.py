import mesop as me


@me.page(path="/focus_component")
def page():
  with me.box(style=me.Style(margin=me.Margin.all(15))):
    me.select(
      options=[
        me.SelectOption(label="Autocomplete", value="autocomplete"),
        me.SelectOption(label="Checkbox", value="checkbox"),
        me.SelectOption(label="Input", value="input"),
        me.SelectOption(label="Link", value="link"),
        me.SelectOption(label="Radio", value="radio"),
        me.SelectOption(label="Select", value="select"),
        me.SelectOption(label="Slider", value="slider"),
        me.SelectOption(label="Slide Toggle", value="slide_toggle"),
        me.SelectOption(label="Textarea", value="textarea"),
        me.SelectOption(label="Uploader", value="uploader"),
      ],
      on_selection_change=on_selection_change,
    )

  me.divider()

  with me.box(
    style=me.Style(
      display="grid",
      gap=5,
      grid_template_columns="1fr 1fr",
      margin=me.Margin.all(15),
    )
  ):
    with me.box():
      me.autocomplete(
        key="autocomplete",
        label="Autocomplete",
        options=[
          me.AutocompleteOption(label="Test", value="Test"),
          me.AutocompleteOption(label="Test2", value="Tes2t"),
        ],
      )

    with me.box():
      me.checkbox("Checkbox", key="checkbox")

    with me.box():
      me.input(key="input", label="Input")

    with me.box():
      me.link(key="link", text="Test", url="https://google.com")

    with me.box():
      me.radio(
        key="radio",
        options=[
          me.RadioOption(label="Option 1", value="1"),
          me.RadioOption(label="Option 2", value="2"),
        ],
      )

    with me.box():
      me.select(
        key="select",
        label="Select",
        options=[
          me.SelectOption(label="label 1", value="value1"),
          me.SelectOption(label="label 2", value="value2"),
          me.SelectOption(label="label 3", value="value3"),
        ],
      )

    with me.box():
      me.slider(key="slider")

    with me.box():
      me.slide_toggle(key="slide_toggle", label="Slide toggle")

    with me.box():
      me.textarea(key="textarea", label="Textarea")

    with me.box():
      me.uploader(
        key="uploader",
        label="Upload Image",
        accepted_file_types=["image/jpeg", "image/png"],
        type="flat",
        color="primary",
        style=me.Style(font_weight="bold"),
      )


def on_selection_change(e: me.SelectSelectionChangeEvent):
  me.focus_component(key=e.value)
