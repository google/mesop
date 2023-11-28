import { Injectable } from "@angular/core";

const SHOW_DEV_TOOLS_KEY = "OPTIC://SHOW_DEV_TOOLS_KEY";

@Injectable()
export class DebugService {
  constructor() {
    window.localStorage.getItem(SHOW_DEV_TOOLS_KEY);
  }

  isDebugMode(): boolean {
    // TODO: configure this.
    return true;
  }

  showDevTools(): boolean {
    return window.localStorage.getItem(SHOW_DEV_TOOLS_KEY) === "true";
  }

  toggleShowDevTools() {
    window.localStorage.setItem(
      SHOW_DEV_TOOLS_KEY,
      (!this.showDevTools()).toString(),
    );
  }
}
