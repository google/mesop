# Build / Toolchain

## Context

Because Optic is a Google open-source project and we want to provide a good integration with Google's internal codebase, Optic uses Google's build system Bazel.

Although Bazel is similar to the [internal tool](https://bazel.build/about/faq#did_you_rewrite_your_internal_tool_as_open-source_is_it_a_fork), there's numerous differences, particularly around the ecosystems, which makes it quite a challenge to maintain Optic for both open-source and internal builds. Nevertheless, it's important that we do this to serve both communities well.

## Differences

We try to isolate as much of the differences between these two environments into the `build_defs/` directory. Different versions of the same files inside `build_defs/` are maintained for each environment. In particular, `build_defs/defaults.bzl` is meant to wrap all external rules/macros used by Optic so we can swap it between the internal and external variants as needed.

Finally, all external dependencies, e.g. Python's `requirement('$package')` or NPM's `@npm//$package`, are referenced via an indirection to build_defs/defaults.bzl. This is because Google has a special approach to handling third-party dependencies.

## Angular

We rely heavily on Angular's toolchain, particularly around Bazel integration. Many of the Web-related Bazel rules, particularly for Angular/TS code was forked from [github.com/angular/components](https://github.com/angular/components).
