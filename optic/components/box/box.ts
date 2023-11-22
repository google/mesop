import { Component, Input } from "@angular/core";
import {
  Click,
  Key,
  Type,
  UserEvent,
} from "optic/protos/ui_ts_proto_pb/protos/ui_pb";
import { BoxType } from "optic/optic/components/box/ts_proto_pb/optic/components/box/box_pb";
import { ChannelService } from "../../../web/src/services/channel_service";

@Component({
  selector: "optic-box",
  templateUrl: "box.html",
  standalone: true,
})
export class BoxComponent {
  @Input({ required: true }) type!: Type;
  @Input() key!: Key;
  private _config: BoxType;
  isChecked = false;

  constructor(private readonly channelService: ChannelService) {}

  ngOnChanges() {
    this._config = BoxType.deserializeBinary(
      this.type.getValue() as Uint8Array,
    );
  }

  config(): BoxType {
    return this._config;
  }

  handleClick(event: any) {
    const userEvent = new UserEvent();
    userEvent.setClick(new Click());
    userEvent.setHandlerId(this.config().getOnClickHandlerId()!);
    this.channelService.dispatch(userEvent);
  }
}
