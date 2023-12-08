// Forked from: https://github.com/angular/components/blob/8ac3ca11add4ae194b2b79169559fb3dbad7e161/test/angular-test-init-spec.ts

/**
 * @license
 * Copyright Google LLC All Rights Reserved.
 *
 * Use of this source code is governed by an MIT-style license that can be
 * found in the LICENSE file at https://angular.io/license
 */

import {TestBed} from '@angular/core/testing';
import {
  BrowserDynamicTestingModule,
  platformBrowserDynamicTesting,
} from '@angular/platform-browser-dynamic/testing';

/*
 * Common setup / initialization for all unit tests in Angular Material and CDK.
 */

TestBed.initTestEnvironment(
  [BrowserDynamicTestingModule],
  platformBrowserDynamicTesting(),
);

(window as any).module = {};
(window as any).isNode = false;
(window as any).isBrowser = true;
(window as any).global = window;
