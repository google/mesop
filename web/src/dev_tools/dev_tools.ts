import { Component } from "@angular/core";
import { LogsPanel } from "./logs_panel/logs_panel";
import { ComponentsPanel } from "./components_panel/components_panel";
import { CommonModule } from "@angular/common";
import { DebugService, Panel } from "./services/debug_service";

@Component({
  selector: "optic-dev-tools",
  templateUrl: "dev_tools.ng.html",
  styleUrl: "dev_tools.css",
  standalone: true,
  imports: [LogsPanel, ComponentsPanel, CommonModule],
})
export class DevTools {
  Panel = Panel; // Make it accessible by template.

  get selectedPanel(): Panel {
    return this.debugService.getCurrentDevToolsPanel();
  }

  constructor(private debugService: DebugService) {}

  selectComponentsPanel() {
    this.debugService.setCurrentDevToolsPanel(Panel.Components);
  }

  selectLogsPanel() {
    this.debugService.setCurrentDevToolsPanel(Panel.Logs);
  }
}
