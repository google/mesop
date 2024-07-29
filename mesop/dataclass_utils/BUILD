load("//build_defs:defaults.bzl", "THIRD_PARTY_PY_DEEPDIFF", "THIRD_PARTY_PY_PANDAS", "THIRD_PARTY_PY_PYTEST", "py_library", "py_test")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

py_library(
    name = "dataclass_utils",
    srcs = glob(
        ["*.py"],
        exclude = ["*_test.py"],
    ),
    deps = [
        "//mesop/components/uploader:uploaded_file",
        "//mesop/exceptions",
    ] + THIRD_PARTY_PY_DEEPDIFF,
)

py_test(
    name = "dataclass_utils_test",
    srcs = ["dataclass_utils_test.py"],
    deps = [
        ":dataclass_utils",
        "//mesop/components/uploader:uploaded_file",
    ] + THIRD_PARTY_PY_PYTEST + THIRD_PARTY_PY_PANDAS,
)

py_test(
    name = "diff_state_test",
    srcs = ["diff_state_test.py"],
    deps = [
        ":dataclass_utils",
        "//mesop/components/uploader:uploaded_file",
    ] + THIRD_PARTY_PY_PYTEST + THIRD_PARTY_PY_PANDAS,
)
