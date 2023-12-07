"""Wrapper for commonly used Bazel rules.
"""

load("@aspect_rules_py//py:defs.bzl", _py_binary = "py_binary", _py_library = "py_library")
load("@build_bazel_rules_nodejs//:index.bzl", _pkg_web = "pkg_web")
load("@my_deps//:requirements.bzl", "requirement")
load("@rules_proto//proto:defs.bzl", _proto_library = "proto_library")
load("@rules_proto_grpc//js:defs.bzl", "js_proto_library")
load("@rules_python//python:defs.bzl", _py_test = "py_test")
load("//build_defs:py_proto_library.bzl", _py_proto_library = "py_proto_library")
load("//tools:defaults.bzl", _esbuild = "esbuild", _esbuild_config = "esbuild_config", _ng_module = "ng_module", _npm_sass_library = "npm_sass_library", _sass_binary = "sass_binary", _ts_library = "ts_library")

# Re-export symbols
proto_library = _proto_library
py_binary = _py_binary
py_library = _py_library
py_proto_library = _py_proto_library
py_test = _py_test
esbuild = _esbuild
esbuild_config = _esbuild_config
ng_module = _ng_module
npm_sass_library = _npm_sass_library
pkg_web = _pkg_web
sass_binary = _sass_binary
ts_library = _ts_library

# Constants for deps
ANGULAR_CORE_DEPS = [
    "@npm//@angular/compiler",
]

ANGULAR_MATERIAL_TS_DEPS = [
    "@npm//@angular/material",
]

ANGULAR_MATERIAL_SASS_DEPS = [
    "@npm//@angular/material",
]

ANGULAR_CDK_TS_DEPS = [
    "@npm//@angular/cdk",
]

ANGULAR_CDK_SASS_DEPS = [
    "@npm//@angular/cdk",
]

JS_STATIC_FILES = [
    "@npm//:node_modules/moment/min/moment-with-locales.min.js",
    "@npm//:node_modules/rxjs/bundles/rxjs.umd.min.js",
    "@npm//:node_modules/zone.js/dist/zone.js",
]

THIRD_PARTY_PY_ABSL_PY = [
    requirement("absl-py"),
]

THIRD_PARTY_PY_FLASK = [
    requirement("flask"),
]

THIRD_PARTY_PYTEST = [
    requirement("pytest"),
]

THIRD_PARTY_MYPY_PROTOBUF = [
    requirement("mypy-protobuf"),
]

PYTHON_RUNFILES_DEP = [
    "@rules_python//python/runfiles",
]

def jspb_proto_library(name, deps):
    """
    Shim for JS proto.

    Args:
        name (str): The name of the rule.
        deps (list): A list of dependencies for the rule.

    Example:
        jspb_proto_library(
            name = "my_proto",
            deps = ["//proto:my_proto"],
        )
    """
    js_proto_library(
        name = name,
        protos = deps,
    )
