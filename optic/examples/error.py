import optic as op


@op.page(path="/error")
def hi():
    # Deliberately call with a non-existent argument.
    op.text(text="Hello, world!", bad_keyword="a")  # type: ignore
