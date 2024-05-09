load("//mesop/components:defs.bzl", "mesop_component")
load("//build_defs:defaults.bzl", "THIRD_PARTY_PY_MARKDOWN", "THIRD_PARTY_PY_PYGMENTS")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

mesop_component(
    name = "markdown",
    py_deps = THIRD_PARTY_PY_MARKDOWN + THIRD_PARTY_PY_PYGMENTS,
)
