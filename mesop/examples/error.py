import mesop as me


@me.page(path="/error")
def hi():
    # Deliberately call with a non-existent argument.
    me.text(text="Hello, world!", bad_keyword="a")  # type: ignore
