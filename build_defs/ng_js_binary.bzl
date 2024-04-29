"""Wrapper for building a js binary.
"""

load("@bazel_skylib//rules:copy_file.bzl", "copy_file")
load("//build_defs/app_bundle:index.bzl", "app_bundle")
load("//tools:defaults.bzl", "esbuild")
load("//tools/angular:index.bzl", "LINKER_PROCESSED_FW_PACKAGES")

def ng_js_binary(name, deps = [], entry_points = [], **kwargs):
    esbuild(
        name = name,
        config = "//mesop/web/src/app:esbuild_config",
        entry_points = entry_points,
        platform = "browser",
        splitting = True,
        # We cannot use `ES2017` or higher as that would result in `async/await` not being downleveled.
        # ZoneJS needs to be able to intercept these as otherwise change detection would not work properly.
        target = "es2016",
        deps = LINKER_PROCESSED_FW_PACKAGES + deps,
        **kwargs
    )

# This rule was based on what tensorboard did:
# https://github.com/tensorflow/tensorboard/blob/4023658707d54976622c3b3a32f5a4a215689da7/tensorboard/defs/defs.bzl#L93
def ng_js_binary_prod(
        name,
        **kwargs):
    """Rule for creating a prod-optimized JavaScript bundle for an Angular app.
    This uses the Angular team's internal toolchain for creating these bundles:
    app_bundle(). This toolchain is not officially supported. We use it at our
    own risk.
    The bundles allow for Angular AOT compilation and are further optimized to
    reduce size. However, the bundle times are significantly slower than those
    for ng_js_binary().
    Args:
        name: Name of the target.
        **kwargs: Other keyword arguments to app_bundle() and esbuild(). Typically
          used for entry_point and deps. Please refer to
          https://esbuild.github.io/api/ for more details.
    """

    app_bundle_name = "%s_app_bundle" % name
    app_bundle(
        config = "//mesop/web/src/app:esbuild_config",
        name = app_bundle_name,
        **kwargs
    )

    # app_bundle() generates several outputs. We copy the one that has gone
    # through a terser pass to be the output of this rule.
    copy_file(
        name = name + "_copy",
        src = "%s.min.js" % app_bundle_name,
        out = "%s.js" % name,
    )

    native.filegroup(
        name = name,
        srcs = ["%s.js" % name, "%s.min.js.map" % app_bundle_name],
    )
