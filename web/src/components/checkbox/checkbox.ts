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
  isChecked = false;

  constructor(private readonly channelService: ChannelService) {}

  handleCheckboxChange(event: any) {
    console.log("Checkbox is now:", event.target.checked);
    this.isChecked = event.target.checked;
    const request = new pb.UiRequest();
    const userAction = new pb.UserAction();
    userAction.setBool(event.target.checked);
    request.setUserAction(userAction);
    this.channelService.dispatch(request);
  }
}
