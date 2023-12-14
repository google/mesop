load("//build_defs:defaults.bzl", "py_binary", "py_library")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

py_library(
    name = "component_specs",
    srcs = glob(["*.py"]),
    deps = [
        "//mesop/protos:ui_py_pb2",
    ],
)

py_binary(
    name = "checkbox_spec",
    srcs = glob(["*.py"]),
    main = "checkbox_spec.py",
    deps = [
        # ":component_specs",
        "//mesop/protos:ui_py_pb2",
    ],
)
