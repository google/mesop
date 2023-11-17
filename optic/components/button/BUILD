load("//tools:defaults.bzl", "ng_module")
load("@rules_proto//proto:defs.bzl", "proto_library")
load("@rules_proto_grpc//js:defs.bzl", "js_proto_library")
load("//builddefs:protos.bzl", "py_proto_library")
load("@my_deps//:requirements.bzl", "requirement")

package(
    default_visibility = ["//:optic_internal"],
)

ng_module(
    name = "ng",
    srcs = glob([
        "*.ts",
    ]),
    assets = glob([
        "*.html",
    ]),
    deps = [
        ":button_ts_proto",
        "//protos:ui_ts_proto",
        "//web/src/services",
        "@npm//@angular/compiler",
        "@npm//@angular/material",
    ],
)

py_library(
    name = "py",
    srcs = glob(["*.py"]),
    deps = [
        requirement("pydantic"),
        ":button_py_proto",
        "//optic/component_helpers",
        "//protos:ui_py_proto",
    ],
)

proto_library(
    name = "button_proto",
    srcs = ["button.proto"],
)

py_proto_library(
    name = "button_py_proto",
    srcs = ["button.proto"],
)

js_proto_library(
    name = "button_ts_proto",
    protos = [":button_proto"],
)
