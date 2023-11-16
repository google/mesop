import { Component, Input } from "@angular/core";
import * as pb from "optic/protos/ui_ts_proto_pb/protos/ui_pb";

@Component({
  selector: "app-text",
  templateUrl: "text.html",
  standalone: true,
})
export class TextComponent {
  @Input() config!: pb.TextComponent;
}
