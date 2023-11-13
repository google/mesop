load("//tools:defaults.bzl", "esbuild_config", "ng_module")

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
