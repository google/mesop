import {Dialog} from '@angular/cdk/dialog';
import {CommandDialog, DialogData} from './command_dialog';
import {Injectable} from '@angular/core';
import {Channel} from '../../services/channel';
import {SourceCodeLocation} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';

@Injectable({
  providedIn: 'root',
})
export class CommandDialogService {
  constructor(
    private dialog: Dialog,
    private channel: Channel,
  ) {}

  openDialog(location: SourceCodeLocation) {
    this.dialog.open(CommandDialog, {
      minWidth: '300px',
      data: {
        sections: [
          {
            title: 'Components',
            commands: this.channel.getComponentConfigs().map((c) => ({
              componentName: c.getComponentName(),
              location: location,
            })),
          },
        ],
      } as DialogData,
    });
  }
}
