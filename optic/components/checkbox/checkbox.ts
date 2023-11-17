import { Component, Input } from "@angular/core";
import * as pb from "optic/protos/ui_ts_proto_pb/protos/ui_pb";
import { CheckboxComponent as CheckboxComponentProto } from "optic/optic/components/checkbox/checkbox_ts_proto_pb/optic/components/checkbox/checkbox_pb";
import { ChannelService } from "../../../web/src/services/channel_service";

@Component({
  selector: "app-checkbox",
  templateUrl: "checkbox.html",
  standalone: true,
})
export class CheckboxComponent {
  @Input() data!: pb.Type;
  @Input() key!: pb.Key;
  isChecked = false;

  constructor(private readonly channelService: ChannelService) {}

  getConfig(): CheckboxComponentProto {
    return CheckboxComponentProto.deserializeBinary(
      this.data.getValue() as Uint8Array,
    );
  }

  handleCheckboxChange(event: any) {
    console.log("Checkbox is now:", event.target.checked);
    this.isChecked = event.target.checked;
    const userAction = new pb.UserAction();
    userAction.setBool(event.target.checked);
    userAction.setHandlerId(this.getConfig().getOnUpdateHandlerId()!);
    userAction.setKey(this.key);
    this.channelService.dispatch(userAction);
  }
}
