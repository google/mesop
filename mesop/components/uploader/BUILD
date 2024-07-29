load("//build_defs:defaults.bzl", "py_library", "sass_binary")
load("//mesop/components:defs.bzl", "mesop_component")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

mesop_component(
    name = "uploader",
    assets = [":uploader.css"],
    py_deps = [":uploaded_file"],
)

sass_binary(
    name = "styles",
    src = "uploader.scss",
    sourcemap = False,
)

py_library(
    name = "uploaded_file",
    srcs = ["uploaded_file.py"],
)
