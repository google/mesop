import {DIALOG_DATA, DialogRef} from '@angular/cdk/dialog';
import {Component, Inject} from '@angular/core';
import {MatDividerModule} from '@angular/material/divider';
import {
  ComponentName,
  EditorEvent,
  EditorNewComponent,
  SourceCodeLocation,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {Channel} from '../../services/channel';

export interface DialogData {
  sections: Section[];
  config: CommandDialogConfig;
}

export interface CommandDialogConfig {
  newComponentMode: 'addChild' | 'appendSibling';
}

interface Section {
  title: string;
  commands: Command[];
}

interface Command {
  componentName: ComponentName;
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
  filter = '';
  constructor(
    private dialogRef: DialogRef,
    @Inject(DIALOG_DATA) private data: DialogData,
    private channel: Channel,
  ) {}

  getData() {
    return {
      sections: this.data.sections.map((s) => ({
        title: s.title,
        commands: s.commands.filter((c) =>
          c.componentName.getFnName()!.includes(this.filter),
        ),
      })),
    };
  }

  onInputChange(event: Event) {
    this.filter = (event.target as HTMLInputElement).value;
  }

  createComponent(location: SourceCodeLocation, componentName: ComponentName) {
    const editorEvent = new EditorEvent();
    const newComponent = new EditorNewComponent();
    newComponent.setComponentName(componentName);
    newComponent.setSourceCodeLocation(location);
    if (this.data.config.newComponentMode === 'addChild') {
      newComponent.setMode(EditorNewComponent.Mode.MODE_CHILD);
    }
    if (this.data.config.newComponentMode === 'appendSibling') {
      newComponent.setMode(EditorNewComponent.Mode.MODE_APPEND_SIBLING);
    }
    editorEvent.setNewComponent(newComponent);
    this.channel.dispatchEditorEvent(editorEvent);
    this.dialogRef.close();
  }
}
