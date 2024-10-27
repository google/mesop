load("//build_defs:defaults.bzl", "THIRD_PARTY_PY_PYTEST", "py_library", "py_test")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

py_library(
    name = "security",
    srcs = glob(
        ["*.py"],
        exclude = [
            "*_test.py",
        ],
    ),
    deps = [
        "//mesop/exceptions",
    ],
)

py_test(
    name = "security_policy_test",
    srcs = ["security_policy_test.py"],
    deps = [":security"] + THIRD_PARTY_PY_PYTEST,
)
