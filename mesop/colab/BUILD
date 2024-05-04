load("//build_defs:defaults.bzl", "THIRD_PARTY_PY_PYTEST", "py_library", "py_test")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

py_library(
    name = "colab",
    srcs = glob(["*.py"]),
    deps = [
        "//mesop/runtime",
        "//mesop/server",
        "//mesop/utils",
    ],
)

py_test(
    name = "colab_run_test",
    srcs = ["colab_run_test.py"],
    deps = [":colab"] + THIRD_PARTY_PY_PYTEST,
)
