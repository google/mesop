# Wrapper for commonly used Bazel rules.

load("@aspect_rules_py//py:defs.bzl", _py_binary = "py_binary", _py_library = "py_library")
load("@rules_proto_grpc//js:defs.bzl", "js_proto_library")
load("//build_defs:py_proto_library.bzl", _py_proto_library = "py_proto_library")
load("//tools:defaults.bzl", _esbuild = "esbuild", _esbuild_config = "esbuild_config", _ng_module = "ng_module", _npm_sass_library = "npm_sass_library", _sass_binary = "sass_binary", _ts_library = "ts_library")

# Re-export symbols
py_binary = _py_binary
py_library = _py_library
py_proto_library = _py_proto_library
esbuild = _esbuild
esbuild_config = _esbuild_config
ng_module = _ng_module
npm_sass_library = _npm_sass_library
sass_binary = _sass_binary
ts_library = _ts_library

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
