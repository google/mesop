import { Component } from "@angular/core";
import { LoggerService } from "../../services/logger_service";
import { ObjectTree } from "../object_tree/object_tree";

@Component({
  selector: "optic-logs-panel",
  templateUrl: "logs_panel.html",
  styleUrl: "logs_panel.css",
  standalone: true,
  imports: [ObjectTree],
})
export class LogsPanel {
  constructor(private loggerService: LoggerService) {
    this.loggerService.setOnLog(this.onLog);
  }

  getLogs() {
    return this.loggerService.getLogs();
  }
  onLog = () => {
    console.log("getLogs", this.getLogs());
  };
}
