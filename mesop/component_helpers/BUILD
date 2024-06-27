load("//build_defs:defaults.bzl", "THIRD_PARTY_PY_ABSL_PY", "THIRD_PARTY_PY_PYTEST", "py_library", "py_test")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

py_library(
    name = "component_helpers",
    srcs = glob(["*.py"]),
    deps = [
        "//mesop/events",
        "//mesop/protos:ui_py_pb2",
        "//mesop/runtime",
        "//mesop/utils",
    ] + THIRD_PARTY_PY_ABSL_PY,
)

py_test(
    name = "diff_component_test",
    srcs = ["diff_component_test.py"],
    deps = [
        ":component_helpers",
        "//mesop/server",
    ] + THIRD_PARTY_PY_PYTEST,
)

py_test(
    name = "helper_test",
    srcs = ["helper_test.py"],
    deps = [
        ":component_helpers",
        "//mesop/server",
    ] + THIRD_PARTY_PY_PYTEST,
)
