import optic as op


@op.page(path="/components/box/e2e/box_app")
def app():
    op.box(label="Hello, world!")
