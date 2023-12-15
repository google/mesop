import {ChangeDetectionStrategy, Component, Input} from '@angular/core';
import {
  Key,
  Type,
  UserEvent,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {InputType} from 'mesop/mesop/components/input/input_jspb_proto_pb/mesop/components/input/input_pb';
import {Channel} from '../../web/src/services/channel';

@Component({
  selector: 'mesop-input',
  templateUrl: 'input.ng.html',
  standalone: true,
})
export class InputComponent {
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  private _config!: InputType;
  isChecked = false;

  constructor(private readonly channel: Channel) {}

  ngOnChanges() {
    this._config = InputType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
  }

  config(): InputType {
    return this._config;
  }
}
