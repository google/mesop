load("//build_defs:defaults.bzl", "THIRD_PARTY_PY_ABSL_PY", "py_binary", "py_library")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

COMMON_DEPS = [
    ":execute_module",
    "//mesop",  # Keep dep to ensure the entire Mesop library is loaded.
    "//mesop/exceptions",
    "//mesop/runtime",
    "//mesop/utils",
] + THIRD_PARTY_PY_ABSL_PY

# Prod CLI
py_binary(
    name = "cli",
    srcs = ["cli.py"],
    data = [
        "//mesop/examples",
        "//mesop/testing:index",
        "//mesop/web/src/app/prod:web_package",
    ],
    main = "cli.py",
    tags = [
        # This tag starts the live_reload server inside iBazel and instructs it to send reload events to webbrowsers.
        "ibazel_live_reload",
        # This tag instructs ibazel to pipe into stdin a event describing actions.
        "ibazel_notify_changes",
    ],
    deps = COMMON_DEPS,
)

# Dev CLI
py_binary(
    name = "dev_cli",
    srcs = ["dev_cli.py"],
    data = [
        "//mesop/examples",
        "//mesop/testing:index",
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
