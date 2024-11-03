load("//mesop/components:defs.bzl", "mesop_component")
load("//build_defs:defaults.bzl", "sass_binary")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

mesop_component(
    name = "expansion_panel",
    assets = [":expansion_panel.css"],
)

sass_binary(
    name = "styles",
    src = "expansion_panel.scss",
    sourcemap = False,
)
