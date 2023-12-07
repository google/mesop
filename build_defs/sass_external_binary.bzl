"""
Wrapper for sass_binary if it depends on npm sass packages.
"""

load("//tools:defaults.bzl", "npm_sass_library", "sass_binary")

def sass_external_binary(name, deps = [], external_deps = [], **kw_args):
    library_name = name + "_lib"
    npm_sass_library(
        name = library_name,
        deps = external_deps,
    )
    sass_binary(
        name = name,
        include_paths = ["external/npm/node_modules"],
        deps = [":" + library_name] + deps,
        **kw_args
    )
