import optic as op


@op.page(path="/components/text/e2e/text_app")
def text():
    op.text(text="Hello, world!")
