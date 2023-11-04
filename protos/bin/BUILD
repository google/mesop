load("@my_deps//:requirements.bzl", "requirement")
load("//builddefs:defs.bzl", "py_binary")

py_binary(
    name = "protoc_gen_mypy",
    srcs = ["protoc_gen_mypy_wrapper.py"],
    main = "protoc_gen_mypy_wrapper.py",
    visibility = ["//visibility:public"],
    deps = [
        requirement("mypy-protobuf"),
    ],
)
