import { Component, Input } from "@angular/core";
import { TextComponent } from "../components/text/text";
import { CommonModule } from "@angular/common";
import * as pb from "optic/protos/ui_ts_proto_pb/protos/ui_pb";
import { CheckboxComponent } from "../components/checkbox/checkbox";
import { ButtonComponent } from "../components/button/button";
import { ComponentLoader } from "./component_loader";

@Component({
  selector: "component-renderer",
  templateUrl: "component_renderer.html",
  standalone: true,
  imports: [
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
    return this.component.getData();
  }

  key() {
    return this.component.getKey()!;
  }
}
