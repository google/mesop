load("//build_defs:defaults.bzl", "PYTHON_RUNFILES_DEP", "THIRD_PARTY_PY_PYDANTIC", "THIRD_PARTY_PY_PYTEST", "py_library", "py_test")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

py_library(
    name = "utils",
    srcs = glob(["*.py"]),
    deps = ["//mesop/protos:ui_py_pb2"] + PYTHON_RUNFILES_DEP + THIRD_PARTY_PY_PYDANTIC,
)

py_test(
    name = "caller_test",
    srcs = ["caller_test.py"],
    deps = [
        ":utils",
        "//mesop/protos:ui_py_pb2",
    ] + THIRD_PARTY_PY_PYTEST,
)
