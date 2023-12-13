import {
  ChangeDetectionStrategy,
  Component,
  HostBinding,
  Input,
} from '@angular/core';
import {
  Key,
  Type,
  UserEvent,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {BoxType} from 'mesop/mesop/components/box/box_jspb_proto_pb/mesop/components/box/box_pb';
import {Channel} from '../../web/src/services/channel';

@Component({
  selector: 'mesop-box',
  templateUrl: 'box.ng.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
  standalone: true,
})
export class BoxComponent {
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  private _config!: BoxType;
  isChecked = false;

  constructor(private readonly channel: Channel) {}

  ngOnChanges() {
    this._config = BoxType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
  }

  config(): BoxType {
    return this._config;
  }

  @HostBinding('style') get style(): string {
    return `
    display: block;
    background-color: ${this.config().getBackgroundColor()};`;
  }
}
