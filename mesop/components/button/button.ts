import {ChangeDetectionStrategy, Component, Input} from '@angular/core';
import {
  Key,
  Type,
  UserEvent,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {ButtonType} from 'mesop/mesop/components/button/button_jspb_proto_pb/mesop/components/button/button_pb';
import {Channel} from '../../web/src/services/channel';
import {MatButtonModule} from '@angular/material/button';

@Component({
  selector: 'mesop-button',
  templateUrl: 'button.ng.html',
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  imports: [MatButtonModule],
})
export class ButtonComponent {
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  private _config!: ButtonType;
  isChecked = false;

  constructor(private readonly channel: Channel) {}

  ngOnChanges() {
    this._config = ButtonType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
  }

  config(): ButtonType {
    return this._config;
  }

  handleClick(event: any) {
    const userEvent = new UserEvent();
    userEvent.setHandlerId(this.config().getOnClickHandlerId()!);
    this.channel.dispatch(userEvent);
  }
}
