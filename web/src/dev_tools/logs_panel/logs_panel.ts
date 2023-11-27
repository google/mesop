import { Component } from "@angular/core";
import { LoggerService } from "../../services/logger_service";

@Component({
  selector: "optic-logs-panel",
  templateUrl: "logs_panel.html",
  styleUrl: "logs_panel.css",
  standalone: true,
})
export class LogsPanel {
  constructor(private loggerService: LoggerService) {
    this.loggerService.setOnLog(this.onLog);
  }

  getLogs() {
    return this.loggerService.getLogs().map((l) => JSON.stringify(l, null, 2));
  }
  onLog = () => {
    console.log("getLogs", this.getLogs());
  };
}
