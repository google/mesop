import {Injectable} from '@angular/core';
import {
  States,
  UserEvent,
  Component as ComponentProto,
  EditorEvent,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {Observable, Subject} from 'rxjs';
import {jsonParse} from '../../utils/strict_types';

@Injectable({
  providedIn: 'root',
})
export class Logger {
  private logs: LogModel[] = [];
  private onLog?: () => void;
  private logSubject = new Subject<LogModel[]>();

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
      case 'EditorEventLog':
        return {
          type: 'Editor Event',
          timestamp: Date.now(),
          editorEvent: input.editorEvent.toObject(),
          duration,
        };
      case 'RenderLog':
        return {
          type: 'Render',
          timestamp: Date.now(),
          duration,
          states: input.states
            .getStatesList()
            .map((s) => jsonParse(s.getData())) as object[],
          rootComponent: mapComponentToObject(input.rootComponent),
        };
    }
  }
}

export function mapComponentToObject(
  component: ComponentProto,
): ComponentObject {
  const debugJson = component.getType()?.getDebugJson();
  let type;
  if (debugJson) {
    type = {
      name: component.getType()!.getName(),
      value: jsonParse(debugJson) as object,
    };
  }
  return {
    type,
    key: component.getKey()?.getKey(),
    sourceCodeLocation: component.getSourceCodeLocation()?.toObject() ?? {},
    children: component
      .getChildrenList()
      .map((child) => mapComponentToObject(child)),
  };
}

export interface ComponentObject {
  type?: {
    name: string;
    value: object;
  };
  key?: string;
  children: ComponentObject[];
  sourceCodeLocation: object;
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

export interface EditorEventLogModel extends BaseLogModel {
  type: 'Editor Event';
  editorEvent: object;
}

export interface RenderLogModel extends BaseLogModel {
  type: 'Render';
  rootComponent: ComponentObject;
  states: object[];
}

export type LogModel =
  | StreamStartLogModel
  | StreamEndLogModel
  | UserEventLogModel
  | EditorEventLogModel
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

export interface EditorEventLogInput extends BaseLogInput {
  type: 'EditorEventLog';
  editorEvent: EditorEvent;
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
  | EditorEventLogInput
  | RenderLogInput;
