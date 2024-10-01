# Update page title

If you want to update the page title, you can use `me.update_page title` which will
update the page title displayed on the browser tab.

This change does not persist if you navigate to a new page. The title will be
reset to the title configured in `me.page`.

## Example

```python
--8<-- "mesop/examples/update_page_title.py"
```

## API

::: mesop.commands.update_page_title.update_page_title
