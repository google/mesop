load("//build_defs:defaults.bzl", "PYTHON_RUNFILES_DEP", "THIRD_PARTY_PY_PYDANTIC", "py_library")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

py_library(
    name = "utils",
    srcs = glob(["*.py"]),
    deps = PYTHON_RUNFILES_DEP + THIRD_PARTY_PY_PYDANTIC,
)
