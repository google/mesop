import optic as op


@op.page(path="/components/text_input/e2e/text_input_app")
def app():
    op.text_input(label="Hello, world!")
