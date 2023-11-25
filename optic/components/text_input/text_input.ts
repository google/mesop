import { Component, Input } from "@angular/core";
import {
  InputChange,
  Key,
  Type,
  UserEvent,
} from "optic/protos/ui_ts_proto_pb/protos/ui_pb";
import { TextInputType } from "optic/optic/components/text_input/text_input_ts_proto_pb/optic/components/text_input/text_input_pb";
import { ChannelService } from "../../../web/src/services/channel_service";
import { MatFormFieldModule } from "@angular/material/form-field";
import { MatInputModule } from "@angular/material/input";
import { FormsModule } from "@angular/forms";
import { ObserversModule } from "@angular/cdk/observers";

@Component({
  selector: "optic-text-input",
  templateUrl: "text_input.html",
  standalone: true,
  imports: [MatFormFieldModule, MatInputModule, FormsModule, ObserversModule],
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

  onChange(event: Event) {
    const userEvent = new UserEvent();
    const inputChange = new InputChange();
    inputChange.setValue((event.target as HTMLInputElement).value);
    userEvent.setChange(inputChange);
    userEvent.setHandlerId(this.config().getOnChangeHandlerId()!);
    this.channelService.dispatch(userEvent);
  }
}
