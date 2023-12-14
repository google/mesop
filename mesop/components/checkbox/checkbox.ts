import {ChangeDetectionStrategy, Component, Input} from '@angular/core';
import {
  Key,
  Type,
  UserEvent,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {CheckboxType} from 'mesop/mesop/components/checkbox/checkbox_jspb_proto_pb/mesop/components/checkbox/checkbox_pb';
import {Channel} from '../../web/src/services/channel';
import {MatCheckboxChange, MatCheckboxModule} from '@angular/material/checkbox';

@Component({
  selector: 'mesop-checkbox',
  templateUrl: 'checkbox.ng.html',
  standalone: true,
  imports: [MatCheckboxModule],
})
export class CheckboxComponent {
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  private _config!: CheckboxType;
  value = false;

  constructor(private readonly channel: Channel) {}

  ngOnChanges() {
    this._config = CheckboxType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
    this.value = this._config.getDefaultValue();
  }

  config(): CheckboxType {
    return this._config;
  }

  handleCheckboxChange(event: MatCheckboxChange) {
    const userEvent = new UserEvent();
    userEvent.setBool(event.checked);
    userEvent.setHandlerId(this.config().getOnUpdateHandlerId()!);
    userEvent.setKey(this.key);
    this.channel.dispatch(userEvent);
  }
}
