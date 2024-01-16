import {Dialog} from '@angular/cdk/dialog';
import {CommandDialog, CommandDialogConfig, DialogData} from './command_dialog';
import {Injectable} from '@angular/core';
import {Channel} from '../../services/channel';
import {Component as ComponentProto} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';

@Injectable({
  providedIn: 'root',
})
export class CommandDialogService {
  constructor(
    private dialog: Dialog,
    private channel: Channel,
  ) {}

  async openDialog(
    component: ComponentProto,
    config: CommandDialogConfig,
  ): Promise<void> {
    const dialogRef = this.dialog.open(CommandDialog, {
      minWidth: '300px',
      data: {
        config,
        sections: [
          {
            title: 'Components',
            commands: this.channel.getComponentConfigs().map((c) => ({
              componentName: c.getComponentName(),
              location: component.getSourceCodeLocation(),
            })),
          },
        ],
      } as DialogData,
    });
    await dialogRef.closed.toPromise();
  }
}
