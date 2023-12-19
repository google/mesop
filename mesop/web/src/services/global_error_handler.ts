import {ErrorHandler, Injectable} from '@angular/core';

@Injectable()
export class GlobalErrorHandlerService implements ErrorHandler {
  onError!: (error: any) => void;
  constructor() {}

  setOnError(onError: (error: any) => void) {
    this.onError = onError;
  }

  handleError(error: any): void {
    console.error('[GlobalErrorHandlerService]', error);
    this.onError(error);
  }
}
