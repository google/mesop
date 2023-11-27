import { Component, ViewChild } from "@angular/core";
import { LogModel, Logger } from "../services/logger";
import { ObjectTree } from "../object_tree/object_tree";
import {
  CdkVirtualScrollViewport,
  ScrollingModule,
} from "@angular/cdk/scrolling";
import { CollectionViewer, DataSource } from "@angular/cdk/collections";
import { Observable } from "rxjs";

@Component({
  selector: "optic-logs-panel",
  templateUrl: "logs_panel.ng.html",
  styleUrl: "logs_panel.css",
  standalone: true,
  imports: [ScrollingModule, ObjectTree],
})
export class LogsPanel {
  @ViewChild("virtualScroll", { static: true })
  virtualScrollViewport: CdkVirtualScrollViewport;

  logDataSource: LogDataSource;

  constructor(private logger: Logger) {
    this.logger.setOnLog(this.onLog);
    this.logDataSource = new LogDataSource(this.logger);
  }

  getLogs() {
    return this.logger.getLogs();
  }

  onLog = () => {
    // Scroll to bottom. In the future, make this configurable.
    setTimeout(() => {
      this.virtualScrollViewport.scrollTo({
        bottom: 0,
        behavior: "auto",
      });
    }, 50);
  };

  trackByFn(index: number, item: LogModel) {
    return index;
  }
}

export class LogDataSource extends DataSource<LogModel> {
  constructor(private logger: Logger) {
    super();
  }

  connect(collectionViewer: CollectionViewer): Observable<LogModel[]> {
    return this.logger.getLogObservable();
  }

  disconnect(collectionViewer: CollectionViewer): void {
    // Any cleanup needed when the data source is disconnected
  }
}
