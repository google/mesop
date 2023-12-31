import {Component} from '@angular/core';
import {ComponentObject, Logger, RenderLogModel} from '../services/logger';
import {ComponentTree, FlatNode} from '../component_tree/component_tree';
import {ObjectTree} from '../object_tree/object_tree';

@Component({
  selector: 'mesop-components-panel',
  templateUrl: 'components_panel.ng.html',
  styleUrl: 'components_panel.css',
  standalone: true,
  imports: [ComponentTree, ObjectTree],
})
export class ComponentsPanel {
  selectedNode!: FlatNode;
  constructor(private logger: Logger) {}

  component(): ComponentObject {
    const renderLog = this.logger
      .getLogs()
      .slice()
      .reverse()
      .find((log) => log.type === 'Render') as RenderLogModel;
    return renderLog?.rootComponent as ComponentObject;
  }

  onNodeSelected(node: FlatNode): void {
    this.selectedNode = node;
  }
}
