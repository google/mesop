load("//builddefs:defs.bzl", "py_binary", "py_library")
load("@my_deps//:requirements.bzl", "requirement")

package(
    default_visibility = ["//:optic_internal"],
)

py_library(
    name = "server",
    srcs = ["server.py"],
    deps = [
        requirement("flask"),
        "//protos:ui_py_proto",
    ],
)

py_binary(
    name = "dev_server",
    srcs = ["dev_server.py"],
    deps = [
        ":server",
    ],
)

py_binary(
    name = "prod_server",
    srcs = ["prod_server.py"],
    data = [
        "//web/src/app:web_package",
    ],
    deps = [
        ":server",
    ],
)
