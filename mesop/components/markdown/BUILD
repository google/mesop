load("//mesop/components:defs.bzl", "mesop_component")
load("//build_defs:defaults.bzl", "THIRD_PARTY_PY_MARKDOWN", "THIRD_PARTY_PY_PYGMENTS", "sass_binary")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

mesop_component(
    name = "markdown",
    assets = [":markdown.css"],
    py_deps = THIRD_PARTY_PY_MARKDOWN + THIRD_PARTY_PY_PYGMENTS,
)

sass_binary(
    name = "styles",
    src = "markdown.scss",
    sourcemap = False,
)
