load("//build_defs:defaults.bzl", "ts_library")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

ts_library(
    name = "marked",
    srcs = ["marked.ts"],
    deps = [
        "@npm//@types/marked",
        "@npm//marked",
    ],
)
