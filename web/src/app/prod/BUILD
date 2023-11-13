load("@build_bazel_rules_nodejs//:index.bzl", "pkg_web")
load("//tools:defaults.bzl", "devmode_esbuild", "esbuild", "esbuild_config", "http_server", "ng_module", "sass_binary")
load("//tools/angular:index.bzl", "LINKER_PROCESSED_FW_PACKAGES")

package(
    default_visibility = ["//:optic_internal"],
)

ng_module(
    name = "main",
    srcs = glob([
        "*.ts",
    ]),
    deps = [
        "//web/src/app",
        "@npm//@angular/compiler",
    ],
)

esbuild(
    name = "bundles",
    config = "//web/src/app:esbuild_config",
    entry_points = [":main.ts"],
    platform = "browser",
    splitting = True,
    # We cannot use `ES2017` or higher as that would result in `async/await` not being downleveled.
    # ZoneJS needs to be able to intercept these as otherwise change detection would not work properly.
    target = "es2016",
    deps = LINKER_PROCESSED_FW_PACKAGES + [
        ":main",
    ],
)

# File group for all static files which are needed to serve the dev-app. These files are
# used in the devserver as runfiles and will be copied into the static web package that can
# be deployed on static hosting services (like firebase).
filegroup(
    name = "static_files",
    srcs = [
        "index.html",
        "@npm//:node_modules/moment/min/moment-with-locales.min.js",
        "@npm//:node_modules/rxjs/bundles/rxjs.umd.min.js",
        "@npm//:node_modules/zone.js/dist/zone.js",
    ],
)

# Target that builds a static web package of the dev-app. The web package can be
# deployed on static hosting services (such as firebase).
pkg_web(
    name = "web_package",
    srcs = [
        ":bundles",
        ":static_files",
    ],
    additional_root_paths = [
        "npm/node_modules",
    ],
    tags = ["manual"],
)
