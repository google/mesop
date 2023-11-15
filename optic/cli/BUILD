load("//builddefs:defs.bzl", "py_binary", "py_library")
load("@my_deps//:requirements.bzl", "requirement")

# Prod CLI
py_binary(
    name = "cli",
    srcs = ["cli.py"],
    data = [
        "//optic",
        "//optic/examples",
    ],
    main = "cli.py",
    deps = [
        ":read_module",
        requirement("absl-py"),
        "//optic/lib",
        "//optic/server:prod_server",
    ],
)

# Dev CLI
py_binary(
    name = "dev_cli",
    srcs = ["dev_cli.py"],
    data = [
        "//optic",
        "//optic/examples",
    ],
    main = "dev_cli.py",
    deps = [
        ":read_module",
        requirement("absl-py"),
        "//optic/lib",
        "//optic/server:dev_server",
    ],
)

py_library(
    name = "read_module",
    srcs = [
        "__init__.py",
        "read_module.py",
    ],
)
