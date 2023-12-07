load("//build_defs:defaults.bzl", "py_library")

package(
    default_visibility = ["//build_defs:optic_internal"],
)

py_library(
    name = "runtime",
    srcs = glob(["*.py"]),
    deps = [
        "//optic/dataclass_utils",
        "//optic/exceptions",
        "//optic/protos:ui_py_pb2",
    ],
)
