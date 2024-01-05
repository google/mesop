import {Injectable} from '@angular/core';

const SHOW_LEFT_SIDENAV_KEY = 'MESOP://SHOW_LEFT_SIDENAV_KEY';
const SHOW_RIGHT_SIDENAV_KEY = 'MESOP://SHOW_RIGHT_SIDENAV_KEY';
const SHOW_DEV_TOOLS_KEY = 'MESOP://SHOW_DEV_TOOLS_KEY';
const CURRENT_DEV_TOOLS_PANEL_KEY = 'MESOP://CURRENT_DEV_TOOLS_PANEL_KEY';

@Injectable({
  providedIn: 'root',
})
export class DevToolsSettings {
  isDebugMode(): boolean {
    // TODO: configure this.
    return true;
  }

  showDevTools(): boolean {
    return window.localStorage.getItem(SHOW_DEV_TOOLS_KEY) === 'true';
  }

  toggleShowDevTools() {
    window.localStorage.setItem(
      SHOW_DEV_TOOLS_KEY,
      (!this.showDevTools()).toString(),
    );
  }

  showLeftSidenav(): boolean {
    return window.localStorage.getItem(SHOW_LEFT_SIDENAV_KEY) === 'true';
  }

  toggleShowLeftSidenav() {
    window.localStorage.setItem(
      SHOW_LEFT_SIDENAV_KEY,
      (!this.showLeftSidenav()).toString(),
    );
  }

  showRightSidenav(): boolean {
    return window.localStorage.getItem(SHOW_RIGHT_SIDENAV_KEY) === 'true';
  }

  toggleShowRightSidenav() {
    window.localStorage.setItem(
      SHOW_RIGHT_SIDENAV_KEY,
      (!this.showRightSidenav()).toString(),
    );
  }

  getCurrentDevToolsPanel(): Panel {
    return Number(window.localStorage.getItem(CURRENT_DEV_TOOLS_PANEL_KEY));
  }

  setCurrentDevToolsPanel(panel: Panel) {
    return window.localStorage.setItem(
      CURRENT_DEV_TOOLS_PANEL_KEY,
      panel.toString(),
    );
  }
}

export enum Panel {
  Editor = 0,
  Components = 1,
  Logs = 2,
}
