import {Component, Input} from '@angular/core';
import {MatIconModule} from '@angular/material/icon';
import {ComponentConfig} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';

@Component({
  selector: 'mesop-component-library',
  templateUrl: 'component_library.ng.html',
  styleUrl: 'component_library.css',
  standalone: true,
  imports: [MatIconModule],
})
export class ComponentLibrary {
  @Input()
  componentConfigs!: ComponentConfig[];
}
