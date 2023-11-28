import { Component } from "@angular/core";
import { LogsPanel } from "./logs_panel/logs_panel";
import { ComponentsPanel } from "./components_panel/components_panel";
import { CommonModule } from "@angular/common";

enum Panel {
  Components,
  Logs,
}

@Component({
  selector: "optic-dev-tools",
  templateUrl: "dev_tools.ng.html",
  styleUrl: "dev_tools.css",
  standalone: true,
  imports: [LogsPanel, ComponentsPanel, CommonModule],
})
export class DevTools {
  Panel = Panel; // Make it accessible by template.
  selectedPanel = Panel.Components; // TODO: store in local storage

  selectComponentsPanel() {
    this.selectedPanel = Panel.Components;
  }

  selectLogsPanel() {
    this.selectedPanel = Panel.Logs;
  }
}
