import { Component, Input } from "@angular/core";
import {
  Click,
  Key,
  Type,
  UserEvent,
} from "optic/protos/ui_ts_proto_pb/protos/ui_pb";
import { ButtonType } from "optic/optic/components/button/button_ts_proto_pb/optic/components/button/button_pb";
import { ChannelService } from "../../../web/src/services/channel_service";
import { MatButtonModule } from "@angular/material/button";

@Component({
  selector: "optic-button",
  templateUrl: "button.html",
  standalone: true,
  imports: [MatButtonModule],
})
export class ButtonComponent {
  @Input({ required: true }) type!: Type;
  @Input() key!: Key;
  private _config: ButtonType;
  isChecked = false;

  constructor(private readonly channelService: ChannelService) {}

  ngOnChanges() {
    this._config = ButtonType.deserializeBinary(
      this.type.getValue() as Uint8Array,
    );
  }

  config(): ButtonType {
    return this._config;
  }

  handleClick(event: any) {
    const userEvent = new UserEvent();
    userEvent.setClick(new Click());
    userEvent.setHandlerId(this.config().getOnClickHandlerId()!);
    this.channelService.dispatch(userEvent);
  }
}
