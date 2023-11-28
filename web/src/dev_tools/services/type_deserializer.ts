import { Injectable } from "@angular/core";
import { ButtonType } from "optic/optic/components/button/button_ts_proto_pb/optic/components/button/button_pb";
import { TextType } from "optic/optic/components/text/text_ts_proto_pb/optic/components/text/text_pb";
import { BoxType } from "optic/optic/components/box/box_ts_proto_pb/optic/components/box/box_pb";
import { CheckboxType } from "optic/optic/components/checkbox/checkbox_ts_proto_pb/optic/components/checkbox/checkbox_pb";
import { TextInputType } from "optic/optic/components/text_input/text_input_ts_proto_pb/optic/components/text_input/text_input_pb";

type Deserializer = (value: Uint8Array) => object;

@Injectable()
export class TypeDeserializer {
  private _map = new Map<string, Deserializer>();
  constructor() {
    this.registerDeserializer("button", (value) =>
      ButtonType.deserializeBinary(value).toObject(),
    );
    this.registerDeserializer("text", (value) =>
      TextType.deserializeBinary(value).toObject(),
    );
    this.registerDeserializer("box", (value) =>
      BoxType.deserializeBinary(value).toObject(),
    );
    this.registerDeserializer("checkbox", (value) =>
      CheckboxType.deserializeBinary(value).toObject(),
    );
    this.registerDeserializer("text_input", (value) =>
      TextInputType.deserializeBinary(value).toObject(),
    );
  }

  registerDeserializer(type: string, deserializer: Deserializer) {
    this._map.set(type, deserializer);
  }

  deserialize(type: string, value: Uint8Array): object {
    const deserializer = this._map.get(type);
    if (!deserializer) {
      throw new Error("Did not find deserializer for type=" + type);
    }
    return deserializer(value);
  }
}
