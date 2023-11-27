import { Component } from "@angular/core";
import { Logger, RenderLogModel } from "../services/logger";
import { ComponentTree } from "../component_tree/component_tree";

@Component({
  selector: "optic-components-panel",
  templateUrl: "components_panel.ng.html",
  styleUrl: "components_panel.css",
  standalone: true,
  imports: [ComponentTree],
})
export class ComponentsPanel {
  constructor(private logger: Logger) {}

  component(): any | undefined {
    const renderLog = this.logger
      .getLogs()
      .slice()
      .reverse()
      .find((log) => log.type === "Render") as RenderLogModel;
    return renderLog?.rootComponent;
  }
}
