import mesop as me


@me.stateclass
class State:
  raw_value: str
  selected_value: str


@me.page(path="/components/autocomplete/e2e/autocomplete_app")
def app():
  state = me.state(State)

  with me.box(style=me.Style(margin=me.Margin.all(15))):
    me.autocomplete(
      label="Select state",
      options=_make_autocomplete_options(state.raw_value),
      require_selection=True,
      on_selection_change=on_value_change,
      on_enter=on_value_change,
      on_input=on_input,  # Needed to provide filtering support
    )

    if state.selected_value:
      me.text("Selected: " + state.selected_value)


def on_value_change(
  e: me.AutocompleteEnterEvent | me.AutocompleteSelectionChangeEvent,
):
  state = me.state(State)
  state.selected_value = e.value


def on_input(e: me.AutocompleteInputEvent):
  state = me.state(State)
  state.raw_value = e.value


def _make_autocomplete_options(prefix) -> list[me.AutocompleteOptionGroup]:
  """Creates and filter autocomplete options.

  The states list assumed to be alphabetized and we group by the first letter of the
  state's name.

  The filtering applied is a simple prefix filter. We filter on the server side to
  provide more flexibility.
  """
  states_options_list = []
  sub_group = None
  for state in _STATES:
    if not prefix or state.lower().startswith(prefix.lower()):
      if not sub_group or sub_group.label != state[0]:
        if sub_group:
          states_options_list.append(sub_group)
        sub_group = me.AutocompleteOptionGroup(label=state[0], options=[])
      sub_group.options.append(me.AutocompleteOption(label=state, value=state))
  if sub_group:
    states_options_list.append(sub_group)
  return states_options_list


_STATES = [
  "Alabama",
  "Alaska",
  "Arizona",
  "Arkansas",
  "California",
  "Colorado",
  "Connecticut",
  "Delaware",
  "Florida",
  "Georgia",
  "Hawaii",
  "Idaho",
  "Illinois",
  "Indiana",
  "Iowa",
  "Kansas",
  "Kentucky",
  "Louisiana",
  "Maine",
  "Maryland",
  "Massachusetts",
  "Michigan",
  "Minnesota",
  "Mississippi",
  "Missouri",
  "Montana",
  "Nebraska",
  "Nevada",
  "New Hampshire",
  "New Jersey",
  "New Mexico",
  "New York",
  "North Carolina",
  "North Dakota",
  "Ohio",
  "Oklahoma",
  "Oregon",
  "Pennsylvania",
  "Rhode Island",
  "South Carolina",
  "South Dakota",
  "Tennessee",
  "Texas",
  "Utah",
  "Vermont",
  "Virginia",
  "Washington",
  "West Virginia",
  "Wisconsin",
  "Wyoming",
]
