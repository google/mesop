import {Injectable} from '@angular/core';
// REF(//scripts/gen_component.py):insert_component_jspb_proto_import
import {MarkdownType} from 'mesop/mesop/components/markdown/markdown_jspb_proto_pb/mesop/components/markdown/markdown_pb';
import {ButtonType} from 'mesop/mesop/components/button/button_jspb_proto_pb/mesop/components/button/button_pb';
import {TextType} from 'mesop/mesop/components/text/text_jspb_proto_pb/mesop/components/text/text_pb';
import {BoxType} from 'mesop/mesop/components/box/box_jspb_proto_pb/mesop/components/box/box_pb';
import {CheckboxType} from 'mesop/mesop/components/checkbox/checkbox_jspb_proto_pb/mesop/components/checkbox/checkbox_pb';
import {TextInputType} from 'mesop/mesop/components/text_input/text_input_jspb_proto_pb/mesop/components/text_input/text_input_pb';

type Deserializer = (value: Uint8Array) => object;

@Injectable({
  providedIn: 'root',
})
export class TypeDeserializer {
  private _map = new Map<string, Deserializer>();
  constructor() {
    // REF(//scripts/gen_component.py):insert_register_deserializer
    this.registerDeserializer('markdown', (value) =>
      MarkdownType.deserializeBinary(value).toObject(),
    );

    this.registerDeserializer('button', (value) =>
      ButtonType.deserializeBinary(value).toObject(),
    );
    this.registerDeserializer('text', (value) =>
      TextType.deserializeBinary(value).toObject(),
    );
    this.registerDeserializer('box', (value) =>
      BoxType.deserializeBinary(value).toObject(),
    );
    this.registerDeserializer('checkbox', (value) =>
      CheckboxType.deserializeBinary(value).toObject(),
    );
    this.registerDeserializer('text_input', (value) =>
      TextInputType.deserializeBinary(value).toObject(),
    );
  }

  registerDeserializer(type: string, deserializer: Deserializer) {
    this._map.set(type, deserializer);
  }

  deserialize(type: string, value: Uint8Array): object {
    const deserializer = this._map.get(type);
    if (!deserializer) {
      throw new Error('Did not find deserializer for type=' + type);
    }
    return deserializer(value);
  }
}
