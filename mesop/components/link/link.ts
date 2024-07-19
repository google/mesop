import {ChangeDetectionStrategy, Component, Input} from '@angular/core';
import {
  Key,
  Type,
  UserEvent,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {LinkType} from 'mesop/mesop/components/link/link_jspb_proto_pb/mesop/components/link/link_pb';
import {Channel} from '../../web/src/services/channel';

@Component({
  selector: 'mesop-link',
  templateUrl: 'link.ng.html',
  standalone: true,
})
export class LinkComponent {
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  private _config!: LinkType;
  isChecked = false;

  constructor(private readonly channel: Channel) {}

  ngOnChanges() {
    this._config = LinkType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
  }

  config(): LinkType {
    return this._config;
  }
}
