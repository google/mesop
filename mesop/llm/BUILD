load("//build_defs:defaults.bzl", "THIRD_PARTY_PY_GOOGLE_GENERATIVEAI", "py_library")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

py_library(
    name = "llm",
    srcs = glob(["*.py"]),
    data = ["prompt.txt"],
    deps = THIRD_PARTY_PY_GOOGLE_GENERATIVEAI,
)
