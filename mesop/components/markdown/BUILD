load("//mesop/components:defs.bzl", "mesop_component")
load("//build_defs:defaults.bzl", "THIRD_PARTY_JS_HIGHLIGHTJS")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

mesop_component(
    name = "markdown",
    ng_deps = ["//mesop/web/third_party:marked"] + THIRD_PARTY_JS_HIGHLIGHTJS,
)
