import { Component, Input } from "@angular/core";
import * as pb from "optic/protos/ui_ts_proto_pb/protos/ui_pb";
import { ButtonComponent as ButtonComponentProto } from "optic/optic/components/button/button_ts_proto_pb/optic/components/button/button_pb";
import { ChannelService } from "../../../web/src/services/channel_service";
import { MatButtonModule } from "@angular/material/button";

@Component({
  selector: "app-button",
  templateUrl: "button.html",
  standalone: true,
  imports: [MatButtonModule],
})
export class ButtonComponent {
  @Input() data!: pb.Type;
  private _config: ButtonComponentProto;
  isChecked = false;

  constructor(private readonly channelService: ChannelService) {}

  ngOnChanges() {
    this._config = ButtonComponentProto.deserializeBinary(
      this.data.getValue() as Uint8Array,
    );
  }

  config(): ButtonComponentProto {
    return this._config;
  }

  handleClick(event: any) {
    const userEvent = new pb.UserEvent();
    userEvent.setClick(new pb.Click());
    userEvent.setHandlerId(this.config().getOnClickHandlerId()!);
    this.channelService.dispatch(userEvent);
  }
}
