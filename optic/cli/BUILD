load("@my_deps//:requirements.bzl", "requirement")
load("//build_defs:defaults.bzl", "py_binary", "py_library")

COMMON_DEPS = [
    ":execute_module",
    "//optic",  # Keep dep to ensure the entire Optic library is loaded.
    "//optic/exceptions",
    "//optic/runtime",
    requirement("absl-py"),
]

# Prod CLI
py_binary(
    name = "cli",
    srcs = ["cli.py"],
    data = [
        "//optic/examples",
        "//optic/testing:index",
        "//web/src/app/prod:web_package",
    ],
    main = "cli.py",
    deps = COMMON_DEPS,
)

# Dev CLI
py_binary(
    name = "dev_cli",
    srcs = ["dev_cli.py"],
    data = [
        "//optic/examples",
        "//optic/testing:index",
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
