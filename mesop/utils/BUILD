load("//build_defs:defaults.bzl", "PYTHON_RUNFILES_DEP", "THIRD_PARTY_PY_PYDANTIC", "THIRD_PARTY_PY_PYTEST", "py_library", "py_test")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

py_library(
    name = "utils",
    srcs = glob(
        ["*.py"],
        exclude = ["*_test.py"],
    ),
    deps = ["//mesop/protos:ui_py_pb2"] + PYTHON_RUNFILES_DEP + THIRD_PARTY_PY_PYDANTIC,
)

py_test(
    name = "url_utils_test",
    srcs = ["url_utils_test.py"],
    deps = [
        ":utils",
    ] + THIRD_PARTY_PY_PYTEST,
)
