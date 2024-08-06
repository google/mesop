load("//build_defs:defaults.bzl", "THIRD_PARTY_PY_FLASK", "py_library")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

py_library(
    name = "runtime",
    srcs = glob(["*.py"]),
    deps = [
        "//mesop/dataclass_utils",
        "//mesop/events",
        "//mesop/exceptions",
        "//mesop/protos:ui_py_pb2",
        "//mesop/security",
        "//mesop/server:state_sessions",
        "//mesop/utils",
    ] + THIRD_PARTY_PY_FLASK,
)
