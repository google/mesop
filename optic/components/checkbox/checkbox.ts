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
  private _config: CheckboxComponentProto;
  isChecked = false;

  constructor(private readonly channelService: ChannelService) {}

  ngOnChanges() {
    this._config = CheckboxComponentProto.deserializeBinary(
      this.data.getValue() as Uint8Array,
    );
  }

  config(): CheckboxComponentProto {
    return this._config;
  }

  handleCheckboxChange(event: any) {
    console.log("Checkbox is now:", event.target.checked);
    this.isChecked = event.target.checked;
    const userEvent = new pb.UserEvent();
    userEvent.setBool(event.target.checked);
    userEvent.setHandlerId(this.config().getOnUpdateHandlerId()!);
    userEvent.setKey(this.key);
    this.channelService.dispatch(userEvent);
  }
}
