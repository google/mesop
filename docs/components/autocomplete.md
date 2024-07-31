## Overview

Autocomplete allows the user to enter free text or select from a list of dynamic values
and is based on the [Angular Material autocomplete component](https://material.angular.io/components/autocomplete/overview).

This components only renders text labels and values.

The autocomplete filters by case-insensitively matching substrings of the option label.

Currently, there is no on blur event with this component since the blur event does not
get the selected value on the first blur. Due to this ambiguous behavior, the blur event
has been left out.

## Examples

<iframe class="component-demo" src="https://google.github.io/mesop/demo/?demo=autocomplete" style="height: 200px"></iframe>

```python
--8<-- "demo/autocomplete.py"
```

## API

::: mesop.components.autocomplete.autocomplete.autocomplete
::: mesop.components.autocomplete.autocomplete.AutocompleteOption
::: mesop.components.autocomplete.autocomplete.AutocompleteOptionGroup
::: mesop.components.autocomplete.autocomplete.AutocompleteEnterEvent
::: mesop.components.autocomplete.autocomplete.AutocompleteSelectionChangeEvent
::: mesop.events.InputEvent
