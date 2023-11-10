load("@my_deps//:requirements.bzl", "requirement")
load("//builddefs:defs.bzl", "py_binary")

package(
    default_visibility = ["//:optic_internal"],
)

py_binary(
    name = "protoc_gen_mypy",
    srcs = ["protoc_gen_mypy_wrapper.py"],
    main = "protoc_gen_mypy_wrapper.py",
    deps = [
        requirement("mypy-protobuf"),
    ],
)
