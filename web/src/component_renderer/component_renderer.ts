import { Component, Input } from "@angular/core";
import { CommonModule } from "@angular/common";
import * as pb from "optic/protos/ui_ts_proto_pb/protos/ui_pb";
import { CheckboxComponent } from "../../../optic/components/checkbox/checkbox";
import { ButtonComponent } from "../../../optic/components/button/button";
import { TextComponent } from "../../../optic/components/text/text";
// INSERT COMPONENT TS IMPORTS HERE:
import { ComponentLoader } from "./component_loader";

@Component({
  selector: "component-renderer",
  templateUrl: "component_renderer.html",
  standalone: true,
  imports: [
    // INSERT COMPONENT NG IMPORTS HERE:
    TextComponent,
    CheckboxComponent,
    ButtonComponent,
    CommonModule,
    ComponentLoader,
  ],
})
export class ComponentRenderer {
  @Input() component!: pb.Component;

  trackByFn(index: any, item: pb.Component) {
    const key = item.getKey()?.getKey();
    if (key) {
      return key;
    }
    return index;
  }

  data() {
    return this.component.getType();
  }

  key() {
    return this.component.getKey()!;
  }
}
