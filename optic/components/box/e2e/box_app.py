import optic as op


@op.page(path="/components/box/e2e/box_app")
def app():
    with op.box(label="Hello, world! Box"):
        op.text(text="hi")
        op.text(text="hi2")
