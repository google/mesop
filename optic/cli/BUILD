load("//builddefs:defs.bzl", "py_binary", "py_library")
load("@my_deps//:requirements.bzl", "requirement")

# Prod CLI
py_binary(
    name = "cli",
    srcs = ["cli.py"],
    data = [
        "//optic",
        "//optic/examples",
        "//optic/testing:index",
    ],
    main = "cli.py",
    deps = [
        ":execute_module",
        requirement("absl-py"),
        "//optic",  # Keep dep to ensure the entire Optic library is loaded.
        "//optic/lib",
        "//optic/server:prod_server",
    ],
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
    deps = [
        ":execute_module",
        requirement("absl-py"),
        "//optic",  # Keep dep to ensure the entire Optic library is loaded.
        "//optic/lib",
        "//optic/server:dev_server",
    ],
)

py_library(
    name = "execute_module",
    srcs = [
        "__init__.py",
        "execute_module.py",
    ],
)
