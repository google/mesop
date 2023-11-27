import { FlatTreeControl } from "@angular/cdk/tree";
import { Component, Input } from "@angular/core";
import {
  MatTreeFlatDataSource,
  MatTreeFlattener,
  MatTreeModule,
} from "@angular/material/tree";
import { CdkTreeModule } from "@angular/cdk/tree";
import { MatIconModule } from "@angular/material/icon";
import { MatButtonModule } from "@angular/material/button";

/** Flat node with expandable and level information */
interface ExampleFlatNode {
  expandable: boolean;
  name: string;
  properties: [string: any];
  level: number;
}

@Component({
  selector: "optic-component-tree",
  templateUrl: "component_tree.ng.html",
  styleUrl: "component_tree.css",
  standalone: true,
  imports: [CdkTreeModule, MatTreeModule, MatButtonModule, MatIconModule],
})
export class ComponentTree {
  @Input({ required: true }) component: InputNode;

  keys() {
    return Object.keys(this.component);
  }
  private _transformer = (node: DisplayNode, level: number) => {
    return {
      expandable: !!node.children && node.children.length > 0,
      name: node.text,
      properties: node.properties,
      level: level,
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

  ngOnInit() {
    this.dataSource.data = [mapObject(this.component)];

    this.treeControl.dataNodes.forEach((node) => {
      if (node.level < 5) {
        this.treeControl.expand(node);
      }
    });
  }

  hasChild = (_: number, node: ExampleFlatNode) => node.expandable;
}

function mapObject(object: InputNode): DisplayNode {
  const node: DisplayNode = { text: "", properties: {} as any, children: [] };
  if (object.type) {
    const values = Object.entries(object.type.value)
      .map((entry) => {
        const [key, value] = entry;
        return `${key}=${value}`;
      })
      .join(", ");
    node.text = `${object.type.name}(${values})`;
  } else {
    node.text = `<root>`;
  }
  if (object.childrenList) {
    node.children = object.childrenList.map((child) => mapObject(child));
  }
  return node;
}

interface InputNode {
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
  properties: [string: any];
  children: DisplayNode[];
}
