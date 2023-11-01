load("@rules_python//python:defs.bzl", "py_binary", "py_library")
load("@rules_python//python:pip.bzl", "compile_pip_requirements")

package(
    default_visibility = [":internal"],
)

package_group(
    name = "internal",
    packages = [
        "//...",
    ],
)

py_library(
    name = "hello",
    srcs = ["hello.py"],
)

py_binary(
    name = "hello_binary",
    srcs = ["hello.py"],
    main = "hello.py",
)

compile_pip_requirements(
    name = "pip_requirements",
    requirements_in = ":requirements.txt",
    requirements_txt = ":requirements_lock.txt",
)
