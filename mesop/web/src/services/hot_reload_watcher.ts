/**
 * This module primarily serves as an interface for the
 * hot reloader mechanism used in downstream.
 */

import {Injectable} from '@angular/core';
import {Channel} from './channel';

const anyWindow = window as any;

export abstract class HotReloadWatcher {
  constructor(private readonly channel: Channel) {}

  handleReload() {
    this.channel.hotReload();
  }
}

/** Simple implementation of a hot reload watcher. */
@Injectable()
export class DefaultHotReloadWatcher extends HotReloadWatcher {
  constructor(channel: Channel) {
    super(channel);
    channel.checkForHotReload();
  }
}
