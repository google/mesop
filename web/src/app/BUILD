load("//tools:defaults.bzl", "esbuild_config", "ng_module", "npm_sass_library", "sass_binary")

package(
    default_visibility = ["//:optic_internal"],
)

ng_module(
    name = "app",
    srcs = glob([
        "*.ts",
    ]),
    assets = [
        "app.html",
    ],
    deps = [
        "//protos:ui_ts_proto",
        "//web/src/component_renderer",
        "//web/src/services",
        "@npm//@angular/compiler",
    ],
)

esbuild_config(
    name = "esbuild_config",
    config_file = "esbuild.config.mjs",
)

npm_sass_library(
    name = "material_sass_deps",
    deps = [
        "@npm//@angular/cdk",
        "@npm//@angular/material",
    ],
)

sass_binary(
    name = "styles",
    src = "styles.scss",
    include_paths = ["external/npm/node_modules"],
    sourcemap = False,
    deps = [":material_sass_deps"],
)
