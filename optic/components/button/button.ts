import { Component, Input } from "@angular/core";
import * as pb from "optic/protos/ui_ts_proto_pb/protos/ui_pb";
import { ChannelService } from "../../../web/src/services/channel_service";
import { MatButtonModule } from "@angular/material/button";

@Component({
  selector: "app-button",
  templateUrl: "button.html",
  standalone: true,
  imports: [MatButtonModule],
})
export class ButtonComponent {
  @Input() config!: pb.ButtonComponent;
  isChecked = false;

  constructor(private readonly channelService: ChannelService) {}

  handleClick(event: any) {
    const userAction = new pb.UserAction();
    userAction.setClick(new pb.Click());
    userAction.setHandlerId(this.config.getOnClickHandlerId()!);
    this.channelService.dispatch(userAction);
  }
}
