import {Component, Input} from '@angular/core';
import {
  UserEvent,
  Key,
  Type,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {ComponentNameType} from 'mesop/mesop/components/component_name/component_name_jspb_proto_pb/mesop/components/component_name/component_name_pb';
import {Channel} from '../../web/src/services/channel';

@Component({
  templateUrl: 'component_name.ng.html',
  standalone: true,
  // GENERATE_NG_IMPORTS:
})
export class ComponentNameComponent {
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  private _config!: ComponentNameType;
  value!: any;

  constructor(private readonly channel: Channel) {}

  ngOnChanges() {
    this._config = ComponentNameType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
    this.value = this._config.getValue();
  }

  config(): ComponentNameType {
    return this._config;
  }

  // INSERT_EVENT_METHODS:
}
