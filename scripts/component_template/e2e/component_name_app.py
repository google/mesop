import optic as op


@op.page(path="/components/component_name/e2e/component_name_app")
def app():
    op.component_name(label="Hello, world!")
