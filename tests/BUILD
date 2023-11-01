load("@rules_python//python:defs.bzl", "py_test")
load("@my_deps//:requirements.bzl", "requirement")

py_test(
    name = "hello_test",
    srcs = ["hello_test.py"],
    deps = [
        "//optic:hello",
        requirement("pytest"),
    ],
)
