import { Component, Input } from "@angular/core";
import * as pb from "optic/protos/ui_ts_proto_pb/protos/ui_pb";
import { ChannelService } from "../../services/channel_service";

@Component({
  selector: "app-checkbox",
  templateUrl: "checkbox.html",
  standalone: true,
})
export class CheckboxComponent {
  @Input() config!: pb.CheckboxComponent;
  @Input() key!: pb.Key;
  isChecked = false;

  constructor(private readonly channelService: ChannelService) {}

  handleCheckboxChange(event: any) {
    console.log("Checkbox is now:", event.target.checked);
    this.isChecked = event.target.checked;
    const userAction = new pb.UserAction();
    userAction.setBool(event.target.checked);
    userAction.setActionType(this.config.getOnUpdate()!);
    userAction.setKey(this.key);
    this.channelService.dispatch(userAction);
  }
}
