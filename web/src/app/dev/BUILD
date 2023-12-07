load("//build_defs:defaults.bzl", "ANGULAR_CORE_DEPS", "JS_STATIC_FILES", "LINKER_PROCESSED_FW_PACKAGES", "devmode_esbuild", "http_server", "ng_module")

package(
    default_visibility = ["//build_defs:optic_internal"],
)

ng_module(
    name = "main",
    srcs = glob([
        "*.ts",
    ]),
    deps = [
        "//web/src/app",
    ] + ANGULAR_CORE_DEPS,
)

devmode_esbuild(
    name = "bundles",
    config = "//web/src/app:esbuild_config",
    entry_points = [":main.ts"],
    platform = "browser",
    splitting = True,
    # We cannot use `ES2017` or higher as that would result in `async/await` not being downleveled.
    # ZoneJS needs to be able to intercept these as otherwise change detection would not work properly.
    target = "es2016",
    # Note: We add all linker-processed FW packages as dependencies here so that ESBuild will
    # map all framework packages to their linker-processed bundles from `tools/angular`.
    deps = LINKER_PROCESSED_FW_PACKAGES + [
        ":main",
    ],
)

# File group for all static files which are needed to serve the dev-app. These files are
# used in the devserver as runfiles and will be copied into the static web package that can
# be deployed on static hosting services (like firebase).
filegroup(
    name = "dev_app_static_files",
    srcs = [
        "//web/src/app:index.html",
        "//web/src/app:styles",
    ] + JS_STATIC_FILES,
)

http_server(
    name = "server",
    srcs = ["//web/src/app:static_files"],
    additional_root_paths = [
        "npm/node_modules",
        # Needed for index.ng.html & style to be loaded.
        "optic/web/src/app",
        # Needed for compatibility with "pkg_web" which always uses the tree
        # artifact output as workspace root.
        "angular_material",
    ],
    enable_dev_ui = True,
    # List of environment variables that will be made available as `window.<NAME>` in the
    # served `index.ng.html` throuhg an injected script. Useful for allowing developers to
    # configure API keys without requiring secrets to be committed.
    environment_variables = [
        "OPTIC_SERVER_HOST",
    ],
    tags = ["manual"],
    deps = [
        ":bundles",
    ],
)
