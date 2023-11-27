import { Component } from "@angular/core";
import { Logger } from "../services/logger";
import { ObjectTree } from "../object_tree/object_tree";

@Component({
  selector: "optic-components-panel",
  templateUrl: "components_panel.ng.html",
  styleUrl: "components_panel.css",
  standalone: true,
  imports: [ObjectTree],
})
export class ComponentsPanel {}
