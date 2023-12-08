# Forked from: https://github.com/angular/components/blob/8ac3ca11add4ae194b2b79169559fb3dbad7e161/test/BUILD.bazel

load("//tools:defaults.bzl", "ts_library")

package(default_visibility = ["//visibility:public"])

exports_files(["bazel-karma-local-config.js"])

# Common set-up for all Angular Material and CDK tests.
ts_library(
    name = "angular_test_init",
    testonly = True,
    # This file *must* end with "spec" in order for "karma_web_test_suite" to load it.
    srcs = ["angular-test-init-spec.ts"],
    deps = [
        "@npm//@angular/core",
        "@npm//@angular/platform-browser-dynamic",
        "@npm//@types/jasmine",
    ],
)
