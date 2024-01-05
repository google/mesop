load("//build_defs:defaults.bzl", "esbuild_config", "sass_external_binary", "sass_library")

package(
    default_visibility = ["//build_defs:mesop_internal"],
)

esbuild_config(
    name = "esbuild_config",
    config_file = "esbuild.config.mjs",
)

sass_library(
    name = "normalize",
    srcs = [
        "_normalize.scss",
    ],
)

sass_external_binary(
    name = "styles",
    src = "styles.scss",
    external_deps = [
        "@npm//@angular/material",
    ],
    sourcemap = False,
    deps = [
        ":normalize",
    ],
)
