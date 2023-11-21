import { Component, Input } from "@angular/core";
import {
  Click,
  Key,
  Type,
  UserEvent,
} from "optic/protos/ui_ts_proto_pb/protos/ui_pb";
import { ComponentNameType } from "optic/optic/components/component_name/ts_proto_pb/optic/components/component_name/component_name_pb";
import { ChannelService } from "../../../web/src/services/channel_service";

@Component({
  selector: "optic-{component-name}",
  templateUrl: "{component_name}.html",
  standalone: true,
})
export class ComponentNameComponent {
  @Input({ required: true }) type!: Type;
  @Input() key!: Key;
  private _config: ComponentNameType;
  isChecked = false;

  constructor(private readonly channelService: ChannelService) {}

  ngOnChanges() {
    this._config = ComponentNameType.deserializeBinary(
      this.type.getValue() as Uint8Array,
    );
  }

  config(): ComponentNameType {
    return this._config;
  }

  handleClick(event: any) {
    const userEvent = new UserEvent();
    userEvent.setClick(new Click());
    userEvent.setHandlerId(this.config().getOnClickHandlerId()!);
    this.channelService.dispatch(userEvent);
  }
}
