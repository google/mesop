"""
This includes the BUILD rules which should be considered
as part of Mesop's public API.
"""

load("//build_defs:defaults.bzl", "py_binary")

def mesop_binary(name, srcs, data = [], deps = []):
    py_binary(
        name = name,
        srcs = srcs,
        data = data + ["//mesop/web/src/app/prod:web_package"],
        deps = deps + ["//mesop"],
    )
