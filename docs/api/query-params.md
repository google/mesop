# Query Params API

## Overview

Query params, also sometimes called query string, provide a way to manage state in the URLs. They are useful for providing deep-links into your Mesop app.

## Example

Here's a simple working example that shows how you can read and write query params.

```py
@me.page(path="/examples/query_params/page_2")
def page_2():
  me.text(f"query_params={me.query_params}")
  me.button("Add query param", on_click=add_query_param)
  me.button("Navigate", on_click=navigate)

def add_query_param(e: me.ClickEvent):
  me.query_params["key"] = "value"

def navigate(e: me.ClickEvent):
  me.navigate("/examples/query_params", query_params=me.query_params)
```

## Usage

You can use query parameters from `me.query_params`, which has a dictionary-like interface, where the key is the parameter name and value is the parameter value.

### Get a query param value

```py
value: str = me.query_params['param_name']
```
This will raise a KeyError if the parameter doesn't exist. You can use `in` to check whether a key exists in `me.query_params`:

```py
if 'key' in me.query_params:
    print(me.query_params['key'])
```

???+ NOTE "Repeated query params"
    If a query param key is repeated, then you will get the _first_ value. If you want all the values use `get_all`.

### Get all values

To get all the values for a particular query parameter key, you can use `me.query_params.get_all`, which returns a sequence of parameter values (currently implemented as a `tuple`).

```py
all_values = me.query_params.get_all('param_name')
```

### Iterate

```py
for key in query_params:
  value = query_params[key]
```

### Set query param

```py
query_params['new_param'] = 'value'
```

### Set repeated query param

```py
query_params['repeated_param'] = ['value1', 'value2']
```

### Delete

```py
del query_params['param_to_delete']
```

## Patterns

### Navigate with existing query params

Here's an example of how to navigate to a new page with query parameters:

```py
def click_navigate_button(e: me.ClickEvent):
    me.query_params['q'] = "value"
    me.navigate('/search', query_params=me.query_params)
```

### Navigate with only new query params

You can also navigate by passing in a dictionary to `query_params` parameter for `me.navigate` if you do _not_ want to keep the existing query parameters.

```py
def click_navigate_button(e: me.ClickEvent):
    me.navigate('/search', query_params={"q": "value})
```
