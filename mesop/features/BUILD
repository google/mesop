load("//build_defs:defaults.bzl", "THIRD_PARTY_PY_PYTEST", "py_library", "py_test")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

py_library(
    name = "features",
    srcs = glob(
        ["*.py"],
        exclude = ["*_test.py"],
    ),
    deps = [
        "//mesop/runtime",
    ],
)

py_test(
    name = "query_params_test",
    srcs = ["query_params_test.py"],
    deps = [
        ":features",
    ] + THIRD_PARTY_PY_PYTEST,
)
