import {MatRadioModule, MatRadioChange} from '@angular/material/radio';
import {Component, Input} from '@angular/core';
import {
  UserEvent,
  Key,
  Type,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {RadioType} from 'mesop/mesop/components/radio/radio_jspb_proto_pb/mesop/components/radio/radio_pb';
import {Channel} from '../../web/src/services/channel';

@Component({
  templateUrl: 'radio.ng.html',
  standalone: true,
  imports: [MatRadioModule],
})
export class RadioComponent {
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  private _config!: RadioType;

  constructor(private readonly channel: Channel) {}

  ngOnChanges() {
    this._config = RadioType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
  }

  config(): RadioType {
    return this._config;
  }

  getColor(): 'primary' | 'accent' | 'warn' {
    return this.config().getColor() as 'primary' | 'accent' | 'warn';
  }

  getLabelPosition(): 'before' | 'after' {
    return this.config().getLabelPosition() as 'before' | 'after';
  }

  onRadioChangeEvent(event: MatRadioChange): void {
    const userEvent = new UserEvent();
    userEvent.setHandlerId(this.config().getOnRadioChangeEventHandlerId()!);
    userEvent.setStringValue(event.value);
    userEvent.setKey(this.key);
    this.channel.dispatch(userEvent);
  }
}
