import {MatSelectModule, MatSelectChange} from '@angular/material/select';
import {Component, Input} from '@angular/core';
import {
  UserEvent,
  Key,
  Type,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {SelectType} from 'mesop/mesop/components/select/select_jspb_proto_pb/mesop/components/select/select_pb';
import {Channel} from '../../web/src/services/channel';

@Component({
  templateUrl: 'select.ng.html',
  standalone: true,
  imports: [MatSelectModule],
})
export class SelectComponent {
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  private _config!: SelectType;

  constructor(private readonly channel: Channel) {}

  ngOnChanges() {
    this._config = SelectType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
  }

  config(): SelectType {
    return this._config;
  }

  onSelectOpenedChangeEvent(event: boolean): void {
    const userEvent = new UserEvent();
    userEvent.setBoolValue(event);
    userEvent.setHandlerId(
      this.config().getOnSelectOpenedChangeEventHandlerId()!,
    );
    userEvent.setKey(this.key);
    this.channel.dispatch(userEvent);
  }

  onSelectSelectionChangeEvent(event: MatSelectChange): void {
    const userEvent = new UserEvent();

    userEvent.setHandlerId(
      this.config().getOnSelectSelectionChangeEventHandlerId()!,
    );
    userEvent.setStringValue(event.value);
    userEvent.setKey(this.key);
    this.channel.dispatch(userEvent);
  }
}
