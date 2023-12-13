import {ChangeDetectionStrategy, Component, Input} from '@angular/core';
import {
  Click,
  Key,
  Type,
  UserEvent,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {ComponentNameType} from 'mesop/mesop/components/component_name/component_name_jspb_proto_pb/mesop/components/component_name/component_name_pb';
import {Channel} from '../../web/src/services/channel';

@Component({
  selector: 'mesop-{component-name}',
  templateUrl: '{component_name}.ng.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  standalone: true,
})
export class ComponentNameComponent {
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  private _config!: ComponentNameType;
  isChecked = false;

  constructor(private readonly channel: Channel) {}

  ngOnChanges() {
    this._config = ComponentNameType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
  }

  config(): ComponentNameType {
    return this._config;
  }

  handleClick(event: any) {
    const userEvent = new UserEvent();
    userEvent.setClick(new Click());
    userEvent.setHandlerId(this.config().getOnClickHandlerId()!);
    this.channel.dispatch(userEvent);
  }
}
