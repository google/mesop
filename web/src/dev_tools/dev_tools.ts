import { Component } from "@angular/core";
import { LogsPanel } from "./logs_panel/logs_panel";

@Component({
  selector: "optic-dev-tools",
  templateUrl: "dev_tools.html",
  styleUrl: "dev_tools.css",
  standalone: true,
  imports: [LogsPanel],
})
export class DevTools {}
