load("//build_defs:defaults.bzl", "THIRD_PARTY_PY_PYTEST", "py_test")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

py_test(
    name = "simple_test",
    srcs = glob(["*.py"]),
    deps = THIRD_PARTY_PY_PYTEST,
)
