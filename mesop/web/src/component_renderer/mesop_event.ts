export const MESOP_EVENT_NAME = 'mesop-event';

export class MesopEvent<T> extends Event {
  payload: T;
  handlerId: string;

  constructor(handlerId: string, payload: T) {
    super(MESOP_EVENT_NAME, {bubbles: true});
    this.payload = payload;
    this.handlerId = handlerId;
  }
}

// Place it on the global object so that web component modules
// can consume this class without needing an explicit import
// (which would require publishing this to an npm package).
(window as any)['MesopEvent'] = MesopEvent;
