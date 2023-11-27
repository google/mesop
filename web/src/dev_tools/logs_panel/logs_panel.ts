import { Component } from "@angular/core";
import { Logger } from "../../services/logger";
import { ObjectTree } from "../object_tree/object_tree";

@Component({
  selector: "optic-logs-panel",
  templateUrl: "logs_panel.html",
  styleUrl: "logs_panel.css",
  standalone: true,
  imports: [ObjectTree],
})
export class LogsPanel {
  constructor(private logger: Logger) {
    this.logger.setOnLog(this.onLog);
  }

  getLogs() {
    return this.logger.getLogs();
  }
  onLog = () => {
    console.log("getLogs", this.getLogs());
  };
}
