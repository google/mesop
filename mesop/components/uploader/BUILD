load("//mesop/components:defs.bzl", "mesop_component")
load("//build_defs:defaults.bzl", "sass_binary")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

mesop_component(
    name = "uploader",
    assets = [":uploader.css"],
)

sass_binary(
    name = "styles",
    src = "uploader.scss",
    sourcemap = False,
)
