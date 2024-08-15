import {
  Component,
  ElementRef,
  Input,
  Renderer2,
  ViewChild,
} from '@angular/core';
import {EditorService} from '../../services/editor_service';
import {ComponentObject, Logger, RenderLogModel} from '../services/logger';
import {ComponentTree, FlatNode} from '../component_tree/component_tree';
import {ObjectTree} from '../object_tree/object_tree';
import {
  FieldType,
  ComponentConfig,
  EditorField,
  ComponentName,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {MatDialogModule, MatDialog} from '@angular/material/dialog';
import {MatDividerModule} from '@angular/material/divider';
import {EditorFields} from './editor_fields/editor_fields';
import {MatIconModule} from '@angular/material/icon';
import {Channel} from '../../services/channel';
import {CommonModule} from '@angular/common';
import {MatButtonModule} from '@angular/material/button';
import {isComponentNameEquals} from '../../utils/proto';

@Component({
  selector: 'mesop-editor-panel',
  templateUrl: 'editor_panel.ng.html',
  styleUrl: 'editor_panel.css',
  standalone: true,
  imports: [
    CommonModule,
    ObjectTree,
    EditorFields,
    MatDividerModule,
    ComponentTree,
    MatIconModule,
    MatDialogModule,
  ],
})
export class EditorPanel {
  @Input()
  componentConfigs!: readonly ComponentConfig[];

  FieldTypeCase = FieldType.TypeCase;
  selectedNode!: FlatNode;

  @ViewChild('dragHandle', {read: ElementRef}) dragHandle!: ElementRef;
  private isDragging = false;
  @ViewChild('topPanel', {read: ElementRef}) topPanel!: ElementRef;
  @ViewChild('bottomPanel', {read: ElementRef}) bottomPanel!: ElementRef;

  constructor(
    private logger: Logger,
    private editorService: EditorService,
    private channel: Channel,
    private renderer: Renderer2,
    private dialog: MatDialog,
  ) {}

  ngAfterViewInit() {
    this.dragHandle.nativeElement.addEventListener('mousedown', () => {
      this.isDragging = true;
    });

    this.renderer.listen(document, 'mousemove', (event) => {
      if (!this.isDragging) return;

      const newHeight = window.innerHeight - event.clientY;
      this.topPanel.nativeElement.style.marginBottom = `${newHeight}px`;
      this.bottomPanel.nativeElement.style.height = `${newHeight}px`;
    });

    this.renderer.listen(document, 'mouseup', (event) => {
      this.isDragging = false;
    });
  }

  hasFocusedComponent(): boolean {
    return Boolean(this.editorService.getFocusedComponent());
  }

  getFocusedComponent() {
    return this.editorService.getFocusedComponent();
  }

  getFocusedComponentName(): string {
    const type = this.getFocusedComponent()?.getType();
    if (!type) {
      return '<root>';
    }
    return type.getName()?.getFnName() ?? '<unknown>';
  }

  getComponentConfig() {
    return this.componentConfigs.find((config) =>
      isComponentNameEquals(
        config.getComponentName()!,
        this.editorService.getFocusedComponent()!.getType()?.getName()!,
      ),
    );
  }

  getFields(): readonly EditorField[] {
    return this.getComponentConfig()?.getFieldsList() ?? [];
  }

  component(): ComponentObject {
    const renderLog = this.logger
      .getLogs()
      .slice()
      .reverse()
      .find((log) => log.type === 'Render') as RenderLogModel;
    return renderLog?.rootComponent as ComponentObject;
  }

  showDocLink(): boolean {
    return Boolean(
      this.getFocusedComponent()?.getType()?.getName()?.getCoreModule(),
    );
  }

  getComponentName(): ComponentName | undefined {
    return this.getFocusedComponent()?.getType()?.getName();
  }

  getDocLink(): string {
    const componentName = this.getComponentName()?.getFnName() ?? '';
    return `https://google.github.io/mesop/components/${componentName}/`;
  }
}

@Component({
  template: `<h1 mat-dialog-title>Confirm deleting component</h1>
    <div mat-dialog-actions>
      <button mat-button [mat-dialog-close]="false">Cancel</button>
      <button mat-button [mat-dialog-close]="true" cdkFocusInitial>Ok</button>
    </div>`,
  imports: [MatButtonModule, MatDialogModule],
  standalone: true,
})
class DeleteConfirmationDialog {}
