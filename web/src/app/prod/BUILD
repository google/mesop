load("@build_bazel_rules_nodejs//:index.bzl", "pkg_web")
load("//build_defs:defaults.bzl", "esbuild", "ng_module")
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

# Target that builds a static web package of the dev-app. The web package can be
# deployed on static hosting services (such as firebase).
pkg_web(
    name = "web_package",
    srcs = [
        ":bundles",
        "//web/src/app:static_files",
    ],
    additional_root_paths = [
        "npm/node_modules",
        # Needed for index.html & style to be loaded.
        "web/src/app",
    ],
    tags = ["manual"],
)
