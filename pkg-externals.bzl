# Forked from: https://github.com/angular/components/blob/ff67a416d19e9237607605bec0d7cc372025387f/pkg-externals.bzl

# Base list of externals which should not be bundled into the APF package output.
# Note that we want to disable sorting of the externals as we manually group entries.
# buildifier: disable=unsorted-list-items
PKG_EXTERNALS = [
    # Framework packages.
    "@angular/animations",
    "@angular/common",
    "@angular/common/http",
    "@angular/common/http/testing",
    "@angular/common/testing",
    "@angular/core",
    "@angular/core/testing",
    "@angular/forms",
    "@angular/platform-browser",
    "@angular/platform-browser-dynamic",
    "@angular/platform-browser-dynamic/testing",
    "@angular/platform-browser/animations",
    "@angular/platform-server",
    "@angular/router",

    # Primary entry-points in the project.
    "@angular/cdk",
    "@angular/cdk-experimental",
    "@angular/google-maps",
    "@angular/material",
    "@angular/material-experimental",
    "@angular/material-moment-adapter",
    "@angular/material-luxon-adapter",
    "@angular/material-date-fns-adapter",
    "@angular/youtube-player",

    # Third-party libraries.
    "kagekiri",
    "moment",
    "moment/locale/fr",
    "moment/locale/ja",
    "luxon",
    "date-fns",
    "protractor",
    "rxjs",
    "rxjs/operators",
    "selenium-webdriver",

    # TODO: Remove slider deep dependencies after we remove depencies on MDC's javascript
    "@material/slider/adapter",
    "@material/slider/foundation",
    "@material/slider/types",
]
