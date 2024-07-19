load("//build_defs:defaults.bzl", "sass_binary")
load("//mesop/components:defs.bzl", "mesop_component")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

mesop_component(
    name = "link",
    assets = ["link.css"],
    py_deps = ["//mesop/components/text:py"],
)

sass_binary(
    name = "styles",
    src = "link.scss",
    sourcemap = False,
)
