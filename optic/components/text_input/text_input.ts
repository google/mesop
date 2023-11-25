import { Component, Input } from "@angular/core";
import {
  Click,
  Key,
  Type,
  UserEvent,
} from "optic/protos/ui_ts_proto_pb/protos/ui_pb";
import { TextInputType } from "optic/optic/components/text_input/text_input_ts_proto_pb/optic/components/text_input/text_input_pb";
import { ChannelService } from "../../../web/src/services/channel_service";

@Component({
  selector: "optic-text-input",
  templateUrl: "text_input.html",
  standalone: true,
})
export class TextInputComponent {
  @Input({ required: true }) type!: Type;
  @Input() key!: Key;
  private _config: TextInputType;
  isChecked = false;

  constructor(private readonly channelService: ChannelService) {}

  ngOnChanges() {
    this._config = TextInputType.deserializeBinary(
      this.type.getValue() as Uint8Array,
    );
  }

  config(): TextInputType {
    return this._config;
  }

  handleClick(event: any) {
    const userEvent = new UserEvent();
    userEvent.setClick(new Click());
    userEvent.setHandlerId(this.config().getOnClickHandlerId()!);
    this.channelService.dispatch(userEvent);
  }
}
