import {Injectable} from '@angular/core';
import {Channel} from './channel';
import {States} from 'optic/optic/protos/ui_jspb_proto_pb/optic/protos/ui_pb';

const HOT_RELOAD_STATE_KEY = '@optic/HOT_RELOAD_STATE_KEY';
const anyWindow = window as any;

@Injectable({
  providedIn: 'root',
})
export class HotReloadWatcher {
  constructor(private readonly channel: Channel) {
    if (anyWindow['LiveReload']) {
      this.monkeyPatchLiveReload();
    }
    this.initPreviousState();
  }

  initPreviousState() {
    const stored_state = localStorage.getItem(HOT_RELOAD_STATE_KEY);
    if (!stored_state) {
      return;
    }

    const states = States.deserializeBinary(
      new Uint8Array(JSON.parse(stored_state)),
    );
    this.channel.setStates(states);
    // Clear from local storage so if the user does a hard reload,
    // they are loading from an empty state (and not this hot reload state).
    localStorage.removeItem(HOT_RELOAD_STATE_KEY);
  }

  monkeyPatchLiveReload() {
    // Since I couldn't find an official livereload API to tap into
    // I'm hacking this by monkeypatching reloadPage, which is effectively
    // a wrapper around document.reload().
    // First, I serialize the latest state (if any) into local storage.
    // Then, I do the original reload functionality.
    const originalReload = anyWindow['LiveReload']['reloader']['reloadPage'];
    anyWindow['LiveReload']['reloader']['reloadPage'] = () => {
      const states = this.channel.getStates();
      if (!states) {
        return;
      }
      anyWindow.localStorage.setItem(
        HOT_RELOAD_STATE_KEY,
        JSON.stringify(Array.from(this.channel.getStates().serializeBinary())),
      );
      originalReload();
    };
  }
}
