import {Component, Input} from '@angular/core';
import {
  Key,
  Type,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {MicType} from 'mesop/mesop/components/mic/mic_jspb_proto_pb/mesop/components/mic/mic_pb';
import {Channel} from '../../web/src/services/channel';

@Component({
  selector: 'mesop-mic',
  templateUrl: 'mic.ng.html',
  standalone: true,
})
export class MicComponent {
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  private _config!: MicType;
  isChecked = false;

  constructor(private readonly channel: Channel) {}

  ngOnChanges() {
    this._config = MicType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
  }

  config(): MicType {
    return this._config;
  }
}
