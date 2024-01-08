import {Injectable} from '@angular/core';
import {Channel} from './channel';

const anyWindow = window as any;

export abstract class HotReloadWatcher {
  constructor(private readonly channel: Channel) {}

  handleReload() {
    this.channel.hotReload();
  }
}

/** Encapsulates all ibazel-specific implementation details of hot reload watcher. */
@Injectable()
export class IbazelHotReloadWatcher extends HotReloadWatcher {
  constructor(channel: Channel) {
    super(channel);
    if (anyWindow['LiveReload']) {
      this.monkeyPatchLiveReload();
    }
  }

  monkeyPatchLiveReload(): void {
    // Since I couldn't find an official livereload API to tap into
    // I'm hacking this by monkeypatching reloadPage, which is effectively
    // a wrapper around document.reload().
    anyWindow['LiveReload']['reloader']['reloadPage'] = () => {
      this.handleReload();
    };
  }
}
