import {Component, Input} from '@angular/core';
import {Warning} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';

import {CommonModule} from '@angular/common';

@Component({
  selector: 'mesop-warning-box',
  templateUrl: 'warning_box.ng.html',
  styleUrl: 'warning_box.css',
  standalone: true,
  imports: [CommonModule],
})
export class WarningBox {
  @Input({required: true}) warnings!: Warning[];
}
