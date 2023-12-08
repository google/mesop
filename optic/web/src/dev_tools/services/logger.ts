import {Injectable} from '@angular/core';
import {
  States,
  UserEvent,
  Component as ComponentProto,
} from 'optic/optic/protos/ui_jspb_proto_pb/optic/protos/ui_pb';
import {TypeDeserializer} from './type_deserializer';
import {Observable, Subject} from 'rxjs';
import {jsonParse} from '../../utils/strict_types';

@Injectable({
  providedIn: 'root',
})
export class Logger {
  private logs: LogModel[] = [];
  private onLog?: () => void;
  private logSubject = new Subject<LogModel[]>();

  constructor(private _typeDeserializer: TypeDeserializer) {}

  log(input: LogInput) {
    const logModel = this.mapLog(input);
    this.logs.push(logModel);
    this.logSubject.next(this.logs);
    this.onLog?.();
  }

  setOnLog(onLog: () => void) {
    this.onLog = onLog;
  }

  getLogs(): LogModel[] {
    return this.logs;
  }

  getLogObservable(): Observable<LogModel[]> {
    return this.logSubject.asObservable();
  }

  mapLog(input: LogInput): LogModel {
    const lastTimestamp = this.logs.length
      ? this.logs[this.logs.length - 1].timestamp
      : undefined;
    const duration = lastTimestamp ? Date.now() - lastTimestamp : undefined;
    switch (input.type) {
      case 'StreamStart':
        return {type: 'Stream Start', timestamp: Date.now(), duration};
      case 'StreamEnd':
        return {type: 'Stream End', timestamp: Date.now(), duration};
      case 'UserEventLog':
        return {
          type: 'User Event',
          timestamp: Date.now(),
          userEvent: input.userEvent.toObject(),
          duration,
        };
      case 'RenderLog':
        const rootComponent = input.rootComponent.toObject();
        this.updateComponent(rootComponent);
        return {
          type: 'Render',
          timestamp: Date.now(),
          duration,
          states: input.states
            .getStatesList()
            .map((s) => jsonParse(s.getData())) as object[],
          rootComponent,
        };
    }
  }

  updateComponent(component: object): void {
    const type = (component as any)['type'];
    if (type) {
      type['value'] = this._typeDeserializer.deserialize(
        type['name'],
        type['value'],
      );
    }
    const children = (component as any)['childrenList'];
    if (children) {
      for (const child of children) {
        this.updateComponent(child);
      }
    }
  }
}

export interface BaseLogModel {
  type: string;
  timestamp: number; // Use Date.now()
  duration: number | undefined;
}

export interface StreamStartLogModel extends BaseLogModel {
  type: 'Stream Start';
}

export interface StreamEndLogModel extends BaseLogModel {
  type: 'Stream End';
}

export interface UserEventLogModel extends BaseLogModel {
  type: 'User Event';
  userEvent: object;
}

export interface RenderLogModel extends BaseLogModel {
  type: 'Render';
  rootComponent: object;
  states: object[];
}

export type LogModel =
  | StreamStartLogModel
  | StreamEndLogModel
  | UserEventLogModel
  | RenderLogModel;

export interface BaseLogInput {
  type: string;
}

export interface StreamStartLogInput extends BaseLogInput {
  type: 'StreamStart';
}

export interface StreamEndLogInput extends BaseLogInput {
  type: 'StreamEnd';
}

export interface UserEventLogInput extends BaseLogInput {
  type: 'UserEventLog';
  userEvent: UserEvent;
}

export interface RenderLogInput extends BaseLogInput {
  type: 'RenderLog';
  rootComponent: ComponentProto;
  states: States;
}

export type LogInput =
  | StreamStartLogInput
  | StreamEndLogInput
  | UserEventLogInput
  | RenderLogInput;
