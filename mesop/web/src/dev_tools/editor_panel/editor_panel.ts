import {Component} from '@angular/core';
import {EditorService} from '../../services/editor_service';
import {mapComponentToObject} from '../services/logger';
import {mapComponentObjectToDisplay} from '../component_tree/component_tree';
import {ObjectTree} from '../object_tree/object_tree';

@Component({
  selector: 'mesop-editor-panel',
  templateUrl: 'editor_panel.ng.html',
  styleUrl: 'editor_panel.css',
  standalone: true,
  imports: [ObjectTree],
})
export class EditorPanel {
  constructor(private editorService: EditorService) {}

  getFocusedComponent() {
    const obj = mapComponentToObject(this.editorService.getFocusedComponent());
    const display = mapComponentObjectToDisplay(obj);
    return display;
  }
}
