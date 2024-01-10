import {MatButtonModule} from '@angular/material/button';
import {Component, Input} from '@angular/core';
import {
  UserEvent,
  Key,
  Type,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {ButtonType} from 'mesop/mesop/components/button/button_jspb_proto_pb/mesop/components/button/button_pb';
import {Channel} from '../../web/src/services/channel';

@Component({
  templateUrl: 'button.ng.html',
  standalone: true,
  imports: [MatButtonModule],
})
export class ButtonComponent {
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  private _config!: ButtonType;

  constructor(private readonly channel: Channel) {}

  ngOnChanges() {
    this._config = ButtonType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
  }

  config(): ButtonType {
    return this._config;
  }

  onClick(event: Event): void {
    const userEvent = new UserEvent();
    userEvent.setHandlerId(this.config().getOnClickHandlerId()!);
    userEvent.setKey(this.key);
    this.channel.dispatch(userEvent);
  }
}
