import { Injectable } from "@angular/core";

@Injectable()
export class DebugService {
  constructor() {}

  isDebugMode(): boolean {
    // TODO: configure this.
    return true;
  }

  showDebugPanel(): boolean {
    return true;
  }
}
