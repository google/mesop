load("//build_defs:defaults.bzl", "py_library")

package(
    default_visibility = ["//build_defs:optic_internal"],
)

py_library(
    name = "event_handler",
    srcs = glob(["*.py"]),
    deps = [
        "//optic/component_helpers",
        "//optic/events",
        "//optic/runtime",
        "//protos:ui_py_pb2",
    ],
)
