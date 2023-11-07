import { ChangeDetectorRef, Component, NgZone } from "@angular/core";
import { UiResponse } from "optic/protos/ui_ts_proto_pb/protos/ui_pb";

// TODO: set this as environmental variable
const DEV_SERVER_URL = "http://127.0.0.1:8080/ui";

@Component({
  selector: "app",
  templateUrl: "app.html",
  standalone: true,
})
export class App {
  val = 1;
  data: any[] = [];

  constructor(
    private zone: NgZone,
    private cd: ChangeDetectorRef
  ) {}

  ngOnInit() {
    const uir = new UiResponse();
    uir.setId(1);

    var eventSource = new EventSource(DEV_SERVER_URL);
    eventSource.onmessage = (e) => {
      // Looks like Angular has a bug where it's not intercepting EventSource onmessage.
      this.zone.run(() => {
        console.log(e.data);
        // Need a new array reference so Angular's dirty checker works.
        this.data = this.data.concat(JSON.stringify(e.data));
      });
    };
  }

  incrementCount() {
    this.val++;
  }
}
