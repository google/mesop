def _bind():
    """Bind targets for some external repositories"""

    # Needed by Protobuf
    native.bind(
        name = "python_headers",
        actual = str(Label("//third_party/python_runtime:headers")),
    )

def op_workspace():
    _bind()
