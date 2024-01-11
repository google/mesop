import {DIALOG_DATA} from '@angular/cdk/dialog';
import {Component, Inject} from '@angular/core';
import {MatDividerModule} from '@angular/material/divider';
import {
  EditorEvent,
  EditorNewComponent,
  SourceCodeLocation,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {Channel} from '../../services/channel';

export interface DialogData {
  sections: Section[];
}

interface Section {
  title: string;
  commands: Command[];
}

interface Command {
  componentName: string;
  location: SourceCodeLocation;
}

@Component({
  selector: 'mesop-command-dialog',
  templateUrl: 'command_dialog.ng.html',
  styleUrl: 'command_dialog.css',
  standalone: true,
  imports: [MatDividerModule],
})
export class CommandDialog {
  constructor(
    @Inject(DIALOG_DATA) public data: DialogData,
    private channel: Channel,
  ) {}

  createComponent(location: SourceCodeLocation, componentName: string) {
    const editorEvent = new EditorEvent();
    const newComponent = new EditorNewComponent();
    newComponent.setComponentName(componentName);
    newComponent.setSourceCodeLocation(location);
    editorEvent.setNewComponent(newComponent);
    this.channel.dispatchEditorEvent(editorEvent);
  }
}
