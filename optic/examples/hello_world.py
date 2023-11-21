import optic as op


@op.page(path="/hello_world")
def hi():
    op.text(text="Hello, world!")
