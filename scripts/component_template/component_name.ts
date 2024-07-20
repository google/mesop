import {ChangeDetectionStrategy, Component, Input} from '@angular/core';
import {
  Key,
  Type,
  UserEvent,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {ComponentNameType} from 'mesop/mesop/components/component_name/component_name_jspb_proto_pb/mesop/components/component_name/component_name_pb';
import {Channel} from '../../web/src/services/channel';

@Component({
  selector: 'mesop-{component-name}',
  templateUrl: '{component_name}.ng.html',
  standalone: true,
})
export class ComponentNameComponent {
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  private _config!: ComponentNameType;

  ngOnChanges() {
    this._config = ComponentNameType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
  }

  config(): ComponentNameType {
    return this._config;
  }
}
