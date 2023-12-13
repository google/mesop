load("//build_defs:defaults.bzl", "py_library")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

py_library(
    name = "event_handler",
    srcs = glob(["*.py"]),
    deps = [
        "//mesop/component_helpers",
        "//mesop/events",
        "//mesop/protos:ui_py_pb2",
        "//mesop/runtime",
    ],
)
