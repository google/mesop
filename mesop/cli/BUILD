load("//build_defs:defaults.bzl", "THIRD_PARTY_PY_ABSL_PY", "THIRD_PARTY_PY_PYTEST", "py_binary", "py_library", "py_test")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

COMMON_DEPS = [
    ":execute_module",
    "//mesop",  # Keep dep to ensure the entire Mesop library is loaded.
    "//mesop/exceptions",
    "//mesop/runtime",
] + THIRD_PARTY_PY_ABSL_PY

exports_files(["cli.py"])

py_library(
    name = "cli_lib",
    srcs = ["cli.py"],
    deps = COMMON_DEPS,
)

# Prod CLI
py_binary(
    name = "cli",
    srcs = ["cli.py"],
    data = [
        "//mesop/examples",
        "//mesop/web/src/app/prod:web_package",
    ],
    main = "cli.py",
    tags = [
        # This tag starts the live_reload server inside iBazel and instructs it to send reload events to webbrowsers.
        "ibazel_live_reload",
        # This tag instructs ibazel to pipe into stdin a event describing actions.
        "ibazel_notify_changes",
    ],
    deps = [":cli_lib"],
)

# Dev CLI
py_binary(
    name = "dev_cli",
    srcs = ["dev_cli.py"],
    data = [
        "//mesop/examples",
    ],
    main = "dev_cli.py",
    deps = COMMON_DEPS,
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
