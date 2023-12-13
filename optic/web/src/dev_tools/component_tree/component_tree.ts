import {FlatTreeControl} from '@angular/cdk/tree';
import {Component, EventEmitter, Input, Output} from '@angular/core';
import {
  MatTreeFlatDataSource,
  MatTreeFlattener,
  MatTreeModule,
} from '@angular/material/tree';
import {CdkTreeModule} from '@angular/cdk/tree';
import {MatIconModule} from '@angular/material/icon';
import {MatButtonModule} from '@angular/material/button';
import {ComponentObject} from '../services/logger';

/** Flat node with expandable and level information */
export interface ExampleFlatNode {
  expandable: boolean;
  text: string;
  componentName: string;
  properties: [string: any];
  level: number;
}

@Component({
  selector: 'optic-component-tree',
  templateUrl: 'component_tree.ng.html',
  styleUrl: 'component_tree.css',
  standalone: true,
  imports: [CdkTreeModule, MatTreeModule, MatButtonModule, MatIconModule],
})
export class ComponentTree {
  @Input({required: true}) component!: ComponentObject;
  @Output() nodeSelected = new EventEmitter<ExampleFlatNode>();

  keys() {
    return Object.keys(this.component);
  }
  private _transformer = (node: DisplayNode, level: number) => {
    return {
      expandable: !!node.children && node.children.length > 0,
      text: node.text,
      properties: node.properties,
      level: level,
      componentName: node.componentName,
    };
  };

  treeControl = new FlatTreeControl<ExampleFlatNode>(
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
    this.dataSource.data = [mapObject(this.component)];

    this.treeControl.dataNodes.forEach((node) => {
      if (node.level < 5) {
        this.treeControl.expand(node);
      }
    });
  }

  hasChild = (_: number, node: ExampleFlatNode) => node.expandable;

  selectNode(node: ExampleFlatNode): void {
    this.nodeSelected.emit(node);
  }
}

function mapObject(object: ComponentObject): DisplayNode {
  const node: DisplayNode = {
    componentName: '<undefined>',
    text: '',
    properties: {} as any,
    children: [],
  };
  if (object.type) {
    const values = Object.entries(object.type.value)
      .map((entry) => {
        const [key, value] = entry;
        return `${key}=${JSON.stringify(value)}`;
      })
      .join(', ');
    const name = object.type.name;
    node.text = `${name}(${values})`;
    node.properties = object.type as any;
    (node.properties as any).key = object.key;
    node.componentName = name;
  } else {
    node.text = `<root>`;
  }
  if (object.children) {
    node.children = object.children.map((child) => mapObject(child));
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

interface DisplayNode {
  text: string; // foo(bar=blue)
  componentName: string;
  properties: [string: any];
  children: DisplayNode[];
}
