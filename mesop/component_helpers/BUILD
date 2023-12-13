load("//build_defs:defaults.bzl", "py_library")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

py_library(
    name = "component_helpers",
    srcs = glob(["*.py"]),
    deps = [
        "//mesop/protos:ui_py_pb2",
        "//mesop/runtime",
    ],
)
