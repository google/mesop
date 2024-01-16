load("//build_defs:defaults.bzl", "THIRD_PARTY_JS_RXJS")
load("//mesop/components:defs.bzl", "mesop_component")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

mesop_component(
    name = "input",
    ng_deps = ["//mesop/web/src/utils"] + THIRD_PARTY_JS_RXJS,
)
