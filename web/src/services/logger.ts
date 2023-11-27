import { Injectable } from "@angular/core";
import * as pb from "optic/protos/ui_ts_proto_pb/protos/ui_pb";
import { TypeDeserializer } from "./type_deserializer";
import { ButtonType } from "optic/optic/components/button/button_ts_proto_pb/optic/components/button/button_pb";
import { TextType } from "optic/optic/components/text/text_ts_proto_pb/optic/components/text/text_pb";
import { BoxType } from "optic/optic/components/box/box_ts_proto_pb/optic/components/box/box_pb";
import { CheckboxType } from "optic/optic/components/checkbox/checkbox_ts_proto_pb/optic/components/checkbox/checkbox_pb";
import { TextInputType } from "optic/optic/components/text_input/text_input_ts_proto_pb/optic/components/text_input/text_input_pb";

@Injectable()
export class Logger {
  private logs: LogModel[] = [];
  private onLog?: () => void;

  constructor(private _typeDeserializer: TypeDeserializer) {
    console.log("constructed logger");
    _typeDeserializer.registerDeserializer("button", (value) =>
      ButtonType.deserializeBinary(value).toObject(),
    );
    _typeDeserializer.registerDeserializer("text", (value) =>
      TextType.deserializeBinary(value).toObject(),
    );
    _typeDeserializer.registerDeserializer("box", (value) =>
      BoxType.deserializeBinary(value).toObject(),
    );
    _typeDeserializer.registerDeserializer("checkbox", (value) =>
      CheckboxType.deserializeBinary(value).toObject(),
    );
    _typeDeserializer.registerDeserializer("text_input", (value) =>
      TextInputType.deserializeBinary(value).toObject(),
    );
  }

  log(input: LogInput) {
    this.logs.push(this.mapLog(input));
    this.onLog?.();
  }

  setOnLog(onLog: () => void) {
    this.onLog = onLog;
  }

  getLogs(): LogModel[] {
    return this.logs;
  }

  mapLog(input: LogInput): LogModel {
    switch (input.type) {
      case "StreamStart":
        return { type: "StreamStart", timestamp: Date.now() };
      case "StreamEnd":
        return { type: "StreamEnd", timestamp: Date.now() };
      case "UserEventLog":
        return {
          type: "UserEventLog",
          timestamp: Date.now(),
          userEvent: input.userEvent.toObject(),
        };
      case "RenderLog":
        const rootComponent = input.rootComponent.toObject();
        this.updateComponent(rootComponent);
        return {
          type: "RenderLog",
          timestamp: Date.now(),
          states: input.states
            .getStatesList()
            .map((s) => JSON.parse(s.getData())),
          rootComponent,
        };
    }
  }

  updateComponent(component: object): void {
    const type = (component as any)["type"];
    if (type) {
      type["value"] = this._typeDeserializer.deserialize(
        type["name"],
        type["value"],
      );
    }
    const children = (component as any)["childrenList"];
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
}

export interface StreamStartLogModel extends BaseLogModel {
  type: "StreamStart";
}

export interface StreamEndLogModel extends BaseLogModel {
  type: "StreamEnd";
}

export interface UserEventLogModel extends BaseLogModel {
  type: "UserEventLog";
  userEvent: object;
}

export interface RenderLogModel extends BaseLogModel {
  type: "RenderLog";
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
  type: "StreamStart";
}

export interface StreamEndLogInput extends BaseLogInput {
  type: "StreamEnd";
}

export interface UserEventLogInput extends BaseLogInput {
  type: "UserEventLog";
  userEvent: pb.UserEvent;
}

export interface RenderLogInput extends BaseLogInput {
  type: "RenderLog";
  rootComponent: pb.Component;
  states: pb.States;
}

export type LogInput =
  | StreamStartLogInput
  | StreamEndLogInput
  | UserEventLogInput
  | RenderLogInput;
