"""Wrapper for commonly used Bazel rules.
"""

load("@aspect_rules_py//py:defs.bzl", _py_binary = "py_binary", _py_library = "py_library")
load("@build_bazel_rules_nodejs//:index.bzl", _pkg_web = "pkg_web")
load("@my_deps//:requirements.bzl", "requirement")
load("@rules_proto//proto:defs.bzl", _proto_library = "proto_library")
load("@rules_python//python:defs.bzl", _py_test = "py_test")
load("//build_defs:jspb_proto_library.bzl", _jspb_proto_library = "jspb_proto_library")
load("//build_defs:py_proto_library.bzl", _py_proto_library = "py_proto_library")
load("//build_defs:sass_external_binary.bzl", _sass_external_binary = "sass_external_binary")
load("//tools:defaults.bzl", _devmode_esbuild = "devmode_esbuild", _esbuild = "esbuild", _esbuild_config = "esbuild_config", _http_server = "http_server", _ng_module = "ng_module", _sass_binary = "sass_binary", _ts_library = "ts_library")
load("//tools/angular:index.bzl", _LINKER_PROCESSED_FW_PACKAGES = "LINKER_PROCESSED_FW_PACKAGES")

# Re-export symbols
devmode_esbuild = _devmode_esbuild
esbuild = _esbuild
esbuild_config = _esbuild_config
http_server = _http_server
jspb_proto_library = _jspb_proto_library
ng_module = _ng_module
pkg_web = _pkg_web
proto_library = _proto_library
py_binary = _py_binary
py_library = _py_library
py_proto_library = _py_proto_library
py_test = _py_test
sass_binary = _sass_binary
sass_external_binary = _sass_external_binary
ts_library = _ts_library

# Constants for deps
ANGULAR_CORE_DEPS = [
    "@npm//@angular/compiler",
]

ANGULAR_MATERIAL_TS_DEPS = [
    "@npm//@angular/material",
]

ANGULAR_CDK_TS_DEPS = [
    "@npm//@angular/cdk",
]

JS_STATIC_FILES = [
    "@npm//:node_modules/moment/min/moment-with-locales.min.js",
    "@npm//:node_modules/rxjs/bundles/rxjs.umd.min.js",
    "@npm//:node_modules/zone.js/dist/zone.js",
]

LINKER_PROCESSED_FW_PACKAGES = _LINKER_PROCESSED_FW_PACKAGES

PYTHON_RUNFILES_DEP = [
    "@rules_python//python/runfiles",
]

THIRD_PARTY_JS_RXJS = [
    "@npm//rxjs",
]

THIRD_PARTY_PY_ABSL_PY = [
    requirement("absl-py"),
]

THIRD_PARTY_PY_FLASK = [
    requirement("flask"),
]

THIRD_PARTY_PY_PYDANTIC = [
    requirement("pydantic"),
]

THIRD_PARTY_PY_PYTEST = [
    requirement("pytest"),
]

THIRD_PARTY_PY_MYPY_PROTOBUF = [
    requirement("mypy-protobuf"),
]
