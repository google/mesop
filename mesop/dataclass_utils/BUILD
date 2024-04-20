load("//build_defs:defaults.bzl", "THIRD_PARTY_PY_PANDAS", "THIRD_PARTY_PY_PYTEST", "py_library", "py_test")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

py_library(
    name = "dataclass_utils",
    srcs = glob(
        ["*.py"],
        exclude = ["*_test.py"],
    ),
    deps = ["//mesop/exceptions"],
)

py_test(
    name = "dataclass_utils_test",
    srcs = ["dataclass_utils_test.py"],
    deps = [":dataclass_utils"] + THIRD_PARTY_PY_PYTEST + THIRD_PARTY_PY_PANDAS,
)
