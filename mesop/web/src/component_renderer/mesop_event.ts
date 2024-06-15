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

(window as any)['MesopEvent'] = MesopEvent;
