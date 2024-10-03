# Set page title

If you want to set the page title, you can use `me.set_page_title` which will
set the page title displayed on the browser tab.

This change does not persist if you navigate to a new page. The title will be
reset to the title configured in `me.page`.

## Example

```python
--8<-- "mesop/examples/set_page_title.py"
```

## API

::: mesop.commands.set_page_title.set_page_title
