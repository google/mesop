import {MatCheckboxModule, MatCheckboxChange} from '@angular/material/checkbox';
import {Component, Input} from '@angular/core';
import {
  UserEvent,
  Key,
  Type,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {CheckboxType} from 'mesop/mesop/components/checkbox/checkbox_jspb_proto_pb/mesop/components/checkbox/checkbox_pb';
import {Channel} from '../../web/src/services/channel';

@Component({
  // selector: 'mesop-{component-name}',
  templateUrl: 'checkbox.ng.html',
  standalone: true,
  imports: [MatCheckboxModule],
})
export class CheckboxComponent {
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  private _config!: CheckboxType;
  value!: boolean;

  constructor(private readonly channel: Channel) {}

  ngOnChanges() {
    this._config = CheckboxType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
    this.value = this._config.getValue();
  }

  config(): CheckboxType {
    return this._config;
  }

  onMatCheckboxChange(event: MatCheckboxChange): void {
    const userEvent = new UserEvent();
    userEvent.setBool(event.checked);
    userEvent.setHandlerId(this.config().getOnMatCheckboxChangeHandlerId());
    userEvent.setKey(this.key);
    this.channel.dispatch(userEvent);
  }
}
