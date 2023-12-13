import {ChangeDetectionStrategy, Component, Input} from '@angular/core';
import {
  Key,
  Type,
  UserEvent,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {CheckboxType} from 'mesop/mesop/components/checkbox/checkbox_jspb_proto_pb/mesop/components/checkbox/checkbox_pb';
import {Channel} from '../../web/src/services/channel';

@Component({
  selector: 'mesop-checkbox',
  templateUrl: 'checkbox.ng.html',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class CheckboxComponent {
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  private _config!: CheckboxType;
  isChecked = false;

  constructor(private readonly channel: Channel) {}

  ngOnChanges() {
    this._config = CheckboxType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
  }

  config(): CheckboxType {
    return this._config;
  }

  handleCheckboxChange(event: any) {
    console.log('Checkbox is now:', event.target.checked);
    this.isChecked = event.target.checked;
    const userEvent = new UserEvent();
    userEvent.setBool(event.target.checked);
    userEvent.setHandlerId(this.config().getOnUpdateHandlerId()!);
    userEvent.setKey(this.key);
    this.channel.dispatch(userEvent);
  }
}
