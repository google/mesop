load("//build_defs:defaults.bzl", "py_library")

package(
    default_visibility = ["//build_defs:optic_internal"],
)

py_library(
    name = "component_helpers",
    srcs = glob(["*.py"]),
    deps = [
        "//optic/runtime",
        "//protos:ui_py_pb2",
    ],
)
