import { Component, Input } from "@angular/core";
import { TextComponent } from "../components/text/text";
import { CommonModule } from "@angular/common";
import * as pb from "optic/protos/ui_ts_proto_pb/protos/ui_pb";

@Component({
  selector: "component-renderer",
  templateUrl: "component_renderer.html",
  standalone: true,
  imports: [TextComponent, CommonModule],
})
export class ComponentRenderer {
  @Input() component!: pb.Component;

  trackByFn(index: any, item: any) {
    // TODO: use item id.
    return index;
  }
}
