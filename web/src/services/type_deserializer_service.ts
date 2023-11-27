import { Injectable, defineInjectable } from "@angular/core";

type Deserializer = (value: Uint8Array) => object;

@Injectable()
export class TypeDeserializerService {
  private _map = new Map<string, Deserializer>();
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
