load("//build_defs:defaults.bzl", "py_test")
load("@my_deps//:requirements.bzl", "requirement")

py_test(
    name = "simple_test",
    srcs = glob(["*.py"]),
    deps = [
        requirement("pytest"),
    ],
)
