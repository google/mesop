import {MatProgressSpinnerModule} from '@angular/material/progress-spinner';
import {Component, Input} from '@angular/core';
import {
  UserEvent,
  Key,
  Type,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {ProgressSpinnerType} from 'mesop/mesop/components/progress_spinner/progress_spinner_jspb_proto_pb/mesop/components/progress_spinner/progress_spinner_pb';
import {Channel} from '../../web/src/services/channel';

@Component({
  templateUrl: 'progress_spinner.ng.html',
  standalone: true,
  imports: [MatProgressSpinnerModule],
})
export class ProgressSpinnerComponent {
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  private _config!: ProgressSpinnerType;

  constructor(private readonly channel: Channel) {}

  ngOnChanges() {
    this._config = ProgressSpinnerType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
  }

  config(): ProgressSpinnerType {
    return this._config;
  }

  getMode(): 'determinate' | 'indeterminate' {
    return this.config().getMode() as 'determinate' | 'indeterminate';
  }
}
