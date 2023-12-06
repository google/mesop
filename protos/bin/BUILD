load("@my_deps//:requirements.bzl", "requirement")
load("//build_defs:defaults.bzl", "py_binary")

package(
    default_visibility = ["//build_defs:optic_internal"],
)

py_binary(
    name = "protoc_gen_mypy",
    srcs = ["protoc_gen_mypy_wrapper.py"],
    main = "protoc_gen_mypy_wrapper.py",
    deps = [
        requirement("mypy-protobuf"),
    ],
)
