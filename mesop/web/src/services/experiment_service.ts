import {Injectable} from '@angular/core';

interface ExperimentSettings {
  websocketsEnabled: boolean;
  concurrentUpdatesEnabled: boolean;
  experimentalEditorToolbarEnabled: boolean;
}

@Injectable({
  providedIn: 'root',
})
export class ExperimentService {
  private readonly settings: ExperimentSettings;

  constructor() {
    // Get experiment settings from window object
    const windowSettings = (window as any).__MESOP_EXPERIMENTS__;
    this.settings = windowSettings ?? {
      websocketsEnabled: false,
      concurrentUpdatesEnabled: false,
      experimentalEditorToolbarEnabled: false,
    };
  }

  get websocketsEnabled(): boolean {
    return this.settings.websocketsEnabled;
  }

  get concurrentUpdatesEnabled(): boolean {
    return this.settings.concurrentUpdatesEnabled;
  }

  get experimentalEditorToolbarEnabled(): boolean {
    return this.settings.experimentalEditorToolbarEnabled;
  }
}
