import {MatTableModule} from '@angular/material/table';
import {Component, Input} from '@angular/core';
import {TableType} from 'mesop/mesop/components/table/table_jspb_proto_pb/mesop/components/table/table_pb';
import {Channel} from '../../web/src/services/channel';
import {
  Key,
  Type,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';

@Component({
  selector: 'mesop-table',
  templateUrl: 'table.ng.html',
  standalone: true,
  imports: [MatTableModule],
})
export class TableComponent {
  @Input({required: true}) type!: Type;
  @Input() key!: Key;
  private _config!: TableType;
  constructor(private readonly channel: Channel) {}

  ngOnChanges() {
    this._config = TableType.deserializeBinary(
      this.type.getValue() as unknown as Uint8Array,
    );
  }

  config(): TableType {
    return this._config;
  }
}
