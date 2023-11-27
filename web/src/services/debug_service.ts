import { Injectable } from "@angular/core";

const SHOW_DEBUG_PANEL_KEY = "OPTIC://SHOW_DEBUG_PANEL_KEY";

@Injectable()
export class DebugService {
  constructor() {
    window.localStorage.getItem(SHOW_DEBUG_PANEL_KEY);
  }

  isDebugMode(): boolean {
    // TODO: configure this.
    return true;
  }

  showDebugPanel(): boolean {
    return window.localStorage.getItem(SHOW_DEBUG_PANEL_KEY) === "true";
  }

  toggleShowDebugPanel() {
    window.localStorage.setItem(
      SHOW_DEBUG_PANEL_KEY,
      (!this.showDebugPanel()).toString(),
    );
  }
}
