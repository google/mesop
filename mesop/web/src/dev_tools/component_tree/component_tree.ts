import {FlatTreeControl} from '@angular/cdk/tree';
import {
  Component,
  ElementRef,
  Input,
  QueryList,
  ViewChildren,
} from '@angular/core';
import {
  MatTreeFlatDataSource,
  MatTreeFlattener,
  MatTreeModule,
} from '@angular/material/tree';
import {
  ComponentName,
  Component as ComponentProto,
} from 'mesop/mesop/protos/ui_jspb_proto_pb/mesop/protos/ui_pb';
import {CdkTreeModule} from '@angular/cdk/tree';
import {MatIconModule} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import {ComponentObject} from '../services/logger';
import {EditorService} from '../../services/editor_service';
import {CommonModule} from '@angular/common';
import {MatTooltipModule} from '@angular/material/tooltip';
import {Channel} from '../../services/channel';

const ROOT_NODE_TEXT = '<root>';

/** Flat node with expandable and level information */
export interface FlatNode {
  expandable: boolean;
  text: string;
  label: string;
  componentName: ComponentName;
  properties: [string: any];
  level: number;
  proto: ComponentProto;
}

@Component({
  selector: 'mesop-component-tree',
  templateUrl: 'component_tree.ng.html',
  styleUrl: 'component_tree.css',
  standalone: true,
  imports: [
    CdkTreeModule,
    MatTreeModule,
    MatButtonModule,
    MatTooltipModule,
    MatIconModule,
    CommonModule,
  ],
})
export class ComponentTree {
  @Input({required: true}) component!: ComponentObject;
  @Input() selectedComponent!: ComponentProto | undefined;
  @ViewChildren('treeNode') treeNodeRefs!: QueryList<ElementRef>;

  highlightedNodes = new Set<FlatNode>();

  constructor(
    private editorService: EditorService,
    private channel: Channel,
  ) {}

  keys() {
    return Object.keys(this.component);
  }
  private _transformer = (node: DisplayNode, level: number): FlatNode => {
    return {
      expandable: !!node.children && node.children.length > 0,
      text: node.text,
      label: node.label,
      properties: node.properties,
      level: level,
      componentName: node.componentName,
      proto: node.proto,
    };
  };

  treeControl = new FlatTreeControl<FlatNode>(
    (node) => node.level,
    (node) => node.expandable,
  );

  treeFlattener = new MatTreeFlattener(
    this._transformer,
    (node) => node.level,
    (node) => node.expandable,
    (node) => node.children,
  );

  dataSource = new MatTreeFlatDataSource(this.treeControl, this.treeFlattener);

  ngOnChanges() {
    this.dataSource.data = [mapComponentObjectToDisplay(this.component)];

    this.treeControl.dataNodes.forEach((node) => {
      if (node.level < 20) {
        this.treeControl.expand(node);
      }
      if (this.selectedComponent === node.proto) {
        this.treeControl.expand(node);
      }
    });

    const focusedComponent = this.editorService.getFocusedComponent();
    if (focusedComponent) {
      // This is quite hacky, but I need to query the DOM after an event loop
      // otherwise the "selected-node" class attribute hasn't been set yet.
      // If it doesn't work, we don't scroll to the selected node which isn't
      // too bad.
      setTimeout(() => {
        this.treeNodeRefs.forEach((ref) => {
          const element = ref.nativeElement as HTMLElement;
          if (element.querySelector('.selected-node')) {
            element.scrollIntoView({behavior: 'smooth'});
          }
        });
      }, 0);
    }
  }

  hasChild = (_: number, node: FlatNode) => node.expandable;

  selectNode(node: FlatNode): void {
    this.editorService.setFocusedComponent(node.proto);
  }

  isNodeSelected(node: FlatNode): boolean {
    return this.editorService.getFocusedComponent() === node.proto;
  }

  onMouseenter(node: FlatNode): void {
    this.highlightedNodes.add(node);
  }

  onMouseleave(node: FlatNode): void {
    this.highlightedNodes.delete(node);
  }

  isRootNode(node: FlatNode): boolean {
    return node.text === ROOT_NODE_TEXT;
  }
}

export function mapComponentObjectToDisplay(
  object: ComponentObject,
): DisplayNode {
  const node: DisplayNode = {
    componentName: new ComponentName(),
    text: '',
    label: '',
    properties: {} as any,
    children: [],
    proto: object.proto,
  };
  if (object.type) {
    const label = (object.type.value as any)['text'];
    const name = object.type.name.getFnName();
    node.text = `${name}`;
    node.label = label;
    node.properties = object.type as any;
    (node.properties as any).key = object.key;
    node.componentName = object.type.name;
  } else {
    node.text = ROOT_NODE_TEXT;
  }
  if (object.children) {
    node.children = object.children.map((child) =>
      mapComponentObjectToDisplay(child),
    );
  }
  return node;
}

export interface InputNode {
  key: {
    key: string;
  };
  type?: {
    name: string;
    value: [string: any];
  };
  childrenList: InputNode[];
}

export interface DisplayNode {
  text: string;
  label: string;
  componentName: ComponentName;
  properties: [string: any];
  children: DisplayNode[];
  proto: ComponentProto;
}
