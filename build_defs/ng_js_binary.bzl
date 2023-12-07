"""Wrapper for building a js binary.
"""

load("//tools/angular:index.bzl", "LINKER_PROCESSED_FW_PACKAGES")
load("//tools:defaults.bzl", "esbuild")

def ng_js_binary(name, deps = [], entry_points = []):
    esbuild(
        name = name,
        config = "//web/src/app:esbuild_config",
        entry_points = entry_points,
        platform = "browser",
        splitting = True,
        # We cannot use `ES2017` or higher as that would result in `async/await` not being downleveled.
        # ZoneJS needs to be able to intercept these as otherwise change detection would not work properly.
        target = "es2016",
        deps = LINKER_PROCESSED_FW_PACKAGES + deps,
    )
