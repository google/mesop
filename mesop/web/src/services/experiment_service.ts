import {Injectable} from '@angular/core';

interface ExperimentSettings {
  readonly websocketsEnabled: boolean;
  readonly concurrentUpdatesEnabled: boolean;
  readonly experimentalEditorToolbarEnabled: boolean;
}

@Injectable({
  providedIn: 'root',
})
export class ExperimentService {
  private readonly settings: ExperimentSettings;

  constructor() {
    const windowSettings = (window as any).__MESOP_EXPERIMENTS__;
    this.settings = windowSettings ?? {
      websocketsEnabled: false,
    };
  }

  get websocketsEnabled(): boolean {
    return this.settings.websocketsEnabled;
  }
}
