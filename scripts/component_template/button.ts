import { Component, Input } from "@angular/core";
import * as pb from "optic/protos/ui_ts_proto_pb/protos/ui_pb";
import { ChannelService } from "../../../web/src/services/channel_service";

@Component({
  selector: "app-{component-name}",
  templateUrl: "{component_name}.html",
  standalone: true,
})
export class ComponentNameComponent {
  @Input() config!: pb.ButtonComponent;

  constructor(private readonly channelService: ChannelService) {}

  handleClick(event: any) {
    const userAction = new pb.UserAction();
    userAction.setClick(new pb.Click());
    userAction.setActionType(this.config.getOnClick()!);
    this.channelService.dispatch(userAction);
  }
}
