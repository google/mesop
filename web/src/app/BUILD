# Forked from: https://github.com/angular/components/blob/ff67a416d19e9237607605bec0d7cc372025387f/src/dev-app/BUILD.bazel

load("@build_bazel_rules_nodejs//:index.bzl", "pkg_web")
load("//tools:defaults.bzl", "devmode_esbuild", "esbuild_config", "http_server", "ng_module", "sass_binary")
load("//tools/angular:index.bzl", "LINKER_PROCESSED_FW_PACKAGES")

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

devmode_esbuild(
    name = "bundles",
    config = ":esbuild_config",
    entry_points = [":main.ts"],
    platform = "browser",
    splitting = True,
    # We cannot use `ES2017` or higher as that would result in `async/await` not being downleveled.
    # ZoneJS needs to be able to intercept these as otherwise change detection would not work properly.
    target = "es2016",
    # Note: We add all linker-processed FW packages as dependencies here so that ESBuild will
    # map all framework packages to their linker-processed bundles from `tools/angular`.
    deps = LINKER_PROCESSED_FW_PACKAGES + [
        ":app",
    ],
)

# Variables that are going to be inlined into the dev app index.html.
filegroup(
    name = "variables",
    # Note that we need the * in the pattern, because there's a lint rule which
    # doesn't allow single files in a `glob`. We have to use a glob, because the file is optional.
    srcs = glob(["*variables.json"]),
)

# File group for all static files which are needed to serve the dev-app. These files are
# used in the devserver as runfiles and will be copied into the static web package that can
# be deployed on static hosting services (like firebase).
filegroup(
    name = "dev_app_static_files",
    srcs = [
        "index.html",
        ":variables",
        "@npm//:node_modules/moment/min/moment-with-locales.min.js",
        "@npm//:node_modules/rxjs/bundles/rxjs.umd.min.js",
        "@npm//:node_modules/zone.js/dist/zone.js",
    ],
)

http_server(
    name = "devserver",
    srcs = [":dev_app_static_files"],
    additional_root_paths = [
        "npm/node_modules",
        # Needed for compatibility with "pkg_web" which always uses the tree
        # artifact output as workspace root.
        "angular_material",
    ],
    enable_dev_ui = True,
    # List of environment variables that will be made available as `window.<NAME>` in the
    # served `index.html` throuhg an injected script. Useful for allowing developers to
    # configure API keys without requiring secrets to be committed.
    environment_variables = [
        "OPTIC_SERVER_HOST",
    ],
    tags = ["manual"],
    deps = [
        ":bundles",
    ],
)

# Target that builds a static web package of the dev-app. The web package can be
# deployed on static hosting services (such as firebase).
pkg_web(
    name = "web_package",
    srcs = [
        ":bundles",
        ":dev_app_static_files",
    ],
    additional_root_paths = [
        "npm/node_modules",
    ],
    tags = ["manual"],
)
