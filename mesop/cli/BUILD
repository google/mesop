load(
    "//build_defs:defaults.bzl",
    "THIRD_PARTY_PY_ABSL_PY",
    "THIRD_PARTY_PY_FIREBASE_ADMIN",
    "THIRD_PARTY_PY_GREENLET",
    "THIRD_PARTY_PY_MATPLOTLIB",
    "THIRD_PARTY_PY_PANDAS",
    "THIRD_PARTY_PY_PYTEST",
    "THIRD_PARTY_PY_SQLALCHEMY",
    "py_binary",
    "py_library",
    "py_test",
)

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

COMMON_DATA = [
    "//mesop:example_index",
]

COMMON_DEPS = (
    [
        ":execute_module",
        "//mesop",  # Keep dep to ensure the entire Mesop library is loaded.
        "//mesop/exceptions",
        "//mesop/runtime",
    ] + THIRD_PARTY_PY_ABSL_PY +
    THIRD_PARTY_PY_MATPLOTLIB +
    THIRD_PARTY_PY_PANDAS +
    THIRD_PARTY_PY_FIREBASE_ADMIN +
    THIRD_PARTY_PY_SQLALCHEMY +
    THIRD_PARTY_PY_GREENLET
)  # Used for /examples

exports_files(["cli.py"])

py_library(
    name = "cli_lib",
    srcs = ["cli.py"],
    visibility = ["//build_defs:mesop_users"],
    deps = COMMON_DEPS,
)

# Prod CLI
py_binary(
    name = "cli",
    srcs = ["cli.py"],
    data = COMMON_DATA + [
        "//mesop/web/src/app/editor:web_package",
        "//mesop/web/src/app/prod:web_package",
    ],
    main = "cli.py",
    tags = [
        # This tag instructs ibazel to pipe into stdin a event describing actions.
        "ibazel_notify_changes",
    ],
    # Need to expose for Colab usage
    visibility = ["//build_defs:mesop_users"],
    deps = [":cli_lib"],
)

# Editor CLI
py_binary(
    name = "editor_cli",
    srcs = ["cli.py"],
    data = COMMON_DATA + [
        "//mesop/web/src/app/editor:web_package",
    ],
    main = "cli.py",
    tags = [
        # This tag instructs ibazel to pipe into stdin a event describing actions.
        "ibazel_notify_changes",
    ],
    # Need to expose for Colab usage
    visibility = ["//build_defs:mesop_users"],
    deps = [":cli_lib"],
)

py_library(
    name = "execute_module",
    srcs = [
        "__init__.py",
        "execute_module.py",
    ],
)

py_test(
    name = "execute_module_test",
    srcs = ["execute_module_test.py"],
    deps = [
        ":execute_module",
        "//mesop/utils",
    ] + THIRD_PARTY_PY_PYTEST,
)
